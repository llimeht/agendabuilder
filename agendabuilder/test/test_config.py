# test loading of config

from pathlib import Path
import re
from typing import (
    Union,
)
import unittest

from agendabuilder import config
from agendabuilder.meeting import AgendaHeading, AgendaItem


def find_test_file(filename: Union[str, Path]) -> Path:
    """ find a test file that is located within the test suite """
    return Path(__file__).parent / Path(filename)


class ConfigTests(unittest.TestCase):
    # pylint: disable=protected-access

    def setUp(self) -> None:
        self.cfg = find_test_file("meeting.yaml")

    def test_load_config(self) -> None:
        """ Test loading config file """
        meeting = config.load(self.cfg)

        self.assertEqual(len(meeting.items), 10)

        self.assertTrue(isinstance(meeting.items[0], AgendaHeading))
        self.assertEqual(meeting.items[0].title, "Procedural matters")
        self.assertTrue(isinstance(meeting.items[4], AgendaItem))
        self.assertEqual(meeting.items[4].title, "Chair's report")
        self.assertTrue(meeting.items[7].starred)  # type: ignore
        self.assertEqual(meeting.items[6].who, "ABC")
        self.assertEqual(meeting.metadata["location"], "Null Island")
