"""Tests for council data loading and validation."""
import re
from textwrap import dedent

import pytest

from council_tracker.repository import CouncilDataError, TomlCouncilRepository

GSS_PATTERN = re.compile(r"^E09\d{6}$")


@pytest.fixture(scope="module")
def repository():
    """The real data file the app ships with."""
    return TomlCouncilRepository()


def write_toml(tmp_path, text):
    path = tmp_path / "councils.toml"
    path.write_text(dedent(text), encoding="utf-8")
    return path


# --- the shipped data file ---------------------------------------------------

def test_east_london_group_has_seven_members(repository):
    assert len(repository.members("east_london")) == 7


def test_every_council_has_a_valid_gss_code(repository):
    for council in repository.councils():
        assert GSS_PATTERN.match(council.gss_code), council.name


def test_every_link_is_https(repository):
    for council in repository.councils():
        for link in council.links:
            assert link.url.startswith("https://"), f"{council.name} {link.kind}"


def test_link_kinds_are_ordered(repository):
    orders = [kind.order for kind in repository.link_kinds()]
    assert orders == sorted(orders)


def test_missing_link_kind_returns_none(repository):
    assert repository.get("E09000012").link("not-a-real-kind") is None


# --- validation catches bad data before the app does ---------------------------

def test_duplicate_gss_codes_are_rejected(tmp_path):
    path = write_toml(tmp_path, """
        [[councils]]
        gss_code = "E09000012"
        name = "Hackney"

        [[councils]]
        gss_code = "E09000012"
        name = "Hackney again"
    """)
    with pytest.raises(CouncilDataError, match="Duplicate GSS codes"):
        TomlCouncilRepository(path)


def test_undeclared_link_kind_is_rejected(tmp_path):
    path = write_toml(tmp_path, """
        [[councils]]
        gss_code = "E09000012"
        name = "Hackney"
        links.contcat = "https://example.org"
    """)
    with pytest.raises(CouncilDataError, match="undeclared link kinds"):
        TomlCouncilRepository(path)


def test_group_with_unknown_member_is_rejected(tmp_path):
    path = write_toml(tmp_path, """
        [groups.east_london]
        label = "East London"
        members = ["E09000099"]
    """)
    with pytest.raises(CouncilDataError, match="unknown councils"):
        TomlCouncilRepository(path)
