"""
scripts/seed_data.py
Script para popular o banco com dados de exemplo
"""
import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from datetime import date, timedelta
from uuid import uuid4

# Agora os imports funcionarão
from app.database import AsyncSessionLocal
from app.models.publication import Publication


async def seed():
    """Popula banco com dados de exemplo"""
    
    print("🌱 Populando banco de dados...")
    
    async with AsyncSessionLocal() as db:
        publications = [
            Publication(
                id=uuid4(),
                tribunal="TJSP",
                publication_date=date.today() - timedelta(days=1),
                process_number="1234567-12.2024.8.26.0100",
                content="DECISÃO: Defiro a liminar requerida para determinar a suspensão imediata do protesto do título, sob pena de multa diária de R$ 500,00. Fundamento: verossimilhança das alegações e perigo de dano irreparável.",
                parties=["JOÃO SILVA", "BANCO XYZ S.A."],
                publication_type="DECISAO"
            ),
            Publication(
                id=uuid4(),
                tribunal="TJSP",
                publication_date=date.today(),
                process_number="7654321-98.2024.8.26.0200",
                content="SENTENÇA: Julgo procedente o pedido de indenização por danos morais no valor de R$ 10.000,00, com correção monetária e juros de mora desde a data do fato. Condeno a ré ao pagamento das custas processuais.",
                parties=["MARIA SANTOS", "EMPRESA ABC LTDA"],
                publication_type="SENTENCA"
            ),
            Publication(
                id=uuid4(),
                tribunal="TJRJ",
                publication_date=date.today(),
                process_number="9876543-21.2024.8.19.0001",
                content="INTIMAÇÃO: Fica a parte autora intimada para apresentar os documentos solicitados no prazo de 10 (dez) dias úteis, sob pena de preclusão do direito de produção desta prova.",
                parties=["PEDRO OLIVEIRA"],
                publication_type="INTIMACAO"
            ),
            Publication(
                id=uuid4(),
                tribunal="TJRJ",
                publication_date=date.today() - timedelta(days=2),
                process_number="5555555-55.2024.8.19.0002",
                content="DESPACHO: Vista à Defensoria Pública para manifestação no prazo legal. Após, retornem os autos conclusos para sentença.",
                parties=["JOSE FERREIRA", "ESTADO DO RIO DE JANEIRO"],
                publication_type="DESPACHO"
            ),
            Publication(
                id=uuid4(),
                tribunal="TJSP",
                publication_date=date.today() - timedelta(days=3),
                process_number="3333333-33.2024.8.26.0300",
                content="EDITAL: Fica intimado o réu EMPRESA DEF LTDA, atualmente em local incerto e não sabido, dos termos da ação de execução. Prazo: 15 dias para pagamento ou apresentação de bens à penhora.",
                parties=["ANA COSTA", "EMPRESA DEF LTDA"],
                publication_type="EDITAL"
            ),
            Publication(
                id=uuid4(),
                tribunal="TJSP",
                publication_date=date.today() - timedelta(days=1),
                process_number="8888888-88.2024.8.26.0400",
                content="ACÓRDÃO: A Turma, por votação unânime, deu provimento ao recurso para reformar a sentença e julgar improcedente o pedido inicial. Custas pelo autor.",
                parties=["CARLOS MENDES", "CONSTRUTORA XYZ LTDA"],
                publication_type="ACORDAO"
            ),
            Publication(
                id=uuid4(),
                tribunal="TJRJ",
                publication_date=date.today() - timedelta(days=4),
                process_number="7777777-77.2024.8.19.0003",
                content="CERTIDÃO: Certifico que decorreu o prazo sem manifestação da parte requerida. Nada mais.",
                parties=["FERNANDA LIMA"],
                publication_type="CERTIDAO"
            ),
        ]
        
        # Adiciona todas as publicações
        for pub in publications:
            db.add(pub)
        
        # Commit no banco
        await db.commit()
        
        print(f"✅ Criadas {len(publications)} publicações de exemplo")
        print("\n📊 Resumo:")
        print(f"   - TJ-SP: {sum(1 for p in publications if p.tribunal == 'TJSP')} publicações")
        print(f"   - TJ-RJ: {sum(1 for p in publications if p.tribunal == 'TJRJ')} publicações")
        print("\n🎉 Banco de dados populado com sucesso!")


if __name__ == "__main__":
    asyncio.run(seed())