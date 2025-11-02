#!/usr/bin/env python3
"""
Script para criar automaticamente toda a estrutura do projeto Judicial Monitor
Execute: python setup_project.py
"""

import os
from pathlib import Path

def create_file(path: str, content: str):
    """Cria arquivo com conteúdo"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Criado: {path}")

def create_empty_file(path: str):
    """Cria arquivo vazio"""
    create_file(path, "")

# ============================================
# ESTRUTURA DE PASTAS
# ============================================
def create_structure():
    """Cria estrutura de diretórios"""
    folders = [
        "app/models",
        "app/schemas", 
        "app/api/routes",
        "app/scrapers",
        "app/services",
        "app/workers",
        "tests",
        "alembic/versions",
        "scripts"
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    # Criar __init__.py em todas as pastas Python
    init_files = [
        "app/__init__.py",
        "app/models/__init__.py",
        "app/schemas/__init__.py",
        "app/api/__init__.py",
        "app/api/routes/__init__.py",
        "app/scrapers/__init__.py",
        "app/services/__init__.py",
        "app/workers/__init__.py",
        "tests/__init__.py",
    ]
    
    for init_file in init_files:
        create_empty_file(init_file)
    
    print("✅ Estrutura de pastas criada")

# ============================================
# CONTEÚDO DOS ARQUIVOS
# ============================================

REQUIREMENTS = """# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Data Validation
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy[asyncio]==2.0.23
asyncpg==0.29.0
alembic==1.12.1

# Cache & Queue
redis==5.0.1
celery==5.3.4

# HTTP & Scraping
httpx==0.25.2
beautifulsoup4==4.12.2
lxml==4.9.3

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Utilities
python-dotenv==1.0.0
"""

DOCKER_COMPOSE = """version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: judicial_user
      POSTGRES_PASSWORD: judicial_pass
      POSTGRES_DB: judicial_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U judicial_user"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  app:
    build:
      context: .
      dockerfile: Dockerfile
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://judicial_user:judicial_pass@db/judicial_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  postgres_data:
"""

DOCKERFILE = """FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

ENV_FILE = """DATABASE_URL=postgresql+asyncpg://judicial_user:judicial_pass@db/judicial_db
REDIS_URL=redis://redis:6379/0
API_V1_PREFIX=/api/v1
PROJECT_NAME=Judicial Monitor API
SCRAPER_CONCURRENCY=5
SCRAPER_TIMEOUT=30
CACHE_TTL=300
"""

GITIGNORE = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
*.egg-info/
.venv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp

# Environment
.env
.env.local

# Database
*.db
*.sqlite

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log

# Docker
docker-compose.override.yml

# OS
.DS_Store
"""

CONFIG_PY = """from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/judicial_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Judicial Monitor API"
    SCRAPER_CONCURRENCY: int = 5
    SCRAPER_TIMEOUT: int = 30
    CACHE_TTL: int = 300
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
"""

DATABASE_PY = """from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
"""

MAIN_PY = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api.routes import publications

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(publications.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "service": "Judicial Monitor API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

MODELS_PUBLICATION = """from sqlalchemy import String, Text, Date, ARRAY, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime
import uuid
from app.database import Base

class Publication(Base):
    __tablename__ = "publications"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tribunal: Mapped[str] = mapped_column(String(10), nullable=False)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    process_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    parties: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    publication_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    scraped_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_pub_tribunal_date', 'tribunal', 'publication_date'),
        Index('idx_pub_process', 'process_number'),
    )
"""

SCHEMAS_PUBLICATION = """from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from uuid import UUID

class PublicationBase(BaseModel):
    tribunal: str = Field(..., max_length=10)
    publication_date: date
    process_number: str | None = None
    content: str
    parties: list[str] | None = None
    publication_type: str | None = None

class PublicationCreate(PublicationBase):
    pass

class PublicationResponse(PublicationBase):
    id: UUID
    scraped_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PublicationFilter(BaseModel):
    tribunal: str | None = None
    date_from: date | None = None
    date_to: date | None = None
    process_number: str | None = None
    search_query: str | None = None
    page: int = Field(1, ge=1)
    page_size: int = Field(50, ge=1, le=100)
