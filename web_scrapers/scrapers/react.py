# scrapers/react.py

import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from logger import setup_logger
from utils.helpful_types import ScraperOutput


SOURCE_NAME = "react"
URL = "https://raw.githubusercontent.com/facebook/react/refs/heads/main/CHANGELOG.md"

def fetch_react() -> ScraperOutput | None:
    logger = setup_logger("react", "web_scrapers/logs/react.log" )
    logger.info("Fetching React changelog...")
    page = requests.get(URL)

    changelog = page.text
    if not changelog:
        logger.error("Changelog not found in the document.")
        return None

    # Captures the full patch block including all text until the next '## ' or end of document
    pattern = r'(^## .+?\([A-Za-z]+ \d{1,2}, \d{4}\).*?)(?=^## |\Z)'
    matches = re.findall(pattern, changelog, re.DOTALL | re.MULTILINE)

    if not matches or len(matches) == 0:
        logger.error("No patch sections found in the changelog.")
        return None

    newest_patch_text = matches[0]
    
    # Extract the patch version and patch date from the first match
    header_line = newest_patch_text.splitlines()[0]
    date_match = re.search(r'\(([A-Za-z]+ \d{1,2}, \d{4})\)', header_line)
    version_match = re.search(r'##\s+([0-9]+(?:\.[0-9]+){1,2})', header_line)

    if not date_match or not version_match:
        logger.error(f"Could not find version or date in the patch header.  Date found: {date_match}, Version found: {version_match}")
        return None

    return {
        "source": SOURCE_NAME,
        "version": version_match.group(1),
        "release_date":  date_match.group(1),
        "changes_raw": matches[0].strip(),
        "link": "https://github.com/facebook/react/blob/main/CHANGELOG.md",
    }

if __name__ == " __main__":
    fetch_react()