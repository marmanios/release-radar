# scrapers/nextjs.py

import requests
from bs4 import BeautifulSoup
from utils.helpful_types import ScraperOutput
from scrapers.scraper import ScraperBaseClass
from typing import Optional

class NextJsScraper(ScraperBaseClass):
    @property
    def name(self) -> str:
        return "nextJS"
    
    @property
    def url(self) -> str:
        return "https://github.com/vercel/next.js/releases"
    
    def scrape(self) -> Optional[ScraperOutput]:
        MAX_DEPTH = 10
        try:
            self.logger.info("Fetching nextJS changelog...")

            for i in range(1, MAX_DEPTH + 1):
                self.logger.info(f"Fetching page {i} of the nextJS changelog...")
                page = requests.get(self.url + f"?page={i}")
                page.raise_for_status() 

                changelog = page.text
                if not changelog:
                    self.logger.error("Changelog not found in the document.")
                    return None

                soup = BeautifulSoup(page.content, "html.parser")
                releases = soup.find_all("section")
                for release in releases:
                    release_tag = release.find("h2")
                    if not release_tag:
                        continue
                    release_name = release_tag.text.lower().strip()
                    self.logger.info(f"Found release: {release_name}")
                    if "canary" in release_name:
                        continue

                    # if here we found a stable release, let's extract its details
                    release_page = requests.get(self.url + f"/tag/{release_name}")
                    release_page.raise_for_status() 

                    release_soup = BeautifulSoup(release_page.content, "html.parser")
                    changelog = release_soup.find("div", id="repo-content-pjax-container")
                    if not changelog:
                        self.logger.error("Changelog not found in the release page.")
                        return None
                    
                    # capture release date
                    date_tag = release_soup.find("relative-time")
                    if not date_tag:
                        self.logger.error("Release date not found in the release page.")
                        return None
                    
                    date = date_tag["datetime"]

                    body = release_soup.find("div", class_="markdown-body my-3")
                    if not body:
                        self.logger.error("Release body not found in the release page.")
                        return None
                    
                    self.logger.info(f"Found version: '{release_name}', Release date: '{date}', Changelog URL: '{self.url + f'/tag/{release_name}'}'")

                    return {
                        "source": self.name,
                        "version": release_name,
                        "release_date": date,
                        "changes_raw": body.prettify(),
                        "link": self.url + f"/tag/{release_name}",
                    }
                
        except Exception as e:
            self.logger.error(f"Unexpect error fetching the changelog: {e}")
            return None