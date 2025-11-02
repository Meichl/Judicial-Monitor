.PHONY: help setup up down logs test lint clean seed

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Executa setup inicial do projeto
	@chmod +x scripts/setup.sh
	@./scripts/setup.sh

up: ## Inicia todos os containers
	docker-compose up -d
	@echo "✅ Containers iniciados!"
	@echo "📖 Documentação: http://localhost:8000/docs"

down: ## Para todos os containers
	docker-compose down

logs: ## Mostra logs dos containers
	docker-compose logs -f

test: ## Executa todos os testes
	docker-compose exec app pytest -v --cov=app

test-watch: ## Executa testes em modo watch
	docker-compose exec app pytest-watch

lint: ## Executa linters
	docker-compose exec app ruff check app/
	docker-compose exec app black --check app/

format: ## Formata o código
	docker-compose exec app black app/
	docker-compose exec app ruff check --fix app/

migrate: ## Executa migrações pendentes
	docker-compose exec app alembic upgrade head

migrate-create: ## Cria nova migração
	@read -p "Nome da migração: " name; \
	docker-compose exec app alembic revision --autogenerate -m "$$name"

seed: ## Popula banco com dados de exemplo
	docker-compose exec app python scripts/seed_data.py

shell: ## Acessa shell do container da aplicação
	docker-compose exec app bash

db-shell: ## Acessa shell do PostgreSQL
	docker-compose exec db psql -U judicial_user -d judicial_db

scrape-test: ## Testa scrapers manualmente
	docker-compose exec app python scripts/test_scraper.py

clean: ## Remove containers, volumes e cache
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage

build: ## Rebuild das imagens Docker
	docker-compose build --no-cache

restart: down up ## Reinicia todos os containers