import json
from typing import Any, Optional
from redis import asyncio as aioredis
from app.config import get_settings

settings = get_settings()

class CacheService:
    """Service para gerenciamento de cache com Redis"""
    
    def __init__(self):
        self.redis = None
        self.default_ttl = settings.CACHE_TTL
    
    async def connect(self):
        """Conecta ao Redis"""
        if not self.redis:
            self.redis = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
    
    async def disconnect(self):
        """Desconecta do Redis"""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> Optional[Any]:
        """Busca valor no cache"""
        await self.connect()
        
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Erro ao buscar cache: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Define valor no cache"""
        await self.connect()
        
        try:
            ttl = ttl or self.default_ttl
            serialized = json.dumps(value, default=str)
            await self.redis.setex(key, ttl, serialized)
            return True
        except Exception as e:
            print(f"Erro ao definir cache: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Remove valor do cache"""
        await self.connect()
        
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            print(f"Erro ao deletar cache: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Remove múltiplas chaves por padrão"""
        await self.connect()
        
        try:
            keys = []
            async for key in self.redis.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                await self.redis.delete(*keys)
                return len(keys)
            return 0
        except Exception as e:
            print(f"Erro ao deletar por padrão: {e}")
            return 0
    
    def cache_key(self, *args) -> str:
        """Gera chave de cache a partir de argumentos"""
        return ":".join(str(arg) for arg in args)