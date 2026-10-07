"""Tests for the link health checker, using a fake HTTP client instead of the network."""
#created by claude code
#I hate writing tests lol

from types import SimpleNamespace

import pytest
import requests

from council_tracker.health_checker import Health, check_councils, check_url, classify
from council_tracker.models import Council, CouncilLink

URL = "https://www.example.gov.uk/contact-us"


class FakeClient:
    """Stands in for `requests`, answering each method from a canned response."""

    def __init__(self, head, get=None):
        self._responses = {"head": head, "get": get or head}
        self.calls = []

    def _respond(self, method, url):
        self.calls.append(method)
        answer = self._responses[method]
        if isinstance(answer, Exception):
            raise answer
        status, final_url = answer
        return SimpleNamespace(status_code=status, url=final_url or url, close=lambda: None)

    def head(self, url, **kwargs):
        return self._respond("head", url)

    def get(self, url, **kwargs):
        return self._respond("get", url)


@pytest.mark.parametrize(
    ("status", "final_url", "expected"),
    [
        (200, URL, Health.OK),
        (200, URL + "/", Health.OK),
        (200, "https://www.example.gov.uk/new-contact", Health.MOVED),
        (403, URL, Health.UNVERIFIED),
        (429, URL, Health.UNVERIFIED),
        (404, URL, Health.BROKEN),
        (500, URL, Health.BROKEN),
    ],
)
def test_classify(status, final_url, expected):
    assert classify(URL, status, final_url) is expected


def test_healthy_link_needs_only_a_head_request():
    client = FakeClient(head=(200, None))
    assert check_url("Hackney", "contact", URL, client).health is Health.OK
    assert client.calls == ["head"]


def test_failed_head_is_confirmed_with_a_get():
    client = FakeClient(head=(405, None), get=(200, None))
    assert check_url("Hackney", "contact", URL, client).health is Health.OK
    assert client.calls == ["head", "get"]


def test_redirect_reports_the_new_address():
    client = FakeClient(head=(200, "https://www.example.gov.uk/new-contact"))
    check = check_url("Hackney", "contact", URL, client)
    assert check.health is Health.MOVED
    assert check.final_url == "https://www.example.gov.uk/new-contact"


def test_timeout_is_unverified_not_broken():
    client = FakeClient(head=requests.Timeout())
    check = check_url("Hackney", "contact", URL, client)
    assert check.health is Health.UNVERIFIED
    assert check.detail == "timed out"


def test_connection_failure_is_broken():
    client = FakeClient(head=requests.ConnectionError())
    check = check_url("Hackney", "contact", URL, client)
    assert check.health is Health.BROKEN
    assert check.detail == "ConnectionError"


def test_check_councils_checks_every_link_of_every_council():
    councils = [
        Council("E09000012", "Hackney", (CouncilLink("contact", URL), CouncilLink("voting", URL + "/vote"))),
        Council("E09000025", "Newham", (CouncilLink("contact", URL + "/newham"),)),
        Council("E09000001", "City of London"),
    ]
    checks = check_councils(councils, client=FakeClient(head=(200, None)))
    assert {(c.council, c.kind) for c in checks} == {
        ("Hackney", "contact"),
        ("Hackney", "voting"),
        ("Newham", "contact"),
    }
