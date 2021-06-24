# test loading of config

from pathlib import Path
import re
from typing import (
    Union,
)
import unittest

from agendabuilder import config
from agendabuilder.meeting import AgendaItem, AgendaHeading, ItemNumber


def find_test_file(filename: Union[str, Path]) -> Path:
    """ find a test file that is located within the test suite """
    return Path(__file__).parent / Path(filename)


class AgendaTests(unittest.TestCase):
    # pylint: disable=protected-access

    def setUp(self) -> None:
        self.cfg = find_test_file("meeting.yaml")

    def test_str(self) -> None:
        """ Test turning agenda into str """
        meeting = config.load(self.cfg)

        text = str(meeting)

        self.assertTrue(text.startswith("Agenda"))
        self.assertIn("Chair's report", text)
        self.assertIn("Business without notice", text)

    def test_building(self) -> None:
        """ Test building the agenda by hand """
        meeting = config.load(self.cfg)

        current_len = len(meeting.items)
        a = AgendaHeading("Yet more meeting")
        meeting.append(a)

        self.assertEqual(len(meeting.items), current_len + 1)

        current_len = len(meeting.items)
        a1 = AgendaItem("Endless discussion")
        a2 = AgendaItem("Longer discussion")
        a3 = AgendaItem("Overtime discussion")
        meeting.extend([a1, a2, a3])

        self.assertEqual(len(meeting.items), current_len + 3)

    def test_enclosures(self) -> None:
        """ Test building the agenda by hand """
        meeting = config.load(self.cfg)

        enc = meeting.enclosures()

        num, title, cover, pages = next(enc)
        self.assertEqual(num, "3.1")
        self.assertEqual(title, "3.1 Consultation report on design")
        self.assertEqual(cover, "consultation-cover.pdf")
        self.assertEqual(len(pages), 2)
        self.assertEqual(pages[0], "consultation report.pdf")

        num, title, cover, pages = next(enc)
        self.assertEqual(num, "3.2")
        self.assertEqual(cover, "consultation-future-cover.pdf")
        self.assertEqual(len(pages), 0)


class ItemNumberTests(unittest.TestCase):
    def setUp(self) -> None:
        self.num1part = ItemNumber(42)
        self.num2part = ItemNumber(13, 1)
        self.num3part = ItemNumber(7, 4, 2)

    def test_init(self) -> None:
        """ Test multi-part item creation """
        self.assertEqual(self.num1part.a, 42)
        self.assertEqual(self.num1part.b, None)
        self.assertEqual(self.num1part.c, None)

        self.assertEqual(self.num2part.a, 13)
        self.assertEqual(self.num2part.b, 1)
        self.assertEqual(self.num2part.c, None)

        self.assertEqual(self.num3part.a, 7)
        self.assertEqual(self.num3part.b, 4)
        self.assertEqual(self.num3part.c, 2)

    def test_str(self) -> None:
        """ Test item serialisation to string """
        self.assertEqual(str(self.num1part), "42")
        self.assertEqual(str(self.num2part), "13.1")
        self.assertEqual(str(self.num3part), "7.4.2")

    def test_custom_sep(self) -> None:
        """ Test use of custom separator """
        self.num3part.sep = "-"
        self.assertEqual(str(self.num3part), "7-4-2")
