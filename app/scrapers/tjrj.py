from datetime import date
from typing import List
from bs4 import BeautifulSoup
import re
from app.scrapers.base import BaseScraper
from app.schemas.publication import PublicationCreate

class TJRJScraper(BaseScraper):
    """Scraper para Tribunal de Justiça do Rio de Janeiro"""
    
    BASE_URL = "http://www.tjrj.jus.br/web/guest/institucional/dir-gerais/dgcon/diario-oficial"
    
    def __init__(self):
        super().__init__("TJRJ")
    
    async def scrape_date(self, target_date: date) -> List[PublicationCreate]:
        """Scrape publicações de uma data específica do TJ-RJ"""
        
        # URL fictícia para exemplo
        url = f"{self.BASE_URL}?data={target_date.strftime('%Y-%m-%d')}"
        
        try:
            html = await self.fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            publications = []
            
            # Parsing específico do TJ-RJ (estrutura diferente do TJ-SP)
            for section in soup.find_all('div', class_='diario-section'):
                items = section.find_all('p', class_='publicacao')
                
                for item in items:
                    pub_data = {
                        'content': item.get_text(strip=True),
                        'process_number': self._extract_process_number(item.get_text()),
                        'parties': self._extract_parties(item.get_text()),
                        'publication_type': self._classify_type(section.find('h3').get_text())
                    }
                    
                    publication = self.parse_publication(pub_data)
                    publications.append(publication)
            
            return publications
            
        except Exception as e:
            print(f"Erro ao fazer scraping TJ-RJ {target_date}: {e}")
            return []
    
    def parse_publication(self, raw_data: dict) -> PublicationCreate:
        """Parse dados brutos em PublicationCreate"""
        return PublicationCreate(
            tribunal=self.tribunal_code,
            publication_date=date.today(),
            process_number=raw_data.get('process_number'),
            content=raw_data['content'],
            parties=raw_data.get('parties'),
            publication_type=raw_data.get('publication_type', 'OUTROS')
        )
    
    def _extract_process_number(self, text: str) -> str | None:
        """Extrai número do processo (padrão CNJ)"""
        pattern = r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}'
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def _extract_parties(self, text: str) -> list[str]:
        """Extrai partes envolvidas"""
        parties = []
        
        # Procura por padrões comuns
        patterns = [
            r'Requerente[:\s]+([A-ZÀ-Ú][A-Za-zÀ-ú\s]+)',
            r'Requerido[:\s]+([A-ZÀ-Ú][A-Za-zÀ-ú\s]+)',
            r'Autor[:\s]+([A-ZÀ-Ú][A-Za-zÀ-ú\s]+)',
            r'Réu[:\s]+([A-ZÀ-Ú][A-Za-zÀ-ú\s]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            parties.extend([m.strip() for m in matches])
        
        return list(set(parties))[:10]  # Limita a 10 partes únicas
    
    def _classify_type(self, section_title: str) -> str:
        """Classifica tipo de publicação baseado na seção"""
        section_lower = section_title.lower()
        
        if 'decisão' in section_lower or 'sentença' in section_lower:
            return 'DECISAO'
        elif 'despacho' in section_lower:
            return 'DESPACHO'
        elif 'edital' in section_lower:
            return 'EDITAL'
        elif 'intimação' in section_lower:
            return 'INTIMACAO'
        else:
            return 'OUTROS'