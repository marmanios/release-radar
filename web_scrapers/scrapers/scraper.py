from abc import ABC, abstractmethod
from typing import Optional
from utils.helpful_types import ScraperOutput
from logger import setup_logger
from utils.helpful_types import ScraperOutput
from utils.constants import log_folder_path

class ScraperBaseClass(ABC):
    def __init__(self):
        """
        Initialize the ScraperBaseClass.
        """
        self.logger = setup_logger(self.name, f"{log_folder_path}/{self.name}.log")


    """
    Abstract base class for web scrapers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the language or framework.

        :return: The name of the language or framework.
        """
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        """
        Get the URL to scrape.

        :return: The URL to scrape.
        """
        pass
     

    @abstractmethod
    def scrape(self) -> Optional[ScraperOutput]:
        """
        Scrape the given URL and return the data as a dictionary.

        :param url: The URL to scrape.
        :

        :return: A string of the scraped data. Either MD or HTML.
        """
        pass