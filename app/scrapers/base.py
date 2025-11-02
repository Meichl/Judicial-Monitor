from abc import ABC, abstractmethod
from typing import List
import asyncio
import httpx
from datetime import date
from app.schemas.publication import PublicationCreate

class BaseScraper(ABC):
    """Classe base abstrata para scrapers de tribunais"""
    
    def __init__(self, tribunal_code: str):
        self.tribunal_code = tribunal_code
        self.timeout = httpx.Timeout(30.0)
        self.limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        
    async def fetch_page(self, url: str, retry: int = 3) -> str:
        """Busca página com retry automático"""
        async with httpx.AsyncClient(timeout=self.timeout, limits=self.limits) as client:
            for attempt in range(retry):
                try:
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.text
                except httpx.HTTPError as e:
                    if attempt == retry - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    @abstractmethod
    async def scrape_date(self, target_date: date) -> List[PublicationCreate]:
        """Método abstrato para scraping de uma data específica"""
        pass
    
    @abstractmethod
    def parse_publication(self, raw_data: dict) -> PublicationCreate:
        """Método abstrato para parsing de publicação"""
        pass