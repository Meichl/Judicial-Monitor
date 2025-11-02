from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import date, timedelta
from app.database import get_db
from app.models.publication import Publication

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/tribunals")
async def get_tribunal_metrics(
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """Obtém métricas por tribunal nos últimos N dias"""
    
    since_date = date.today() - timedelta(days=days)
    
    query = select(
        Publication.tribunal,
        func.count(Publication.id).label('total'),
        func.count(func.distinct(Publication.publication_date)).label('days_active')
    ).where(
        Publication.publication_date >= since_date
    ).group_by(Publication.tribunal)
    
    result = await db.execute(query)
    metrics = result.all()
    
    return {
        "period_days": days,
        "tribunals": [
            {
                "tribunal": m.tribunal,
                "total_publications": m.total,
                "days_active": m.days_active,
                "avg_per_day": round(m.total / days, 2)
            }
            for m in metrics
        ]
    }

@router.get("/scraping-status")
async def get_scraping_status(db: AsyncSession = Depends(get_db)):
    """Status dos scrapers (última execução)"""
    
    # Última publicação por tribunal
    query = select(
        Publication.tribunal,
        func.max(Publication.scraped_at).label('last_scrape'),
        func.count(Publication.id).label('total_today')
    ).where(
        Publication.publication_date == date.today()
    ).group_by(Publication.tribunal)
    
    result = await db.execute(query)
    status = result.all()
    
    return {
        "tribunals": [
            {
                "tribunal": s.tribunal,
                "last_scrape": s.last_scrape.isoformat() if s.last_scrape else None,
                "publications_today": s.total_today,
                "status": "active" if s.last_scrape else "inactive"
            }
            for s in status
        ]
    }