## Pré-requisitos

- Docker e Docker Compose instalados
- Git
- Python 3.11+ (para desenvolvimento local)

## Setup Inicial

### 1. Clone o repositório
```bash
git clone <repository-url>
cd judicial-monitor
```

### 2. Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite .env se necessário
```

### 3. Inicie os serviços
```bash
docker-compose up -d
```

### 4. Execute as migrações
```bash
docker-compose exec app alembic upgrade head
```

### 5. Verifique a instalação
```bash
curl http://localhost:8000/health
# Resposta esperada: {"status":"healthy"}
```

### 6. Acesse a documentação da API
Abra no navegador: http://localhost:8000/docs

## Comandos Úteis

### Executar scraping manual
```bash
docker-compose exec app python -c "
from app.workers.tasks import scrape_tribunal_task
result = scrape_tribunal_task.delay('TJSP')
print(f'Task ID: {result.id}')
"
```

### Ver logs
```bash
# API
docker-compose logs -f app

# Celery Worker
docker-compose logs -f celery_worker

# Todos
docker-compose logs -f
```

### Executar testes
```bash
docker-compose exec app pytest -v
```

### Acessar banco de dados
```bash
docker-compose exec db psql -U judicial_user -d judicial_db
```

### Parar serviços
```bash
docker-compose down
```

### Limpar volumes (CUIDADO: apaga dados)
```bash
docker-compose down -v
```

## Desenvolvimento Local

### Setup ambiente Python
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Executar API localmente
```bash
# Certifique-se que PostgreSQL e Redis estão rodando
uvicorn app.main:app --reload
```

### Criar nova migração
```bash
alembic revision --autogenerate -m "descrição da migração"
alembic upgrade head
```

## Testando os Endpoints

### Listar publicações
```bash
curl "http://localhost:8000/api/v1/publications/?page=1&page_size=10"
```

### Buscar por tribunal
```bash
curl "http://localhost:8000/api/v1/publications/?tribunal=TJSP"
```

### Criar monitoramento
```bash
curl -X POST "http://localhost:8000/api/v1/monitors/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "keywords": ["execução", "sentença"],
    "tribunals": ["TJSP", "TJRJ"]
  }'
```

### Ver métricas
```bash
curl "http://localhost:8000/api/v1/metrics/tribunals"
```

## Troubleshooting

### Erro de conexão com banco
- Verifique se o container do PostgreSQL está rodando: `docker-compose ps`
- Verifique os logs: `docker-compose logs db`

### Testes falhando
- Certifique-se que o banco de testes está limpo
- Execute: `docker-compose exec app pytest --create-db`

### Scraper não funciona
- Verifique se o Celery worker está ativo
- Veja logs: `docker-compose logs celery_worker`

## Próximos Passos

1. Explore a documentação interativa em `/docs`
2. Adicione novos scrapers em `app/scrapers/`
3. Customize os modelos em `app/models/`
4. Configure notificações no Celery Beat

## Suporte

Para dúvidas ou problemas, abra uma issue no repositório.