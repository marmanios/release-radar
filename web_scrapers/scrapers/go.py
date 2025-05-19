# scrapers/go.py

import re
import requests
from bs4 import BeautifulSoup
from logger import setup_logger
from utils.helpful_types import ScraperOutput

SOURCE_NAME = "go"
GO_ROOT_URL = "https://go.dev"
URL = f"{GO_ROOT_URL}/doc/devel/release"


# extracts version date from strings like "go1.24.0 (released 2025-02-11)"
def extract_release_date(s: str) -> str | None:
    match = re.search(r"\(released (\d{4}-\d{2}-\d{2})\)", s)
    if match:
        date = match.group(1)
        return date
    else:
        return None

def fetch_go() -> ScraperOutput | None:
    logger = setup_logger("go", "web_scrapers/logs/go.log" )
    logger.info("Fetching go changelog...")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Step 1: Find the latest release section (first h2 with version ID)
    latest_release_h2 = soup.find('h2', id=re.compile(r'^go\d+\.\d+\.\d+$'))

    if not latest_release_h2:
        logger.error("No release headers found in the document.")
        return None

    # Step 2: Traverse the siblings after the h2 to collect minor versions
    minor_version_p_elements = []
    for sibling in latest_release_h2.find_next_siblings():
        if sibling.name == 'h2':
            break  # stop at the next main release
        if sibling.name == 'p' and 'id' in sibling.attrs:
            version_match = re.match(r'go\d+\.\d+\.\d+', sibling['id'])
            if version_match:
                minor_version_p_elements.append(sibling)

    if False and minor_version_p_elements:
        latest_version_p = minor_version_p_elements[-1]
        latest_version = latest_version_p['id']
        latest_version_changelog_url = latest_version_p.find('a')['href']
        latest_version_release_date = extract_release_date("".join(latest_version_p.text.strip().splitlines()))

        # Extract changelog data from 'latest_version_changelog_url'
        changelog_page = requests.get(latest_version_changelog_url)
        changeLog_soup = BeautifulSoup(changelog_page.content, "html.parser")

        changelog_pr_titles = changeLog_soup.find_all("a", attrs={"data-testid":"issue-pr-title-link"})
        if not changelog_pr_titles:
            logger.error("Changelog content not found in the page.")
            return None
        
        logger.info(f"Latest version: {latest_version}, Release date: {latest_version_release_date}, Changelog URL: {latest_version_changelog_url}")
        
        return {
            "source": SOURCE_NAME,
            "version": latest_version,
            "release_date": latest_version_release_date,
            "changes_raw": "\n".join([changelog_pr_title.prettify() for changelog_pr_title in changelog_pr_titles]),
            "link": latest_version_changelog_url,
        }

        # TODO: EXTRACT RELEASE DATE FROM MAJOR VERSION AND ALSO GET CHANGELOG URL
        logger.info(f"Latest version: {latest_version}, Release date: {latest_version_release_date}, Changelog URL: {latest_version_changelog_url}")
    else:
        logger.info("No minor versions found under latest release.")
        latest_version = latest_release_h2['id']
        latest_version_changelog_path: str | None = latest_release_h2.find_next('p').find('a')['href'] if latest_release_h2.find_next('p') and  latest_release_h2.find_next('p').find('a') else None
        if not latest_version_changelog_path:
            logger.error("No changelog URL found for the latest version.")
            return None
        
        latest_version_changelog_url = f"{GO_ROOT_URL}{latest_version_changelog_path}" 
        if not latest_version_changelog_url:
            logger.error("Changelog URL is empty or malformed.")
            return None

        latest_version_release_date = extract_release_date(latest_release_h2.text.strip())
        if not latest_version_release_date:
            logger.error("Could not extract release date from the latest version header.")
    
        # Extract changelog data from 'latest_version_changelog_url'
        changelog_page = requests.get(latest_version_changelog_url)
        changeLog_soup = BeautifulSoup(changelog_page.content, "html.parser")

        changelog_page_html = changeLog_soup.find("article", class_="Doc Article")
        if not changelog_page_html:
            logger.error("Changelog content not found in the page.")
            return None
        
        logger.info(f"Latest version: {latest_version}, Release date: {latest_version_release_date}, Changelog URL: {latest_version_changelog_url}")
        
        return {
            "source": SOURCE_NAME,
            "version": latest_version,
            "release_date": latest_version_release_date,
            "changes_raw": changelog_page_html.prettify(),
            "link": latest_version_changelog_url,
        }





    
    # # Find parameters
    # return {
    #     "source": SOURCE_NAME,
    #     "version": newest_version.find("h2").text,
    #     "release_date":  newest_version.find("p").find("em").text[-10:],
    #     "changes_raw": newest_version.prettify(),
    #     "link": URL + newest_version.find("h2").find("a")["href"],
    # }

if __name__ == " __main__":
    fetch_go()