from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID, uuid4
from datetime import datetime
from app.database import get_db
from app.models.publication import Monitor
from pydantic import BaseModel

router = APIRouter(prefix="/monitors", tags=["monitoring"])

# Schemas
class MonitorCreate(BaseModel):
    user_id: UUID
    keywords: List[str]
    tribunals: List[str] | None = None
    active: bool = True

class MonitorResponse(BaseModel):
    id: UUID
    user_id: UUID
    keywords: List[str]
    tribunals: List[str] | None
    active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class MonitorUpdate(BaseModel):
    keywords: List[str] | None = None
    tribunals: List[str] | None = None
    active: bool | None = None

@router.post("/", response_model=MonitorResponse, status_code=201)
async def create_monitor(
    monitor: MonitorCreate,
    db: AsyncSession = Depends(get_db)
):
    """Cria novo monitoramento"""
    
    db_monitor = Monitor(
        id=uuid4(),
        user_id=monitor.user_id,
        keywords=monitor.keywords,
        tribunals=monitor.tribunals,
        active=monitor.active,
        created_at=datetime.utcnow()
    )
    
    db.add(db_monitor)
    await db.commit()
    await db.refresh(db_monitor)
    
    return MonitorResponse.model_validate(db_monitor)

@router.get("/", response_model=List[MonitorResponse])
async def list_monitors(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Lista monitoramentos de um usuário"""
    
    query = select(Monitor).where(Monitor.user_id == user_id)
    result = await db.execute(query)
    monitors = result.scalars().all()
    
    return [MonitorResponse.model_validate(m) for m in monitors]

@router.get("/{monitor_id}", response_model=MonitorResponse)
async def get_monitor(
    monitor_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Obtém detalhes de um monitoramento"""
    
    query = select(Monitor).where(Monitor.id == monitor_id)
    result = await db.execute(query)
    monitor = result.scalar_one_or_none()
    
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor não encontrado")
    
    return MonitorResponse.model_validate(monitor)

@router.patch("/{monitor_id}", response_model=MonitorResponse)
async def update_monitor(
    monitor_id: UUID,
    updates: MonitorUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Atualiza um monitoramento"""
    
    query = select(Monitor).where(Monitor.id == monitor_id)
    result = await db.execute(query)
    monitor = result.scalar_one_or_none()
    
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor não encontrado")
    
    # Atualiza campos
    if updates.keywords is not None:
        monitor.keywords = updates.keywords
    if updates.tribunals is not None:
        monitor.tribunals = updates.tribunals
    if updates.active is not None:
        monitor.active = updates.active
    
    await db.commit()
    await db.refresh(monitor)
    
    return MonitorResponse.model_validate(monitor)

@router.delete("/{monitor_id}", status_code=204)
async def delete_monitor(
    monitor_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Remove um monitoramento"""
    
    query = select(Monitor).where(Monitor.id == monitor_id)
    result = await db.execute(query)
    monitor = result.scalar_one_or_none()
    
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor não encontrado")
    
    await db.delete(monitor)
    await db.commit()
    
    return None