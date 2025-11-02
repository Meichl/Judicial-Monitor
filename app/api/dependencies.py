from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.cache_service import CacheService

# Cache service singleton
cache_service = CacheService()

async def get_cache_service() -> CacheService:
    """Dependency para obter cache service"""
    return cache_service

async def verify_api_key(api_key: str = None) -> bool:
    """Dependency para verificar API key (exemplo simplificado)"""
    # Em produção, validaria contra banco de dados
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key não fornecida"
        )
    
    # Validação fictícia
    valid_keys = ["dev-key-123", "prod-key-456"]
    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key inválida"
        )
    
    return True

