# main.py

from scrapers.python import fetch_python
from ai_models.o4_mini_openai import O4MiniByOpenAI
from utils.helpful_types import ScraperOutput, RefinedOutput
from db import load_to_sql

dummy_refined_data = [
    {
        "source": "Python",
        "version": "3.12.0",
        "release_date": "2023-10-02",
        "changes_markdown": "### Python 3.12.0 Release Notes\n\n- **New Features**:\n  - Added new syntax for pattern matching.\n  - Improved performance of the garbage collector.\n\n- **Bug Fixes**:\n  - Fixed an issue with the `asyncio` module.\n\n- **Deprecations**:\n  - Deprecated the `distutils` module.",
        "link": "https://www.python.org/downloads/release/python-3120/"
    }
]

def main():
    # fetch data from all scrapers
    scrapers_data: list[ScraperOutput] = []
    py_data = fetch_python()

    if py_data:
        scrapers_data.append(py_data)

    # use AI
    ai_model = O4MiniByOpenAI()
    refined_data: list[RefinedOutput] = []

    for raw_data in scrapers_data:
        # call AI model
        refined = ai_model.call_o4_api(raw_data['changes_html'])
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