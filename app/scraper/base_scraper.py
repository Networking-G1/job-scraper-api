# ============= app/scraper/base_scraper.py =============
from abc import ABC, abstractmethod
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def scrape_jobs(self, keywords: List[str], location: str = "") -> List[Dict]:
        """Método abstracto para implementar el scraping específico"""
        pass
    
    def get_page(self, url: str, retries: int = 3) -> BeautifulSoup:
        """Obtiene y parsea una página con reintentos"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                logger.error(f"Error fetching {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
    
    def clean_text(self, text: str) -> str:
        """Limpia y normaliza texto"""
        if not text:
            return ""
        return " ".join(text.strip().split())