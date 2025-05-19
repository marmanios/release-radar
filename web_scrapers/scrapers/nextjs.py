# scrapers/nextjs.py

import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from logger import setup_logger
from utils.helpful_types import ScraperOutput


SOURCE_NAME = "nextJS"
URL = "https://github.com/vercel/next.js/releases"
MAX_DEPTH = 10 # NextJS changelog has all the canary releases so we need to go through a few pages to find the latest stable release. 

def fetch_nextJS() -> ScraperOutput | None:
    logger = setup_logger("nextJS", "web_scrapers/logs/nextJS.log" )
    logger.info("Fetching nextJS changelog...")

    for i in range(1, MAX_DEPTH + 1):
        logger.info(f"Fetching page {i} of the nextJS changelog...")
        page = requests.get(URL + f"?page={i}")

        changelog = page.text
        if not changelog:
            logger.error("Changelog not found in the document.")
            return None

        soup = BeautifulSoup(page.content, "html.parser")
        releases = soup.find_all("section")
        for release in releases:
            release_tag = release.find("h2")
            if not release_tag:
                continue
            release_name = release_tag.text.lower().strip()
            logger.info(f"Found release: {release_name}")
            if "canary" in release_name:
                continue

            # if here we found a stable release, let's extract its details
            release_page = requests.get(URL + f"/tag/{release_name}")
            release_soup = BeautifulSoup(release_page.content, "html.parser")
            changelog = release_soup.find("div", id="repo-content-pjax-container")
            if not changelog:
                logger.error("Changelog not found in the release page.")
                return None
            
            # capture release date
            date_tag = release_soup.find("relative-time")
            if not date_tag:
                logger.error("Release date not found in the release page.")
                return None
            
            date = date_tag["datetime"]

            body = release_soup.find("div", class_="markdown-body my-3")
            if not body:
                logger.error("Release body not found in the release page.")
                return None
            

            return {
                "source": SOURCE_NAME,
                "version": release_name,
                "release_date": date,
                "changes_raw": body.prettify(),
                "link": URL + f"/tag/{release_name}",
            }
            

if __name__ == " __main__":
    fetch_nextJS()