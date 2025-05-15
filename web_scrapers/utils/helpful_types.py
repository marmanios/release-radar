# utils/helpful_types.py

from typing import TypedDict


class ScraperOutput(TypedDict):
    source: str
    version: str
    release_date: str
    changes_html: str
    link: str

class RefinedOutput(TypedDict):
    source: str
    version: str
    release_date: str
    changes_markdown: str
    link: str