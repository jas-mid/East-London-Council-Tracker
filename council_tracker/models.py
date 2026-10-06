"""Domain models for councils and the pages they publish."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LinkKind:
    """A category of council web page, and how the UI should present it."""

    key: str
    label: str
    icon: str
    blurb: str = ""
    order: int = 100


@dataclass(frozen=True, slots=True)
class CouncilLink:
    """One published page belonging to a council."""

    kind: str
    url: str


@dataclass(frozen=True, slots=True)
class Council:
    """A local authority, identified by its ONS GSS code."""

    gss_code: str
    name: str
    links: tuple[CouncilLink, ...] = ()

    def link(self, kind: str) -> CouncilLink | None:
        """This council's page of the given kind, or None if none is recorded."""
        return next((link for link in self.links if link.kind == kind), None)


@dataclass(frozen=True, slots=True)
class CouncilGroup:
    """A named set of councils, such as the boroughs the app compares."""

    key: str
    label: str
    members: tuple[str, ...]
