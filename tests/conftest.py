"""Shared test setup."""
import pytest
import streamlit as st

from council_tracker import health_checker

#fixing all reports to healthy
@pytest.fixture(autouse=True)
def no_network_link_checks(monkeypatch):
    """bypasses real council checks and returns all as healthy"""

    def all_ok(councils, **kwargs):
        return tuple(
            health_checker.LinkCheck(council.name, link.kind, link.url, health_checker.Health.OK, 200, link.url)
            for council in councils
            for link in council.links
        )

    #sets attributes to all good and clears cache
    monkeypatch.setattr(health_checker, "check_councils", all_ok)
    st.cache_data.clear()