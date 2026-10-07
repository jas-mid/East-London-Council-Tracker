"""Client for the ONS Explore Local Statistics API."""

#ONS has stated their API is "liable to change" as it is in beta stages still
#this file is here to be a single point of failure, making it easy to update

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

import pandas as pd
import requests


#defaults to compare against
BASE_URL = "https://www.ons.gov.uk/explore-local-statistics/api/v1"
HEADERS = {"User-Agent": "EastLondonCouncilTracker/1.0"}
TIMEOUT_SECONDS = 20

#GSS codes of areas to compare against ONS data
LONDON = "E12000007"
ENGLAND = "E92000001"

class OnsError(RuntimeError):
    """Spotting if the ONS API is unreachable or returns something unexpected"""


@dataclass(frozen=True, slots=True)
class Indicator:
    """format for how a single statistic should be displayed"""

    slug: str
    label: str
    topic: str
    subtitle: str
    prefix: str = ""
    suffix: str = ""
    sub_text: str = ""
    decimal_places: int = 1
    source_name: str = ""
    source_url: str = ""

    #taking in the ONS data before normalized
    def format_value(self, value: float) -> str:
        """taking in the format the way ONS initially display it"""
        return f"{self.prefix}{value:,.{self.decimal_places}f}{self.suffix}"


    #chart axis descriptors
    @property
    def unit(self) -> str:
        """unit description for axis titles"""
        return self.sub_text or self.suffix or self.prefix


#----- add notation from here onwards -----


#single function to retrieve a dataset
def _get(path: str, client, **params):
    """GET one API route and return its decoded JSON, or raise OnsError."""
    try:
        response = client.get(f"{BASE_URL}/{path}", params=params, headers=HEADERS, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as error:
        raise OnsError(f"Could not load {path} from the ONS: {error}") from error


def _to_indicator(entry: dict) -> Indicator:
    """Build an Indicator from one entry of the metadata response."""
    sources = entry.get("source") or [{}]
    return Indicator(
        slug=entry["slug"],
        label=entry["label"],
        topic=entry["topic"],
        subtitle=entry.get("subtitle") or "",
        prefix=entry.get("prefix") or "",
        suffix=entry.get("suffix") or "",
        sub_text=entry.get("subText") or "",
        decimal_places=entry.get("decimalPlaces", 1),
        source_name=sources[0].get("name", ""),
        source_url=sources[0].get("href", ""),
    )


def list_indicators(area_type: str = "E09", client=requests) -> tuple[Indicator, ...]:
    """Every single-value indicator ONS publish for a type of area (E09 is London boroughs)."""
    entries = _get("metadata/indicators", client, hasGeo=area_type)
    indicators = (_to_indicator(entry) for entry in entries if not entry.get("isMultivariate"))
    return tuple(sorted(indicators, key=lambda indicator: (indicator.topic, indicator.label)))


def fetch_latest(slug: str, area_codes: tuple[str, ...], client=requests) -> pd.DataFrame:
    """The most recent value of one indicator for each area that has one."""
    rows = _get(f"data/{slug}.rows.json", client, geo=",".join(area_codes), time="latest", measure="value")
    frame = pd.DataFrame(rows, columns=["areacd", "areanm", "period", "value"])
    return frame.rename(columns={"areacd": "code", "areanm": "area"})


#periods come back as a date ("2024-06-30") or a span ("2024-04-01/P1Y")
_SPAN = re.compile(r"^(\d{4}-\d{2}-\d{2})/P(\d+)([YM])$")


def describe_period(period: str) -> str:
    """A readable version of an ONS period, e.g. '2024-04-01/P1Y' -> '1 year from April 2024'."""
    span = _SPAN.match(period)
    if span:
        start, length, unit = date.fromisoformat(span[1]), int(span[2]), span[3]
        if (length, unit) == (1, "M"):
            return f"{start:%B %Y}"
        noun = {"Y": "year", "M": "month"}[unit] + ("s" if length != 1 else "")
        return f"{length} {noun} from {start:%B %Y}"
    try:
        return f"{date.fromisoformat(period):%d %B %Y}".lstrip("0")
    except ValueError:
        return period