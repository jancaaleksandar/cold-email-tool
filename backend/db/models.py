from datetime import datetime
import enum

from sqlalchemy import JSON, Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class EnrichmentStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    company = Column(String, nullable=True)
    title = Column(String, nullable=True)
    website = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    # Enrichment data
    enrichment_status = Column(SQLEnum(EnrichmentStatus), default=EnrichmentStatus.PENDING)
    enriched_data = Column(JSON, nullable=True)  # Store all enriched info

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    enrichment_tasks = relationship("EnrichmentTask", back_populates="lead")


class EnrichmentTask(Base):
    __tablename__ = "enrichment_tasks"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    task_type = Column(String)  # e.g., "email_validation", "apollo_enrichment", "ai_enrichment"
    status = Column(SQLEnum(EnrichmentStatus), default=EnrichmentStatus.PENDING)
    result = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    celery_task_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    lead = relationship("Lead", back_populates="enrichment_tasks")
