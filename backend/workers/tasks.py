from datetime import datetime
import os

from celery import Celery

# Import database
from db.database import SessionLocal
from db.models import EnrichmentStatus, EnrichmentTask, Lead
from services.ai_enrichment import AIEnrichmentService

# Import services
from services.apollo_service import ApolloService
from services.email_validation import EmailValidationService
from services.scraper import ScraperService
from sqlalchemy.orm import Session

# Initialize Celery
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("clay_clone_workers", broker=redis_url, backend=redis_url)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(name="enrich_lead")
def enrich_lead_task(lead_id: int, enrichment_type: str, task_id: int):
    """
    Main task for enriching a lead
    Enrichment types: email, apollo, ai, scraper
    """
    db = SessionLocal()

    try:
        # Get lead and task
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        task = db.query(EnrichmentTask).filter(EnrichmentTask.id == task_id).first()

        if not lead or not task:
            return {"error": "Lead or task not found"}

        # Update task status
        task.status = EnrichmentStatus.PROCESSING
        db.commit()

        # Perform enrichment based on type
        result = None
        if enrichment_type == "email":
            result = enrich_email(lead, db)
        elif enrichment_type == "apollo":
            result = enrich_apollo(lead, db)
        elif enrichment_type == "ai":
            result = enrich_ai(lead, db)
        elif enrichment_type == "scraper":
            result = enrich_scraper(lead, db)
        else:
            result = {"error": f"Unknown enrichment type: {enrichment_type}"}

        # Update task with result
        if result and not result.get("error"):
            task.status = EnrichmentStatus.COMPLETED
            task.result = result
            task.completed_at = datetime.utcnow()

            # Update lead enriched data
            if not lead.enriched_data:
                lead.enriched_data = {}
            lead.enriched_data[enrichment_type] = result

            # Check if all tasks are complete
            all_tasks = db.query(EnrichmentTask).filter(EnrichmentTask.lead_id == lead_id).all()
            if all(t.status == EnrichmentStatus.COMPLETED for t in all_tasks):
                lead.enrichment_status = EnrichmentStatus.COMPLETED
        else:
            task.status = EnrichmentStatus.FAILED
            task.error_message = result.get("error", "Unknown error") if result else "Unknown error"
            task.completed_at = datetime.utcnow()

        db.commit()
        return result

    except Exception as e:
        # Update task as failed
        if task:
            task.status = EnrichmentStatus.FAILED
            task.error_message = str(e)
            task.completed_at = datetime.utcnow()
            db.commit()
        return {"error": str(e)}
    finally:
        db.close()


def enrich_email(lead: Lead, db: Session) -> dict:
    """Enrich lead with email validation"""
    try:
        service = EmailValidationService()

        if lead.email:
            # Validate existing email
            import asyncio

            result = asyncio.run(service.validate_email_full(lead.email))
            return result
        elif lead.first_name and lead.last_name and lead.website:
            # Try to find email
            domain = lead.website.replace("http://", "").replace("https://", "").split("/")[0]
            result = asyncio.run(service.find_email_pattern(lead.first_name, lead.last_name, domain))

            if result.get("email"):
                lead.email = result["email"]
                db.commit()

            return result
        else:
            return {"error": "Insufficient data for email enrichment"}
    except Exception as e:
        return {"error": str(e), "success": False}


def enrich_apollo(lead: Lead, db: Session) -> dict:
    """Enrich lead using Apollo.io"""
    try:
        service = ApolloService()

        if not lead.first_name or not lead.last_name:
            return {"error": "First name and last name required"}

        import asyncio

        result = asyncio.run(
            service.enrich_person(
                first_name=lead.first_name,
                last_name=lead.last_name,
                company=lead.company,
                linkedin_url=lead.linkedin_url,
            )
        )

        # Update lead with enriched data
        if result.get("success") and result.get("person"):
            person = result["person"]
            if not lead.email and person.get("email"):
                lead.email = person["email"]
            if not lead.phone and person.get("phone"):
                lead.phone = person["phone"]
            if not lead.title and person.get("title"):
                lead.title = person["title"]
            if not lead.linkedin_url and person.get("linkedin_url"):
                lead.linkedin_url = person["linkedin_url"]
            db.commit()

        return result
    except Exception as e:
        return {"error": str(e), "success": False}


def enrich_ai(lead: Lead, db: Session) -> dict:
    """Enrich lead using AI"""
    try:
        service = AIEnrichmentService()

        lead_data = {
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "company": lead.company,
            "title": lead.title,
            "linkedin_url": lead.linkedin_url,
        }

        import asyncio

        result = asyncio.run(service.enrich_lead_profile(lead_data))

        return result
    except Exception as e:
        return {"error": str(e), "success": False}


def enrich_scraper(lead: Lead, db: Session) -> dict:
    """Enrich lead using web scraping"""
    try:
        service = ScraperService()

        if not lead.website:
            return {"error": "Website URL required for scraping"}

        import asyncio

        result = asyncio.run(service.scrape_company_website(lead.website))

        return result
    except Exception as e:
        return {"error": str(e), "success": False}
