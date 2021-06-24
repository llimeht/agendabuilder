import argparse
from pathlib import Path

from typing import (
    List,
    Optional,
    Union,
)

from .meeting import Agenda
from .agendalisting import AgendaListing
from .pack import MeetingPack
from . import config
from .locator import FileLocator


def configure(filename: Union[str, Path]) -> Agenda:
    meeting = config.load(filename)
    print(meeting)
    return meeting


def build_listing(meeting: Agenda, locator: FileLocator) -> None:
    agenda_template = meeting.metadata["agenda_template"]
    agenda_draft = meeting.metadata["agenda_draft"]

    listing = AgendaListing(meeting, agenda_template, locator)
    listing.build()
    listing.save(agenda_draft)


def build_pack(meeting: Agenda, locator: FileLocator) -> None:
    agenda_final = meeting.metadata["agenda_final"]
    meeting_pack = meeting.metadata["meeting_pack"]

    pack = MeetingPack(meeting, agenda_final, locator)
    pack.build()
    pack.save(meeting_pack)


def main(argv: Optional[List[str]] = None) -> int:
    """agendabuilder: builds an agenda for a meeting

    ---
    Examples:

    Build the agenda as a Word document

        agendabuilder agenda meeting.yaml

    Combine the agenda and all attachments into a meeting pack

        agendabuilder pack meeting.yaml

    The 'meeting.yaml' file contains information about the files that
    are to be used for the templates and attachments, along with the
    details of each agenda item.
    """
    # Get the help information out of the docstring for the file
    (description, examples) = main.__doc__.split("---")  # type: ignore

    parser = argparse.ArgumentParser(
        description=description,
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # create sub commands for each action to be performed
    subparsers = parser.add_subparsers(dest="step")
    subparsers.required = True

    # agenda builder
    agenda_parser = subparsers.add_parser(
        "agenda", help="build the agenda as a Word document"
    )

    agenda_parser.add_argument(
        "config", metavar="meeting.yaml", help="meeting configuration file"
    )

    # meeting pack builder
    pack_parser = subparsers.add_parser(
        "pack", help="build the meeting pack fro the PDF documents"
    )

    pack_parser.add_argument(
        "config", metavar="meeting.yaml", help="meeting configuration file"
    )

    args = parser.parse_args(argv)

    config_filename = args.config
    run_build_listing = args.step == "agenda"
    run_build_pack = args.step == "pack"

    meeting = configure(config_filename)
    locator = FileLocator(config_filename)

    if run_build_listing:
        build_listing(meeting, locator)

    if run_build_pack:
        build_pack(meeting, locator)

    return 0