"""

ROUTES_PUBLICATIONS = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List
from app.database import get_db
from app.schemas.publication import PublicationResponse, PublicationFilter
from app.models.publication import Publication

router = APIRouter(prefix="/publications", tags=["publications"])

@router.get("/", response_model=dict)
async def list_publications(
    tribunal: str | None = None,
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = Depends(get_db)
):
    \"\"\"Lista publicações com filtros e paginação\"\"\"
    
    query = select(Publication)
    conditions = []
    
    if tribunal:
        conditions.append(Publication.tribunal == tribunal)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0
    
    # Apply pagination
    query = query.order_by(Publication.publication_date.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    publications = result.scalars().all()
    
    return {
        "items": [PublicationResponse.model_validate(pub) for pub in publications],
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size
    }

@router.get("/{publication_id}", response_model=PublicationResponse)
async def get_publication(
    publication_id: str,
    db: AsyncSession = Depends(get_db)
):
    \"\"\"Obtém detalhes de uma publicação\"\"\"
    from uuid import UUID
    
    try:
        pub_uuid = UUID(publication_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    query = select(Publication).where(Publication.id == pub_uuid)
    result = await db.execute(query)
    publication = result.scalar_one_or_none()
    
    if not publication:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")
    
    return PublicationResponse.model_validate(publication)
"""

ALEMBIC_INI = """[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql+asyncpg://judicial_user:judicial_pass@db/judicial_db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""

ALEMBIC_ENV = """import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.database import Base
from app.models.publication import Publication
from app.config import get_settings

config = context.config
settings = get_settings()

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

README = """# Judicial Monitor API

Sistema de monitoramento de publicações em Diários Oficiais de Tribunais.

## Quick Start

```bash
# 1. Criar estrutura
python setup_project.py

# 2. Iniciar containers
docker-compose up -d

# 3. Executar migrações
docker-compose exec app alembic upgrade head

# 4. Acessar API
open http://localhost:8000/docs
```

## Comandos Úteis

```bash
# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Executar testes
docker-compose exec app pytest

# Acessar shell
docker-compose exec app bash
```

## Endpoints

- GET /docs - Documentação Swagger
- GET /health - Health check
- GET /api/v1/publications/ - Listar publicações
- GET /api/v1/publications/{id} - Detalhes de publicação

## Tecnologias

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Pytest
"""

def main():
    """Função principal"""
    print("🚀 Criando projeto Judicial Monitor...\n")
    
    # Criar estrutura de pastas
    create_structure()
    
    # Criar arquivos de configuração
    print("\n📝 Criando arquivos de configuração...")
    create_file("requirements.txt", REQUIREMENTS)
    create_file("docker-compose.yml", DOCKER_COMPOSE)
    create_file("Dockerfile", DOCKERFILE)
    create_file(".env", ENV_FILE)
    create_file(".gitignore", GITIGNORE)
    create_file("alembic.ini", ALEMBIC_INI)
    create_file("README.md", README)
    
    # Criar arquivos Python
    print("\n🐍 Criando arquivos Python...")
    create_file("app/config.py", CONFIG_PY)
    create_file("app/database.py", DATABASE_PY)
    create_file("app/main.py", MAIN_PY)
    create_file("app/models/publication.py", MODELS_PUBLICATION)
    create_file("app/schemas/publication.py", SCHEMAS_PUBLICATION)
    create_file("app/api/routes/publications.py", ROUTES_PUBLICATIONS)
    create_file("alembic/env.py", ALEMBIC_ENV)
    
    print("\n" + "="*60)
    print("✨ Projeto criado com sucesso!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("\n1. Iniciar containers:")
    print("   docker-compose up -d")
    print("\n2. Executar migrações:")
    print("   docker-compose exec app alembic upgrade head")
    print("\n3. Acessar a API:")
    print("   http://localhost:8000/docs")
    print("\n4. Ver logs:")
    print("   docker-compose logs -f")
    print()

if __name__ == "__main__":
    main()