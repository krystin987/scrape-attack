import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit

import bs4.element
from bs4 import BeautifulSoup
import requests

CACHE_DIR = Path(os.getenv("XDG_CACHE_DIR") or os.path.expanduser("~/.cache")) / "StationIndex"
TREE_BUILDER = "lxml"
URL_BASE = "https://www.stationindex.com"


def _rectify_key(text):
    text = text.lower()
    return "_id" if text == "id" else text


def download(
        page_url: str,
        path: os.PathLike,
        session: Optional[requests.sessions.Session] = None,
):
    path = Path(path)  # wrap a filename with the Python Path handler
    # The Session context manager can re-use a TCP connection for efficiency
    response = (session or requests).get(f"{URL_BASE}/{page_url}")
    response.raise_for_status()  # throws an exception when appropriate

    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_bytes(response.content)
    return path


def get_station_owners(refresh=False,
                       session: Optional[requests.sessions.Session] = None):
    page_url = "tv/by-owner/"  # suffix on URL to fetch
    path = CACHE_DIR / "tv/by-owner/index.html"  # Local path caching the page
    if not path.exists() or refresh:
        download(page_url, path, session=session)
    return parse_by_owner(path.read_bytes())


def parse_by_owner(content: bytes):
    soup = BeautifulSoup(content, TREE_BUILDER)

    results = {}
    for n, row in enumerate(soup.find_all(
            "div",
            attrs={"class": "col-sm-6"}  # discovered by trial-and-error
    )):
        for anchor in row.find_all("a"):
            link = urlsplit(anchor.attrs["href"])
            results[anchor.text.strip()] = link
    return results


def get_stations_by_owner(name, refresh=False,
                          session: Optional[requests.sessions.Session] = None):
    page_url = f"tv/by-owner/{name}"  # suffix on URL to fetch
    path = CACHE_DIR / "tv/by-owner" / name.replace("+", "_").replace(" ", "_")  # Local path caching the page
    if not path.exists() or refresh:
        download(page_url, path, session=session)
    return parse_stations_by_owner(path.read_bytes(), owner=path.stem)


def parse_stations_by_owner(content: bytes, owner: str):
    soup = BeautifulSoup(content, TREE_BUILDER)

    results = {}
    for n, parent in enumerate(soup.find_all("p"), start=1):
        key = None
        value = None

        station_dict = {}
        for tag in parent:
            if key is None and tag.name == "b":
                key = "callsign"
                callsign_anchor = tag.find("a")
                value = (
                    callsign_anchor.text,
                    callsign_anchor.attrs["href"],
                    get_station_info_by_callsign(callsign_anchor.text),
                )
            elif tag.name == "a":
                value = (
                    tag.text.strip(),
                    tag.attrs["href"],
                )
            elif tag.name == "span":
                key = tag.text.strip(": ")
            elif isinstance(tag, bs4.element.NavigableString):
                value = tag.text.strip().strip('"')
            else:
                continue
            if key and value:
                station_dict[_rectify_key(key)] = value
                key = None
                value = None
        if station_dict:
            results[station_dict.get("ID", f"{owner}-{n}")] = station_dict
    return results


def get_station_info_by_callsign(callsign, refresh=False,
                                 session: Optional[requests.sessions.Session] = None):
    page_url = f"tv/callsign/{callsign}"  # suffix on URL to fetch
    path = CACHE_DIR / "tv/callsign" / callsign.replace("+", "_").replace(" ", "_")  # Local path caching the page
    if not path.exists() or refresh:
        download(page_url, path, session=session)
    return parse_station_by_callsign(path.read_bytes())


def parse_station_by_callsign(content: bytes):
    soup = BeautifulSoup(content, TREE_BUILDER)

    results = {}
    for parent in soup.find_all("p"):
        key = None
        value = None
        for child in parent:
            if isinstance(child, bs4.element.NavigableString):
                value = child.text.strip().strip('"')
            elif child.name == "font":
                key = child.text.strip(": ")
            elif child.name in {"a", "b"}:
                value = child.text.strip()
            else:
                continue
            if key and value:
                results[_rectify_key(key)] = value
                key = None
                value = None
    return results
