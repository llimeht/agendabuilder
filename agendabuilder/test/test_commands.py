# test commands

from pathlib import Path
import re
from typing import (
    Union,
)
import unittest

from reportlab.lib.pagesizes import A4  # type: ignore
from reportlab.pdfgen.canvas import Canvas  # type: ignore

from agendabuilder import commands
from agendabuilder.locator import FileLocator


def find_test_file(filename: Union[str, Path]) -> Path:
    """ find a test file that is located within the test suite """
    return Path(__file__).parent / Path(filename)


class CommandTests(unittest.TestCase):
    # pylint: disable=protected-access

    def setUp(self) -> None:
        self.cfg = find_test_file("meeting.yaml")
        self.locator = FileLocator(self.cfg)

        self.test_pdfs = [
            "agenda-final.pdf",
            "consultation-cover.pdf",
            "consultation report.pdf",
            "consultation report appendices.pdf",
            "consultation-future-cover.pdf",
        ]

    def tearDown(self) -> None:
        other_files = [
            "agenda-draft.docx",
            "meeting-pack.pdf",
        ]
        for f in self.test_pdfs + other_files:
            p = Path(self.locator(f))
            if p.exists():
                p.unlink()

    def _build_test_pdfs(self) -> None:
        for pdf in self.test_pdfs:
            self._build_test_pdf(pdf, "This is %s" % pdf)

    def _build_test_pdf(self, filename: Union[str, Path], text: str) -> None:

        canvas = Canvas(str(self.locator(filename)), pagesize=A4)
        canvas.setFont("Times-Roman", 12)
        canvas.drawString(140, 140, text)
        canvas.save()

    def test_configure(self) -> None:
        """ Test loading the meeting from the config file """
        meeting = commands.configure(self.cfg)
        self.assertEqual(len(meeting.items), 10)

    def test_build_listing(self) -> None:
        """ Test building the docx of the agenda listing """
        # FIXME: this is only a smoke test
        meeting = commands.configure(self.cfg)

        commands.build_listing(meeting, self.locator)

        draft = self.locator(meeting.metadata["agenda_draft"])
        self.assertTrue(draft.exists())

        stat = draft.stat()
        self.assertTrue(stat.st_size > 60000)

    def test_build_pack(self) -> None:
        """ Test building the meeting pack """
        # FIXME: this is only a smoke test
        meeting = commands.configure(self.cfg)

        self._build_test_pdfs()
        commands.build_pack(meeting, self.locator)

        packfile = self.locator(meeting.metadata["meeting_pack"])
        self.assertTrue(packfile.exists())

        stat = packfile.stat()
        self.assertTrue(stat.st_size > 6000)

    def test_main_agenda(self) -> None:
        """ Test main with agenda argument """
        # FIXME: this is only a smoke test
        commands.main(
            [
                "agenda",
                str(self.cfg),
            ]
        )

    def test_main_pack(self) -> None:
        """ Test main with pack argument """
        # FIXME: this is only a smoke test
        self._build_test_pdfs()
        commands.main(
            [
                "pack",
                str(self.cfg),
            ]
        )
