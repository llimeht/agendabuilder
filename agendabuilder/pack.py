"""
Representation of the meeting pack for a meeting
"""

import io

from typing import (
    Callable,
    IO,
    Optional,
    Tuple,
    Union,
)

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger  # type: ignore
from reportlab.pdfgen import canvas  # type: ignore
import reportlab.lib.colors  # type: ignore

from .meeting import Agenda


class AgendaPdfPart:
    def __init__(
        self,
        fh: Optional[Union[IO[bytes], str]] = None,
    ) -> None:
        self.fh = fh  # can actually be a file handle or filename
        self.font_name = "Helvetica"
        self.font_size = 9
        self.font_color = "#000000"
        self.location = (0.0, 0.0)
        # mode is: first = first page only; repeat = same every page; match = 1:1
        self.mode = "first"

    def page_size(self, num: int = 0) -> Tuple[float, float]:
        reader = PdfFileReader(self.fh)
        box = reader.getPage(num).mediaBox
        return (float(box.getWidth()), float(box.getHeight()))

    def num_pages(self) -> int:
        pdf = PdfFileReader(self.fh)
        return pdf.getNumPages()  # type: ignore

    def stamp(self, stamp: PdfFileReader) -> IO[bytes]:
        output = PdfFileWriter()

        original_pdf = PdfFileReader(self.fh)

        if self.mode not in ("first", "repeat", "match"):
            raise ValueError("Unknown stamping mode '%s'" % self.mode)

        if self.mode in ("first", "repeat"):
            overlay = stamp.getPage(0)

        for page_num in range(original_pdf.getNumPages()):
            print(" processing page %d" % page_num)

            # add the stamp to the existing page
            page = original_pdf.getPage(page_num)

            if self.mode == "match":
                overlay = stamp.getPage(page_num)
            elif self.mode == "first" and page_num > 0:
                overlay = None

            if overlay:
                page.mergePage(overlay)

            output.addPage(page)

        buffer = io.BytesIO()
        output.write(buffer)

        buffer.seek(0)
        return buffer

    def as_pdf_stream(self) -> IO[bytes]:
        stamp = self.stamp_stream()
        return self.stamp(stamp)

    def stamp_stream(
        self,
        texter: Optional[Callable[[canvas.Canvas, float, float], None]] = None,
    ) -> PdfFileReader:
        # prepare the text stamp
        buffer = io.BytesIO()

        size = self.page_size(0)
        layer = canvas.Canvas(buffer, pagesize=size)

        x, y = [float(v) for v in self.location]
        x = float(x if (x > 0) else x + size[0])
        y = float(y if (y > 0) else y + size[1])
        # print("Marking at (%f, %f) / (%f, %f)" % (x, y, size[0], size[1]))

        texter = texter or self._default_texter
        texter(layer, x, y)

        layer.save()
        buffer.seek(0)

        stamp = PdfFileReader(buffer)
        return stamp

    def _default_texter(
        self,
        layer: canvas.Canvas,
        x: float,
        y: float,
    ) -> None:
        pass

    def __call__(self) -> IO[bytes]:
        return self.as_pdf_stream()


class AgendaPageNumPdfPart(AgendaPdfPart):
    def __init__(
        self,
        fh: Union[IO[bytes], str],
        start: int,
    ) -> None:
        super().__init__(fh=fh)
        self.location = (292.0, 40.0)
        self.format = "{num}"
        self.mode = "match"
        self.font_color = "#ff0000"
        self.start = start

    def _default_texter(
        self,
        layer: canvas.Canvas,
        x: float,
        y: float,
    ) -> None:
        color = reportlab.lib.colors.HexColor(self.font_color)
        for page in range(self.num_pages()):
            layer.setFillColor(color)
            layer.setFont(self.font_name, self.font_size)
            layer.drawCentredString(
                x, y, self.format.format(num=str(page + self.start))
            )
            layer.showPage()


class AgendaCoverPdfPart(AgendaPdfPart):
    def __init__(
        self,
        fh: Union[IO[bytes], str],
        num: str,
    ) -> None:
        super().__init__(fh)
        self.num = num
        # in point (x, y) with -ve being from the top right
        self.location = (297.5, -90.5)
        self.font_name = "Helvetica"
        self.font_size = 9
        self.format = "{num}"
        self.mode = "first"

    def _default_texter(self, layer: canvas.Canvas, x: float, y: float) -> None:
        color = reportlab.lib.colors.HexColor(self.font_color)
        layer.setFillColor(color)
        layer.setFont(self.font_name, self.font_size)
        layer.drawRightString(x, y, self.format.format(num=str(self.num)))
        layer.showPage()


class MeetingPack:
    def __init__(self, meeting: Agenda, agendapdf: str) -> None:
        self.meeting = meeting
        self.agendapdf = agendapdf
        self.agenda_bookmark = "Agenda"
        self.buffer = io.BytesIO()

    def build(self) -> None:
        merger = PdfFileMerger()
        pagenum = 1

        def append(
            stream: IO[bytes], bookmark: Optional[str], filename: Optional[str]
        ) -> int:
            pdf_reader = PdfFileReader(stream)
            numpages = pdf_reader.getNumPages()  # type: int
            merger.append(pdf_reader, bookmark=bookmark, import_bookmarks=False)
            print("  Merged file: %s [%s] " % (filename, bookmark))
            return numpages

        numberer = AgendaPageNumPdfPart(self.agendapdf, pagenum)
        pagenum += append(numberer(), self.agenda_bookmark, self.agendapdf)

        for itemnum, bookmark, filename, extras in self.meeting.enclosures():
            print("Item: [%s]" % (bookmark))
            # pass pdf stream through stampers
            coverer = AgendaCoverPdfPart(filename, itemnum)
            numberer = AgendaPageNumPdfPart(coverer(), pagenum)
            pagenum += append(numberer(), bookmark, filename)
            for extra_filename in extras:
                with open(extra_filename, "rb") as fh:
                    numberer = AgendaPageNumPdfPart(fh, pagenum)
                    pagenum += append(numberer(), None, extra_filename)

        merger.write(self.buffer)

        self.buffer.seek(0)

    def save(self, filename: str) -> None:
        with open(filename, "wb") as fh:
            fh.write(self.buffer.getvalue())
