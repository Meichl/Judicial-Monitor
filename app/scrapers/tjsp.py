from datetime import date
from typing import List
from bs4 import BeautifulSoup
import re
from app.scrapers.base import BaseScraper
from app.schemas.publication import PublicationCreate

class TJSPScraper(BaseScraper):
    """Scraper para Tribunal de Justiça de São Paulo"""
    
    BASE_URL = "https://www.tjsp.jus.br/DiarioJusticaEletronico"
    
    def __init__(self):
        super().__init__("TJSP")
    
    async def scrape_date(self, target_date: date) -> List[PublicationCreate]:
        """Scrape publicações de uma data específica do TJ-SP"""
        
        # URL fictícia para exemplo (em produção seria a URL real)
        url = f"{self.BASE_URL}?data={target_date.strftime('%d/%m/%Y')}"
        
        try:
            html = await self.fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            publications = []
            
            # Parsing específico do TJ-SP
            for item in soup.find_all('div', class_='publicacao-item'):
                pub_data = {
                    'content': item.get_text(strip=True),
                    'process_number': self._extract_process_number(item.get_text()),
                    'parties': self._extract_parties(item.get_text()),
                }
                
                publication = self.parse_publication(pub_data)
                publications.append(publication)
            
            return publications
            
        except Exception as e:
            print(f"Erro ao fazer scraping TJ-SP {target_date}: {e}")
            return []
    
    def parse_publication(self, raw_data: dict) -> PublicationCreate:
        """Parse dados brutos em PublicationCreate"""
        return PublicationCreate(
            tribunal=self.tribunal_code,
            publication_date=date.today(),  # Seria extraído do HTML
            process_number=raw_data.get('process_number'),
            content=raw_data['content'],
            parties=raw_data.get('parties'),
            publication_type='DECISAO'  # Seria classificado
        )
    
    def _extract_process_number(self, text: str) -> str | None:
        """Extrai número do processo usando regex"""
        pattern = r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}'
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def _extract_parties(self, text: str) -> list[str]:
        """Extrai partes do processo"""
        # Lógica simplificada
        parties = []
        if "Autor:" in text:
            parties.append(text.split("Autor:")[1].split("Réu:")[0].strip())
        if "Réu:" in text:
            parties.append(text.split("Réu:")[1].split("\n")[0].strip())
        return parties