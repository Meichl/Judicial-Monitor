from pydantic import BaseModel, Field, ConfigDict
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
