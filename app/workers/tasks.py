from celery import Celery
from datetime import date, timedelta
import asyncio
from app.config import get_settings
from app.scrapers.tjsp import TJSPScraper
from app.database import AsyncSessionLocal
from app.services.publication_service import PublicationService

settings = get_settings()

celery_app = Celery(
    "judicial_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery_app.task(name="scrape_tribunal")
def scrape_tribunal_task(tribunal_code: str, target_date: str = None):
    """Task assíncrona para scraping de tribunal"""
    
    if target_date:
        scrape_date = date.fromisoformat(target_date)
    else:
        scrape_date = date.today() - timedelta(days=1)
    
    # Run async scraping
    result = asyncio.run(run_scraping(tribunal_code, scrape_date))
    return result

async def run_scraping(tribunal_code: str, target_date: date):
    """Executa scraping e salva no banco"""
    
    # Seleciona scraper apropriado
    if tribunal_code == "TJSP":
        scraper = TJSPScraper()
    else:
        return {"error": f"Tribunal {tribunal_code} não suportado"}
    
    # Executa scraping
    publications = await scraper.scrape_date(target_date)
    
    # Salva no banco
    async with AsyncSessionLocal() as db:
        service = PublicationService(db)
        created = await service.bulk_create(publications)
    
    return {
        "tribunal": tribunal_code,
        "date": target_date.isoformat(),
        "scraped": len(publications),
        "created": created
    }

@celery_app.task(name="daily_scraping")
def daily_scraping_task():
    """Task diária para scraping de todos os tribunais"""
    tribunals = ["TJSP", "TJRJ"]
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    
    results = []
    for tribunal in tribunals:
        result = scrape_tribunal_task.delay(tribunal, yesterday)
        results.append(result.id)
    
    return {"scheduled_tasks": results}