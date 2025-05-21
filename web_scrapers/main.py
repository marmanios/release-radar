# main.py

import re
import concurrent.futures
from scrapers.python import PythonScraper
from scrapers.react import ReactScraper
from scrapers.nextjs import NextJsScraper
from scrapers.scraper import ScraperBaseClass
from scrapers.go import GoScraper
from ai_models.o4_mini_openai import O4MiniByOpenAI
from utils.helpful_types import ScraperOutput, RefinedOutput
from db import load_to_sql, check_if_patch_exists
from typing import Optional

def scrape_wrapper(scraper: ScraperBaseClass) -> Optional[ScraperOutput]:
    try:
        data = scraper.scrape()
        if data:
            return data
    except Exception as e:
        print(f"Error scraping {scraper.name}: {e}")
    return None


def main():
    # fetch data from all scrapers
    scrapers_data: list[ScraperOutput] = []
    scrapers = [
        PythonScraper(),
        ReactScraper(),
        NextJsScraper(),
        GoScraper(),
    ]

    # scraper
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(scrape_wrapper, scrapers))
        scrapers_data.extend([data for data in results if data])

    # use AI
    ai_model = O4MiniByOpenAI()
    refined_data: list[RefinedOutput] = []

    for raw_data in scrapers_data:

        # clean up version
        raw_data['version'] = re.sub(r'[^a-zA-Z0-9._\-]+', ' ', raw_data['version']).strip()

        # check if patch already exists
        if check_if_patch_exists(source=raw_data['source'], version=raw_data['version']):
            print(f"Patch {raw_data['version']} from {raw_data['source']} already exists in the database. Skipping...")
            continue

        # call AI model
        refined = ai_model.call_o4_api(raw_data['changes_raw'])
        refined_data.append({
            "source": raw_data['source'],
            "version": raw_data['version'],
            "release_date": raw_data['release_date'],
            "changes_markdown": refined,
            "link": raw_data['link'],
        }) 

    # load to DB
    load_to_sql(refined_data)

    # done 

print(__name__)
if (__name__ == "__main__"):
    main()