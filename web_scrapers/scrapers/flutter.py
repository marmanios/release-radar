# scrapers/flutter.py

import re
import requests
from bs4 import BeautifulSoup
from utils.helpful_types import ScraperOutput
from scrapers.scraper import ScraperBaseClass
from typing import Optional
from datetime import datetime, timedelta
from html_to_markdown import convert_to_markdown

def parse_release_date(date_str: str) -> datetime:
    """
    Parses the release date from the announcement page.
    If the post was posted recently it can be of format 'X days ago' or 
    something like 'Feb 12, 2025'.
    """
    date_str = date_str.strip().lower()

    # Handle "X days ago"
    match = re.match(r"(\d+)\s+days?\s+ago", date_str)
    if match:
        days_ago = int(match.group(1))
        return datetime.now() - timedelta(days=days_ago)

    # Handle "Feb 12, 2025" format
    try:
        return datetime.strptime(date_str, "%b %d, %Y")
    except ValueError:
        raise ValueError(f"Unrecognized date format: {date_str}")
    
class FlutterScraper(ScraperBaseClass):
    @property
    def name(self) -> str:
        return "flutter"
    
    @property
    def url(self) -> str:
        return "https://docs.flutter.dev/release/release-notes"
    
    def scrape(self) -> Optional[ScraperOutput]:
        try:
            self.logger.info("Fetching Flutter changelog...")

            page = requests.get(self.url)
            page.raise_for_status() 
            soup = BeautifulSoup(page.content, "html.parser")

            article = soup.find("article")
            changelogs = article.find("ul")
            most_recent_changelog = changelogs.find("li")

            # extract the version 
            version = f"Flutter {most_recent_changelog.contents[0]}"

            # extract the urls for the announcement and release notes
            links = most_recent_changelog.find_all("a")
            announcement_blog_url = links[0]["href"]
            release_notes_url = links[1]["href"]

            # extract the release date from the announcement blog & its contents
            announcement_page = requests.get(announcement_blog_url)
            announcement_page.raise_for_status()
            announcement_soup = BeautifulSoup(announcement_page.content, "html.parser")
            release_date_text = announcement_soup.find("div", class_="ac af").contents[2].strip()
            release_date = parse_release_date(release_date_text)
            announcement_content = announcement_soup.find("article").find("div", class_="ci bh hw hx hy hz")

            # extract the content from the release notes page too
            release_notes_page = requests.get("https://docs.flutter.dev" + release_notes_url)
            release_notes_page.raise_for_status()
            release_notes_soup = BeautifulSoup(release_notes_page.content, "html.parser")
            release_notes_content = release_notes_soup.find("article")
            

            # combine the content from both pages
            combined_content = convert_to_markdown(announcement_content) + "\n" + convert_to_markdown(release_notes_content)

            # Find parameters
            return {
                "source": self.name,
                "version": version,
                "release_date":  release_date,
                "changes_raw": combined_content,
                # not sure if this is the best link to use or the release notes
                "link": announcement_blog_url,
            }
        
        except Exception as e:
            self.logger.error(f"Unexpect error fetching the changelog: {e}")
            return None
    