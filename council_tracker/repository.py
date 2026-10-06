"""Where council data comes from.

Pages depend on the `CouncilRepository` protocol rather than on TOML, so a new
source (a cached ONS snapshot, a database) can be added later without
modifying any page that consumes it.
"""
from __future__ import annotations

import tomllib
from collections import Counter
from functools import cache
from pathlib import Path
from typing import Protocol

from council_tracker.models import Council, CouncilGroup, CouncilLink, LinkKind
from council_tracker.paths import DATA_DIR

DEFAULT_PATH = DATA_DIR / "councils.toml"


class CouncilDataError(ValueError):
    """The council data is internally inconsistent."""


class CouncilRepository(Protocol):
    """Anything that can supply councils, their groupings, and link kinds."""

    def councils(self) -> tuple[Council, ...]: ...

    def get(self, gss_code: str) -> Council: ...

    def link_kinds(self) -> tuple[LinkKind, ...]: ...

    def groups(self) -> tuple[CouncilGroup, ...]: ...

    def group(self, key: str) -> CouncilGroup: ...

    def members(self, group_key: str) -> tuple[Council, ...]: ...


class TomlCouncilRepository:
    """Council data read from a TOML file and validated as it loads."""

    def __init__(self, path: Path = DEFAULT_PATH) -> None:
        with path.open("rb") as handle:
            document = tomllib.load(handle)

        entries = document.get("councils", [])
        duplicates = sorted(code for code, n in Counter(e["gss_code"] for e in entries).items() if n > 1)
        if duplicates:
            raise CouncilDataError(f"Duplicate GSS codes: {duplicates}")

        self._link_kinds = tuple(
            sorted(
                (LinkKind(**entry) for entry in document.get("link_kinds", [])),
                key=lambda kind: (kind.order, kind.label),
            )
        )
        self._councils = {
            entry["gss_code"]: Council(
                gss_code=entry["gss_code"],
                name=entry["name"],
                links=tuple(CouncilLink(kind, url) for kind, url in entry.get("links", {}).items()),
            )
            for entry in entries
        }
        self._groups = {
            key: CouncilGroup(key=key, label=entry["label"], members=tuple(entry["members"]))
            for key, entry in document.get("groups", {}).items()
        }
        self._validate()

    def _validate(self) -> None:
        declared = {kind.key for kind in self._link_kinds}
        for council in self._councils.values():
            undeclared = sorted({link.kind for link in council.links} - declared)
            if undeclared:
                raise CouncilDataError(f"{council.name} uses undeclared link kinds: {undeclared}")

        for group in self._groups.values():
            unknown = sorted(set(group.members) - self._councils.keys())
            if unknown:
                raise CouncilDataError(f"Group {group.key!r} references unknown councils: {unknown}")

    def councils(self) -> tuple[Council, ...]:
        return tuple(sorted(self._councils.values(), key=lambda council: council.name))

    def get(self, gss_code: str) -> Council:
        return self._councils[gss_code]

    def link_kinds(self) -> tuple[LinkKind, ...]:
        return self._link_kinds

    def groups(self) -> tuple[CouncilGroup, ...]:
        return tuple(self._groups.values())

    def group(self, key: str) -> CouncilGroup:
        return self._groups[key]

    def members(self, group_key: str) -> tuple[Council, ...]:
        codes = self._groups[group_key].members
        return tuple(sorted((self._councils[code] for code in codes), key=lambda council: council.name))


@cache
def get_repository() -> CouncilRepository:
    """The repository the app uses. Swap the implementation here, and only here."""
    return TomlCouncilRepository()
