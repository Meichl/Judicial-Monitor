import pytest
from datetime import date
from uuid import uuid4
from app.services.publication_service import PublicationService
from app.schemas.publication import PublicationCreate, PublicationFilter

@pytest.mark.asyncio
async def test_create_publication(db_session):
    """Test publication creation"""
    service = PublicationService(db_session)
    
    pub_data = PublicationCreate(
        tribunal="TJSP",
        publication_date=date.today(),
        process_number="1234567-12.2024.8.26.0100",
        content="Teste de publicação",
        parties=["João Silva", "Maria Santos"],
        publication_type="DECISAO"
    )
    
    publication = await service.create_publication(pub_data)
    assert publication.id is not None
    assert publication.tribunal == "TJSP"

@pytest.mark.asyncio
async def test_check_duplicate(db_session):
    """Test duplicate detection"""
    service = PublicationService(db_session)
    
    pub_data = PublicationCreate(
        tribunal="TJSP",
        publication_date=date.today(),
        process_number="1234567-12.2024.8.26.0100",
        content="Teste",
        parties=["João"],
        publication_type="DECISAO"
    )
    
    # Create first
    await service.create_publication(pub_data)
    
    # Check duplicate
    duplicate = await service._check_duplicate(pub_data)
    assert duplicate is not None

@pytest.mark.asyncio
async def test_get_publications_with_filters(db_session):
    """Test publication retrieval with filters"""
    service = PublicationService(db_session)
    
    filters = PublicationFilter(
        tribunal="TJSP",
        page=1,
        page_size=10
    )
    
    publications, total = await service.get_publications(filters)
    assert isinstance(publications, list)
    assert isinstance(total, int)