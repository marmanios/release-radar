# scrapers/typescript.py

import re
import requests
from bs4 import BeautifulSoup
from utils.helpful_types import ScraperOutput
from scrapers.scraper import ScraperBaseClass
from typing import Optional
from html_to_markdown import convert_to_markdown

class TypescriptScraper(ScraperBaseClass):
    @property
    def name(self) -> str:
        return "typescript"
    
    @property
    def url(self) -> str:
        return "https://github.com/microsoft/TypeScript/releases"
    
    def scrape(self) -> Optional[ScraperOutput]:
        MAX_DEPTH = 5
        try:
            self.logger.info("Fetching typescript changelog...")

            for i in range(1, MAX_DEPTH + 1):
                self.logger.info(f"Fetching page {i} of the typescript changelog...")
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

                    # check if it's a major release
                    # for now im ignoring minor, rc, and beta releases
                    re_match = re.match(r"^typescript [0-9]*\.[0-9]*$", release_name)
                    if not re_match:
                        continue

                    # if here we found a stable release, let's extract its details
                    release_announcement_url = str(release.find("div", class_="markdown-body my-3").find("a")["href"])
                    release_date = release.find("relative-time")["datetime"]

                    if not release_announcement_url or not release_date:
                        self.logger.error("Release notes URL or release date not found in the release page. Release announcement url: {release_announcement_url}, release date: {release_date}")
                        return None

                    # fetch the release notes
                    release_page = requests.get(release_announcement_url)
                    release_page.raise_for_status() 

                    release_soup = BeautifulSoup(release_page.content, "html.parser")
                    changelog = release_soup.find("article")
                    if not changelog:
                        self.logger.error("Changelog not found in the release page.")
                        return None
                    
                    
                    self.logger.info(f"Found version: '{release_name}', Release date: '{release_date}', Changelog URL: '{release_announcement_url}'")

                    return {
                        "source": self.name,
                        "version": release_name,
                        "release_date": release_date,
                        "changes_raw": convert_to_markdown(changelog),
                        "link": release_announcement_url,
                    }
                
        except Exception as e:
            self.logger.error(f"Unexpect error fetching the changelog: {e}")
            return None