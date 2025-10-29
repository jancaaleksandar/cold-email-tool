import csv
import io

from db.database import get_db
from db.models import Lead
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()


class LeadCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    company: str | None = None
    title: str | None = None
    website: str | None = None
    linkedin_url: str | None = None
    email: str | None = None
    phone: str | None = None


class LeadResponse(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    company: str | None
    title: str | None
    website: str | None
    linkedin_url: str | None
    email: str | None
    phone: str | None
    enrichment_status: str
    enriched_data: dict | None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


@router.post("/", response_model=LeadResponse)
async def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a single lead"""
    db_lead = Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


@router.post("/bulk", response_model=list[LeadResponse])
async def create_leads_bulk(leads: list[LeadCreate], db: Session = Depends(get_db)):
    """Create multiple leads at once"""
    db_leads = [Lead(**lead.model_dump()) for lead in leads]
    db.add_all(db_leads)
    db.commit()
    for lead in db_leads:
        db.refresh(lead)
    return db_leads


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload leads from CSV file"""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    csv_file = io.StringIO(contents.decode("utf-8"))
    csv_reader = csv.DictReader(csv_file)

    leads = []
    for row in csv_reader:
        lead = Lead(
            first_name=row.get("first_name"),
            last_name=row.get("last_name"),
            company=row.get("company"),
            title=row.get("title"),
            website=row.get("website"),
            linkedin_url=row.get("linkedin_url"),
            email=row.get("email"),
            phone=row.get("phone"),
        )
        leads.append(lead)

    db.add_all(leads)
    db.commit()

    return {"message": f"Successfully uploaded {len(leads)} leads", "count": len(leads)}


@router.get("/", response_model=list[LeadResponse])
async def get_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all leads with pagination"""
    leads = db.query(Lead).offset(skip).limit(limit).all()
    return leads


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get a specific lead by ID"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(lead_id: int, lead_update: LeadCreate, db: Session = Depends(get_db)):
    """Update a lead"""
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    for key, value in lead_update.model_dump(exclude_unset=True).items():
        setattr(db_lead, key, value)

    db.commit()
    db.refresh(db_lead)
    return db_lead


@router.delete("/{lead_id}")
async def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    """Delete a lead"""
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    db.delete(db_lead)
    db.commit()
    return {"message": "Lead deleted successfully"}
