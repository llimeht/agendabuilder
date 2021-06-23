"""
Representation of the agenda for a meeting
"""

from typing import (
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
)


class ItemNumber:
    def __init__(
        self,
        a: int = 0,
        b: Optional[int] = None,
        c: Optional[int] = None,
    ) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.sep = "."

    def __str__(self) -> str:
        if self.b is None or self.b == 0:
            fmt = "{a}"
        elif self.c is None or self.c == 0:
            fmt = "{a}{sep}{b}"
        else:
            fmt = "{a}{sep}{b}{sep}{c}"

        return fmt.format(a=self.a, b=self.b, c=self.c, sep=self.sep)


class ItemBase:
    def __init__(
        self,
        title: Optional[str] = None,
        cover: Optional[str] = None,
    ) -> None:
        self.cover = cover
        self.title = title
        self.who: Optional[str] = None
        self.num = ItemNumber()
        self.duration = 0
        self.pages: List[str] = []


class AgendaItem(ItemBase):
    def __init__(
        self,
        title: Optional[str] = None,
        cover: Optional[str] = None,
        who: Optional[str] = None,
        pages: Optional[List[str]] = None,
        action: Optional[str] = None,
        starred: bool = False,
    ) -> None:
        super().__init__(title=title, cover=cover)
        self.who = who
        self.pages = pages or []
        self.action = action
        self.num = ItemNumber()
        self.duration = 0
        self.starred = starred


class AgendaHeading(ItemBase):
    def __init__(
        self,
        title: Optional[str] = None,
    ) -> None:
        super().__init__(title=title)


class Agenda:
    def __init__(self, items: Optional[List[ItemBase]] = None):
        self.items = items or []
        self.metadata: Dict[str, str] = {}
        self.number_items()

    def append(self, item: ItemBase) -> None:
        self.items.append(item)
        self.number_items()

    def extend(self, items: List[ItemBase]) -> None:
        self.items.extend(items)
        self.number_items()

    def number_items(self) -> None:
        section = 0
        subsection = 0
        for item in self.items:
            if isinstance(item, AgendaHeading):
                section += 1
                subsection = 0
            if isinstance(item, AgendaItem):
                subsection += 1
            item.num.a = section
            item.num.b = subsection

    def enclosures(self) -> Iterator[Tuple[str, str, str, List[str]]]:
        for item in self.items:
            num = str(item.num)
            title = "{num} {title}".format(
                num=num,
                title=item.title,
            )
            if item.cover:
                yield (num, title, item.cover, item.pages)

    def __str__(self) -> str:
        s = []
        s.append("Agenda")
        s.append("")
        for item in self.items:
            s.append("% 5s: %-50s [%s]" % (item.num, item.title, item.who))
        return "\n".join(s)
