import pytest
from httpx import AsyncClient
from app.main import app
from datetime import date

@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "service" in response.json()

@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_list_publications():
    """Test publications listing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/publications/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data

@pytest.mark.asyncio
async def test_list_publications_with_filters():
    """Test publications listing with filters"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        params = {
            "tribunal": "TJSP",
            "page": 1,
            "page_size": 10
        }
        response = await client.get("/api/v1/publications/", params=params)
        assert response.status_code == 200
