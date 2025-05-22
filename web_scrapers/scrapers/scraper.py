
from abc import ABC, abstractmethod
from typing import Optional
from utils.helpful_types import ScraperOutput
from logger import setup_logger
from utils.helpful_types import ScraperOutput
from utils.constants import log_folder_path
import os

class ScraperBaseClass(ABC):
    def __init__(self):
        """
        Initialize the ScraperBaseClass.
        """
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        log_file_path = os.path.join(parent_dir, log_folder_path, f"{self.name}.log")
        self.logger = setup_logger(self.name, log_file_path)


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