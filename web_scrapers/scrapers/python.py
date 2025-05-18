# scrapers/python.py

import requests
from bs4 import BeautifulSoup
from logger import setup_logger
from utils.helpful_types import ScraperOutput

SOURCE_NAME = "python"
URL = "https://docs.python.org/3/whatsnew/changelog.html"

def fetch_python() -> ScraperOutput | None:
    logger = setup_logger("python", "web_scrapers/logs/python.log" )
    logger.info("Fetching Python changelog...")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")


    changelog = soup.find("section", id="changelog")
    # Get the latest version by finding the section after 'python-next'
    python_next_section = changelog.find("section", id="python-next")
    newest_version = python_next_section.find_next_sibling("section")

    # Find parameters
    return {
        "source": SOURCE_NAME,
        "version": newest_version.find("h2").text,
        "release_date":  newest_version.find("p").find("em").text[-10:],
        "changes_raw": newest_version.prettify(),
        "link": URL + newest_version.find("h2").find("a")["href"],
    }

if __name__ == " __main__":
    fetch_python()