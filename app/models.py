# ============= app/models.py =============
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from .database import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(String)
    max_salary = Column(Float, nullable=True)
    pay_period = Column(String, nullable=True)
    location = Column(String, index=True)
    company_id = Column(String, nullable=True)
    views = Column(Integer, default=0)
    med_salary = Column(Float, nullable=True)
    min_salary = Column(Float, nullable=True)
    formatted_work_type = Column(String, nullable=True)
    applies = Column(Integer, default=0)
    original_listed_time = Column(DateTime, nullable=True)
    remote_allowed = Column(Boolean, default=False)
    job_posting_url = Column(String, unique=True)
    application_url = Column(String, nullable=True)
    application_type = Column(String, nullable=True)
    expiry = Column(DateTime, nullable=True)
    closed_time = Column(DateTime, nullable=True)
    formatted_experience_level = Column(String, nullable=True)
    skills_desc = Column(String, nullable=True)
    listed_time = Column(DateTime, default=datetime.utcnow)
    posting_domain = Column(String, nullable=True)
    sponsored = Column(Boolean, default=False)
    work_type = Column(String, nullable=True)
    currency = Column(String, default="USD")
    compensation_type = Column(String, nullable=True)
    normalized_salary = Column(Float, nullable=True)
    zip_code = Column(String, nullable=True)
    fips = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)