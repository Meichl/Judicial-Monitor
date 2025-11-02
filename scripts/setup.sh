#!/bin/bash

# Script de setup automatizado para o projeto

set -e  # Para na primeira falha

echo "🚀 Iniciando setup do Judicial Monitor..."

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verifica se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker não está instalado${NC}"
    echo "Por favor, instale o Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verifica se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose não está instalado${NC}"
    echo "Por favor, instale o Docker Compose"
    exit 1
fi

echo -e "${GREEN}✅ Docker detectado${NC}"

# Cria arquivo .env se não existir
if [ ! -f .env ]; then
    echo -e "${BLUE}📝 Criando arquivo .env...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ Arquivo .env criado${NC}"
else
    echo -e "${GREEN}✅ Arquivo .env já existe${NC}"
fi

# Para containers existentes
echo -e "${BLUE}🛑 Parando containers existentes...${NC}"
docker-compose down 2>/dev/null || true

# Remove volumes antigos (opcional)
read -p "Deseja remover volumes antigos? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${BLUE}🗑️  Removendo volumes...${NC}"
    docker-compose down -v
fi

# Build das imagens
echo -e "${BLUE}🏗️  Construindo imagens Docker...${NC}"
docker-compose build

# Inicia os containers
echo -e "${BLUE}🐳 Iniciando containers...${NC}"
docker-compose up -d

# Aguarda banco de dados estar pronto
echo -e "${BLUE}⏳ Aguardando banco de dados...${NC}"
sleep 5

# Executa migrações
echo -e "${BLUE}📊 Executando migrações do banco...${NC}"
docker-compose exec -T app alembic upgrade head

# Popula dados de exemplo
read -p "Deseja popular com dados de exemplo? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${BLUE}🌱 Populando banco de dados...${NC}"
    docker-compose exec -T app python scripts/seed_data.py
fi

# Verifica saúde da API
echo -e "${BLUE}🏥 Verificando saúde da API...${NC}"
sleep 3

if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ API está saudável!${NC}"
else
    echo -e "${RED}❌ API não está respondendo corretamente${NC}"
    echo "Verifique os logs com: docker-compose logs app"
fi

# Resumo final
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✨ Setup concluído com sucesso!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. Acesse a documentação da API:"
echo -e "   ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo "2. Verifique os logs:"
echo -e "   ${BLUE}docker-compose logs -f${NC}"
echo ""
echo "3. Execute os testes:"
echo -e "   ${BLUE}docker-compose exec app pytest${NC}"
echo ""
echo "4. Teste um scraper:"
echo -e "   ${BLUE}docker-compose exec app python scripts/test_scraper.py${NC}"
echo ""
echo "5. Para parar os serviços:"
echo -e "   ${BLUE}docker-compose down${NC}"
echo ""
