from sqlalchemy import String, Text, Date, ARRAY, Index
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
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
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    __table_args__ = (
        Index('idx_pub_tribunal_date', 'tribunal', 'publication_date'),
        Index('idx_pub_process', 'process_number'),
    )


class Monitor(Base):
    __tablename__ = "monitors"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    tribunals: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
