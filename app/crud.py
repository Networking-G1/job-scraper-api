# ============= app/crud.py =============
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from . import models, schemas
from typing import List, Optional

def create_job_posting(db: Session, job: schemas.JobPostingCreate):
    db_job = models.JobPosting(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job_posting(db: Session, job_id: int):
    return db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()

def get_job_postings(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    location: Optional[str] = None,
    company_name: Optional[str] = None,
    remote_allowed: Optional[bool] = None,
    experience_level: Optional[str] = None,
    search: Optional[str] = None
):
    query = db.query(models.JobPosting)
    
    if location:
        query = query.filter(models.JobPosting.location.ilike(f"%{location}%"))
    
    if company_name:
        query = query.filter(models.JobPosting.company_name.ilike(f"%{company_name}%"))
    
    if remote_allowed is not None:
        query = query.filter(models.JobPosting.remote_allowed == remote_allowed)
    
    if experience_level:
        query = query.filter(models.JobPosting.formatted_experience_level.ilike(f"%{experience_level}%"))
    
    if search:
        query = query.filter(
            or_(
                models.JobPosting.title.ilike(f"%{search}%"),
                models.JobPosting.description.ilike(f"%{search}%"),
                models.JobPosting.skills_desc.ilike(f"%{search}%")
            )
        )
    
    return query.offset(skip).limit(limit).all()

def update_job_posting(db: Session, job_id: int, job: schemas.JobPostingCreate):
    db_job = get_job_posting(db, job_id)
    if db_job:
        for key, value in job.model_dump().items():
            setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
    return db_job

def delete_job_posting(db: Session, job_id: int):
    db_job = get_job_posting(db, job_id)
    if db_job:
        db.delete(db_job)
        db.commit()
        return True
    return False

def get_job_statistics(db: Session):
    total_jobs = db.query(models.JobPosting).count()
    remote_jobs = db.query(models.JobPosting).filter(models.JobPosting.remote_allowed == True).count()
    
    avg_salary = db.query(models.JobPosting).filter(
        models.JobPosting.normalized_salary.isnot(None)
    ).with_entities(models.JobPosting.normalized_salary).all()
    
    avg_salary_value = sum([s[0] for s in avg_salary]) / len(avg_salary) if avg_salary else 0
    
    return {
        "total_jobs": total_jobs,
        "remote_jobs": remote_jobs,
        "average_salary": round(avg_salary_value, 2)
    }