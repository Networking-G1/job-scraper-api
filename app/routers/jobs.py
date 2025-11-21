# ============= app/routers/jobs.py =============
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db
from ..scraper.linkedin_scraper import LinkedInScraper
import logging

router = APIRouter(prefix="/jobs", tags=["jobs"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.JobPosting)
def create_job(job: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    """Crear una nueva oferta de trabajo manualmente"""
    try:
        return crud.create_job_posting(db, job)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.JobPosting])
def get_jobs(
    skip: int = 0,
    limit: int = 100,
    location: Optional[str] = None,
    company_name: Optional[str] = None,
    remote_allowed: Optional[bool] = None,
    experience_level: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de ofertas de trabajo con filtros opcionales"""
    jobs = crud.get_job_postings(
        db, 
        skip=skip, 
        limit=limit,
        location=location,
        company_name=company_name,
        remote_allowed=remote_allowed,
        experience_level=experience_level,
        search=search
    )
    return jobs

@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de las ofertas"""
    return crud.get_job_statistics(db)

@router.get("/{job_id}", response_model=schemas.JobPosting)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Obtener una oferta específica por ID"""
    job = crud.get_job_posting(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=schemas.JobPosting)
def update_job(job_id: int, job: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    """Actualizar una oferta de trabajo"""
    updated_job = crud.update_job_posting(db, job_id, job)
    if not updated_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return updated_job

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Eliminar una oferta de trabajo"""
    success = crud.delete_job_posting(db, job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}

@router.post("/scrape")
async def scrape_jobs(
    background_tasks: BackgroundTasks,
    keywords: str = "practicas profesionales",
    location: str = "Lima, Peru",
    db: Session = Depends(get_db)
):
    """
    Iniciar proceso de scraping de ofertas de trabajo
    Este endpoint ejecuta el scraping en background
    """
    def scrape_and_save():
        try:
            scraper = LinkedInScraper()
            jobs = scraper.scrape_jobs(keywords.split(","), location)
            
            saved_count = 0
            for job_data in jobs:
                try:
                    job = schemas.JobPostingCreate(**job_data)
                    crud.create_job_posting(db, job)
                    saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving job: {e}")
                    continue
            
            logger.info(f"Scraping completed. Saved {saved_count} jobs")
        except Exception as e:
            logger.error(f"Scraping error: {e}")
    
    background_tasks.add_task(scrape_and_save)
    
    return {
        "message": "Scraping initiated in background",
        "keywords": keywords,
        "location": location
    }
