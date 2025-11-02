from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List
import logging
from app.database import get_db
from app.schemas.publication import PublicationResponse
from app.models.publication import Publication

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/publications", tags=["publications"])


@router.get("/", response_model=dict)
async def list_publications(
    tribunal: str | None = Query(
        None, 
        description="Código do tribunal (ex: TJSP, TJRJ)",
        example="TJSP"
    ),
    page: int = Query(
        1, 
        ge=1, 
        description="Número da página"
    ),
    page_size: int = Query(
        50, 
        ge=1, 
        le=100, 
        description="Itens por página"
    ),
    db: AsyncSession = Depends(get_db)
):
    """
    Lista publicações com filtros e paginação
    
    - **tribunal**: Filtrar por código do tribunal (TJSP, TJRJ, etc.)
    - **page**: Número da página (começa em 1)
    - **page_size**: Quantidade de itens por página (máximo 100)
    
    Retorna:
    - **items**: Lista de publicações
    - **total**: Total de registros encontrados
    - **page**: Página atual
    - **page_size**: Itens por página
    - **pages**: Total de páginas
    """
    
    try:
        query = select(Publication)
        conditions = []
        
        # Normalizar tribunal para uppercase se fornecido
        if tribunal:
            tribunal = tribunal.upper().strip()
            conditions.append(Publication.tribunal == tribunal)
            logger.info(f"Filtrando por tribunal: {tribunal}")
        
        # Aplicar condições
        if conditions:
            query = query.where(and_(*conditions))
        
        # Contar total de registros
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query) or 0
        
        # Se não houver registros, retornar resposta vazia
        if total == 0:
            logger.info(f"Nenhuma publicação encontrada. Filtros: tribunal={tribunal}")
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size,
                "pages": 0,
                "message": f"Nenhuma publicação encontrada" + (f" para o tribunal {tribunal}" if tribunal else "")
            }
        
        # Aplicar ordenação e paginação
        query = query.order_by(Publication.publication_date.desc(), Publication.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        # Executar query
        result = await db.execute(query)
        publications = result.scalars().all()
        
        # Calcular total de páginas
        total_pages = (total + page_size - 1) // page_size
        
        logger.info(f"Retornando {len(publications)} publicações de {total} totais")
        
        return {
            "items": [PublicationResponse.model_validate(pub) for pub in publications],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": total_pages
        }
        
    except Exception as e:
        logger.error(f"Erro ao buscar publicações: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro ao buscar publicações",
                "message": str(e),
                "tip": "Verifique se o banco de dados está acessível e se há dados cadastrados"
            }
        )


@router.get("/{publication_id}", response_model=PublicationResponse)
async def get_publication(
    publication_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtém detalhes de uma publicação específica
    
    - **publication_id**: UUID da publicação
    """
    from uuid import UUID
    
    try:
        # Validar UUID
        try:
            pub_uuid = UUID(publication_id)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": "ID inválido",
                    "message": f"O ID '{publication_id}' não é um UUID válido",
                    "example": "550e8400-e29b-41d4-a716-446655440000"
                }
            )
        
        # Buscar publicação
        query = select(Publication).where(Publication.id == pub_uuid)
        result = await db.execute(query)
        publication = result.scalar_one_or_none()
        
        if not publication:
            raise HTTPException(
                status_code=404, 
                detail={
                    "error": "Publicação não encontrada",
                    "message": f"Nenhuma publicação encontrada com o ID {publication_id}"
                }
            )
        
        logger.info(f"Publicação {publication_id} encontrada")
        return PublicationResponse.model_validate(publication)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar publicação {publication_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro ao buscar publicação",
                "message": str(e)
            }
        )


@router.get("/tribunals/list", response_model=dict)
async def list_tribunals(db: AsyncSession = Depends(get_db)):
    """
    Lista todos os tribunais disponíveis no sistema
    
    Retorna:
    - **tribunals**: Lista de códigos de tribunais
    - **count**: Quantidade de tribunais únicos
    """
    try:
        query = select(Publication.tribunal, func.count(Publication.id).label('total')).group_by(Publication.tribunal)
        result = await db.execute(query)
        tribunals = result.all()
        
        return {
            "tribunals": [
                {
                    "code": t.tribunal,
                    "publications_count": t.total
                }
                for t in tribunals
            ],
            "count": len(tribunals)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar tribunais: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro ao listar tribunais",
                "message": str(e)
            }
        )