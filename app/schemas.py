# ============= app/schemas.py =============
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class JobPostingBase(BaseModel):
    company_name: str
    title: str
    description: str
    max_salary: Optional[float] = None
    pay_period: Optional[str] = None
    location: str
    company_id: Optional[str] = None
    views: int = 0
    med_salary: Optional[float] = None
    min_salary: Optional[float] = None
    formatted_work_type: Optional[str] = None
    applies: int = 0
    original_listed_time: Optional[datetime] = None
    remote_allowed: bool = False
    job_posting_url: str
    application_url: Optional[str] = None
    application_type: Optional[str] = None
    expiry: Optional[datetime] = None
    closed_time: Optional[datetime] = None
    formatted_experience_level: Optional[str] = None
    skills_desc: Optional[str] = None
    listed_time: Optional[datetime] = None
    posting_domain: Optional[str] = None
    sponsored: bool = False
    work_type: Optional[str] = None
    currency: str = "USD"
    compensation_type: Optional[str] = None
    normalized_salary: Optional[float] = None
    zip_code: Optional[str] = None
    fips: Optional[str] = None

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True