import pytest
from datetime import date
from app.scrapers.tjsp import TJSPScraper

@pytest.mark.asyncio
async def test_tjsp_scraper_initialization():
    """Test TJSP scraper initialization"""
    scraper = TJSPScraper()
    assert scraper.tribunal_code == "TJSP"
    assert scraper.BASE_URL is not None

@pytest.mark.asyncio
async def test_extract_process_number():
    """Test process number extraction"""
    scraper = TJSPScraper()
    text = "Processo nº 1234567-12.2024.8.26.0100 - Autor: João Silva"
    process_num = scraper._extract_process_number(text)
    assert process_num == "1234567-12.2024.8.26.0100"

@pytest.mark.asyncio
async def test_extract_parties():
    """Test parties extraction"""
    scraper = TJSPScraper()
    text = "Autor: João Silva\nRéu: Maria Santos\nAdvogado: Dr. Pedro"
    parties = scraper._extract_parties(text)
    assert len(parties) == 2
    assert "João Silva" in parties[0]
    assert "Maria Santos" in parties[1]
