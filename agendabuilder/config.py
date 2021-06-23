from typing import List

import ruamel.yaml

from .meeting import Agenda, AgendaItem, AgendaHeading, ItemBase


def load(filename: str) -> Agenda:
    with open(filename, "rt") as fh:
        details = ruamel.yaml.safe_load(fh)  # type: ignore

    meeting_items: List[ItemBase] = []

    for part in details:
        if "heading" in part:
            heading = AgendaHeading(title=part["heading"])
            meeting_items.append(heading)

        elif "item" in part:
            item = AgendaItem(
                title=part["item"],
                who=part.get("who", ""),
                cover=part.get("cover", None),
                pages=part.get("pages", None),
                starred=part.get("starred", False),
                action=part.get("action", "Note"),
            )
            meeting_items.append(item)
        elif "metadata" in part:
            metadata = part["metadata"]
        else:
            raise ValueError("Don't know how to understand this part: " + str(part))

    meeting = Agenda(meeting_items)
    meeting.metadata = metadata

    return meeting
