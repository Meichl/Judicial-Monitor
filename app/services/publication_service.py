from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date
from app.models.publication import Publication
from app.schemas.publication import PublicationCreate, PublicationFilter

class PublicationService:
    """Service layer para operações de publicações"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_publication(self, pub: PublicationCreate) -> Publication:
        """Cria nova publicação"""
        db_pub = Publication(**pub.model_dump())
        self.db.add(db_pub)
        await self.db.commit()
        await self.db.refresh(db_pub)
        return db_pub
    
    async def bulk_create(self, publications: List[PublicationCreate]) -> int:
        """Criação em lote com deduplicação"""
        created = 0
        for pub in publications:
            # Check se já existe
            existing = await self._check_duplicate(pub)
            if not existing:
                await self.create_publication(pub)
                created += 1
        return created
    
    async def _check_duplicate(self, pub: PublicationCreate) -> Publication | None:
        """Verifica se publicação já existe"""
        query = select(Publication).where(
            and_(
                Publication.tribunal == pub.tribunal,
                Publication.publication_date == pub.publication_date,
                Publication.process_number == pub.process_number
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_publications(self, filters: PublicationFilter) -> tuple[List[Publication], int]:
        """Busca publicações com filtros e paginação"""
        
        # Build query
        query = select(Publication)
        conditions = []
        
        if filters.tribunal:
            conditions.append(Publication.tribunal == filters.tribunal)
        
        if filters.date_from:
            conditions.append(Publication.publication_date >= filters.date_from)
        
        if filters.date_to:
            conditions.append(Publication.publication_date <= filters.date_to)
        
        if filters.process_number:
            conditions.append(Publication.process_number.ilike(f"%{filters.process_number}%"))
        
        if filters.search_query:
            conditions.append(Publication.content.ilike(f"%{filters.search_query}%"))
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)
        
        # Apply pagination
        query = query.order_by(Publication.publication_date.desc())
        query = query.offset((filters.page - 1) * filters.page_size)
        query = query.limit(filters.page_size)
        
        result = await self.db.execute(query)
        publications = result.scalars().all()
        
        return list(publications), total or 0