# Judicial Monitor API

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
