# main.py

from scrapers.python import fetch_python
from ai_models.o4_mini_openai import O4MiniByOpenAI
from utils.helpful_types import ScraperOutput, RefinedOutput

def main():
    # fetch data from all scrapers
    scrapers_data: list[ScraperOutput] = []
    py_data = fetch_python()
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
    

    # done 

print(__name__)
if (__name__ == "__main__"):
    main()