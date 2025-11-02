Write-Host "🔧 Configurando Alembic...`n" -ForegroundColor Cyan

# 1. Criar template se não existir
$templateContent = @'
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
'@

Write-Host "1️⃣ Criando template..." -ForegroundColor Yellow
Set-Content -Path "alembic/script.py.mako" -Value $templateContent -Encoding UTF8
Write-Host "   ✅ Template criado`n" -ForegroundColor Green

# 2. Criar migration inicial retroativa
$migrationContent = @'
"""initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2024-11-01 10:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tabela já existe, migration vazia
    pass


def downgrade() -> None:
    # Não desfazer nada
    pass
'@

Write-Host "2️⃣ Criando migration inicial..." -ForegroundColor Yellow
Set-Content -Path "alembic/versions/001_initial.py" -Value $migrationContent -Encoding UTF8
Write-Host "   ✅ Migration criada`n" -ForegroundColor Green

# 3. Marcar como aplicada
Write-Host "3️⃣ Sincronizando Alembic com banco..." -ForegroundColor Yellow
docker-compose exec app alembic stamp 001_initial
Write-Host "   ✅ Sincronizado`n" -ForegroundColor Green

# 4. Verificar
Write-Host "4️⃣ Verificando status..." -ForegroundColor Yellow
docker-compose exec app alembic current

Write-Host "`n✨ Alembic configurado com sucesso!" -ForegroundColor Green
Write-Host "📋 Próximas mudanças no schema:" -ForegroundColor Cyan
Write-Host "   1. Altere os models em app/models/" -ForegroundColor White
Write-Host "   2. Execute: docker-compose exec app alembic revision --autogenerate -m 'descrição'" -ForegroundColor White
Write-Host "   3. Execute: docker-compose exec app alembic upgrade head`n" -ForegroundColor White