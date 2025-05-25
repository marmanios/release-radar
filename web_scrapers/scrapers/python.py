# scrapers/python.py

import requests
from bs4 import BeautifulSoup
from utils.helpful_types import ScraperOutput
from scrapers.scraper import ScraperBaseClass
from typing import Optional
from html_to_markdown import convert_to_markdown

class PythonScraper(ScraperBaseClass):
    @property
    def name(self) -> str:
        return "python"
    
    @property
    def url(self) -> str:
        return "https://docs.python.org/3/whatsnew/changelog.html"
    
    def scrape(self) -> Optional[ScraperOutput]:
        try:
            self.logger.info("Fetching Python changelog...")

            page = requests.get(self.url)
            page.raise_for_status() 
            soup = BeautifulSoup(page.content, "html.parser")

            changelog = soup.find("section", id="changelog")
            # Get the latest version by finding the section after 'python-next'
            python_next_section = changelog.find("section", id="python-next")
            newest_version = python_next_section.find_next_sibling("section")

            self.logger.info(f"Found version: '{newest_version.find("h2").text}', Release date: '{newest_version.find("p").find("em").text[-10:]}', Changelog URL: '{self.url + newest_version.find("h2").find("a")["href"]}'")


            # Find parameters
            return {
                "source": self.name,
                "version": newest_version.find("h2").text,
                "release_date":  newest_version.find("p").find("em").text[-10:],
                "changes_raw": convert_to_markdown(newest_version),
                "link": self.url + newest_version.find("h2").find("a")["href"],
            }
        
        except Exception as e:
            self.logger.error(f"Unexpect error fetching the changelog: {e}")
            return None
    