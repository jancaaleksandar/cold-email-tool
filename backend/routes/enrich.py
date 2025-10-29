from db.database import get_db
from db.models import EnrichmentStatus, EnrichmentTask, Lead
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from workers.tasks import enrich_lead_task

router = APIRouter()


class EnrichmentRequest(BaseModel):
    lead_ids: list[int]
    enrichment_types: list[str]  # e.g., ["email", "apollo", "ai"]


class EnrichmentResponse(BaseModel):
    message: str
    task_ids: list[str]
    lead_count: int


@router.post("/", response_model=EnrichmentResponse)
async def enrich_leads(request: EnrichmentRequest, db: Session = Depends(get_db)):
    """
    Trigger enrichment for multiple leads
    Enrichment types: email, apollo, ai, scraper
    """
    # Validate leads exist
    leads = db.query(Lead).filter(Lead.id.in_(request.lead_ids)).all()
    if len(leads) != len(request.lead_ids):
        raise HTTPException(status_code=404, detail="Some leads not found")

    task_ids = []

    for lead in leads:
        # Update status to processing
        lead.enrichment_status = EnrichmentStatus.PROCESSING

        # Create enrichment tasks
        for enrich_type in request.enrichment_types:
            task = EnrichmentTask(lead_id=lead.id, task_type=enrich_type, status=EnrichmentStatus.PENDING)
            db.add(task)
            db.flush()  # Get the task ID

            # Trigger Celery task
            celery_task = enrich_lead_task.delay(lead.id, enrich_type, task.id)
            task.celery_task_id = celery_task.id
            task_ids.append(celery_task.id)

    db.commit()

    return {"message": f"Enrichment started for {len(leads)} leads", "task_ids": task_ids, "lead_count": len(leads)}


@router.get("/status/{lead_id}")
async def get_enrichment_status(lead_id: int, db: Session = Depends(get_db)):
    """Get enrichment status for a specific lead"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    tasks = db.query(EnrichmentTask).filter(EnrichmentTask.lead_id == lead_id).all()

    return {
        "lead_id": lead_id,
        "overall_status": lead.enrichment_status.value,
        "enriched_data": lead.enriched_data,
        "tasks": [
            {
                "task_type": task.task_type,
                "status": task.status.value,
                "result": task.result,
                "error_message": task.error_message,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            }
            for task in tasks
        ],
    }


@router.post("/retry/{lead_id}")
async def retry_enrichment(lead_id: int, db: Session = Depends(get_db)):
    """Retry failed enrichment tasks for a lead"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Find failed tasks
    failed_tasks = (
        db.query(EnrichmentTask)
        .filter(EnrichmentTask.lead_id == lead_id, EnrichmentTask.status == EnrichmentStatus.FAILED)
        .all()
    )

    if not failed_tasks:
        return {"message": "No failed tasks to retry"}

    task_ids = []
    for task in failed_tasks:
        task.status = EnrichmentStatus.PENDING
        task.error_message = None

        # Trigger Celery task again
        celery_task = enrich_lead_task.delay(lead.id, task.task_type, task.id)
        task.celery_task_id = celery_task.id
        task_ids.append(celery_task.id)

    lead.enrichment_status = EnrichmentStatus.PROCESSING
    db.commit()

    return {"message": f"Retrying {len(failed_tasks)} failed tasks", "task_ids": task_ids}
