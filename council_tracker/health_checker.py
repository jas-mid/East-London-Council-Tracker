"""Checks all webpage links to find their state and ensure they are healthy"""
#run independently before app to make sure links all function
## python -m council_tracker.health_checker

from __future__ import annotations

import sys
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum

import requests

from council_tracker.models import Council
#setting up user agent
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; EastLondonCouncilTracker/1.0)"}
TIMEOUT_SECONDS = 10
#allowance for bot protection
UNVERIFIABLE_STATUSES = frozenset({401, 403, 429})


#health status class
class Health(Enum):
    OK = "ok"
    MOVED = "moved"
    UNVERIFIED = "unverified"
    BROKEN = "broken"


#link check output
@dataclass (frozen=True, slots=True)
class LinkCheck:
    #outputs from when a link is checked
    council: str
    kind: str
    url: str
    health: Health
    status: int | None = None
    final_url: str | None = None
    detail: str = ""
    

#translating http response to format for code to work with
def classify(url: str, status: int, final_url: str) -> Health:
    #selection depending on http response
    if status in UNVERIFIABLE_STATUSES:
        return Health.UNVERIFIED
    if status >= 400:
        return Health.BROKEN
    if url.rstrip("/") != final_url.rstrip("/"):
        return Health.MOVED
    return Health.OK

#actual link checking
def check_url(council: str, kind: str, url: str, client=requests) -> LinkCheck:
    #Check one URL. `client` is anything with requests-style head() and get().
    try:
        response = client.head(url, headers=HEADERS, timeout=TIMEOUT_SECONDS, allow_redirects=True)
        if response.status_code >= 400:
            # Some servers mishandle HEAD, so confirm with a real GET before judging.
            response = client.get(
                url, headers=HEADERS, timeout=TIMEOUT_SECONDS, allow_redirects=True, stream=True
            )
            response.close()
    #for if the link doesn't normally work
    except requests.Timeout:
        #if it times out
        return LinkCheck(council, kind, url, Health.UNVERIFIED, detail="timed out")
    except requests.RequestException as error:
        #if an error is returned
        return LinkCheck(council, kind, url, Health.BROKEN, detail=type(error).__name__)

    #creating returns for the link check with health status
    health = classify(url, response.status_code, response.url)
    return LinkCheck(council, kind, url, health, response.status_code, response.url)

#function that iterates through every council to check status
def check_councils(councils: Iterable[Council], client=requests, max_workers: int=8) -> tuple[LinkCheck,...]:
    #defining 1 'job'
    jobs = [(council.name, link.kind, link.url) for council in councils for link in council.links]
    #iterating through jobs using threads for faster iteration
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return tuple(pool.map(lambda job: check_url(*job, client = client), jobs))

def main() -> int:
    #prints a report of every link. returns 1 if any links are broken
    from council_tracker.repository import get_repository

    checks = check_councils(get_repository().councils())
    for check in sorted(checks, key=lambda c: (c.council, c.kind)):
        print(f"{check.health.value.upper():<11}{check.status or '-':<5}{check.council:<20}{check.kind:<10}{check.url}")
        if check.health is Health.MOVED:
            print(f"{'':<36}now at {check.final_url}")
        elif check.detail:
            print(f"{'':<36}{check.detail}")
    #determining the amount of broken links#
    broken = sum(check.health is Health.BROKEN for check in checks)
    print(f"\n{len(checks)} links checked, {broken} broken.")
    return 1 if broken else 0

if __name__ == "__main__":
    sys.exit(main())