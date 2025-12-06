import pandas as pd
import asyncio
import logging
from datetime import datetime
from tqdm import tqdm   # PROGRESS BAR
from app.database import SessionLocal
from app.models import JobPosting

# =======================================================
# CONFIG
# =======================================================
CSV_PATH = "postings.csv/postings.csv"
BATCH_SIZE = 100  # PROCESAR SOLO 200 TAREAS A LA VEZ

# =======================================================
# LOGGING SETUP
# =======================================================
logging.basicConfig(
    filename="job_import.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("=== Starting asynchronous job import ===")


# =======================================================
# CLEANING HELPERS
# (igual que antes, no los toco)
# =======================================================

def clean_string(x):
    if pd.isna(x):
        return None
    return str(x).strip()

def to_bool(x):
    if pd.isna(x): return None
    val = str(x).strip().lower()
    if val in ["true", "1", "yes"]: return True
    if val in ["false", "0", "no"]: return False
    return None

def to_float(x):
    try: return float(x)
    except: return None

def to_int(x):
    try: return int(x)
    except: return None

def to_datetime(x):
    if pd.isna(x) or x == "":
        return None
    try:
        if str(x).isdigit():
            return datetime.fromtimestamp(int(x))
        return pd.to_datetime(x, errors="coerce")
    except:
        return None

def clean_row(row):
    return {
        "company_name": clean_string(row.get("company_name")),
        "title": clean_string(row.get("title")),
        "description": clean_string(row.get("description")),
        "max_salary": to_float(row.get("max_salary")),
        "min_salary": to_float(row.get("min_salary")),
        "med_salary": to_float(row.get("med_salary")),
        "pay_period": clean_string(row.get("pay_period")),
        "location": clean_string(row.get("location")),
        "company_id": clean_string(row.get("company_id")),
        "views": to_int(row.get("views")),
        "formatted_work_type": clean_string(row.get("formatted_work_type")),
        "applies": to_int(row.get("applies")),
        "original_listed_time": to_datetime(row.get("original_listed_time")),
        "remote_allowed": to_bool(row.get("remote_allowed")),
        "job_posting_url": clean_string(row.get("job_posting_url")),
        "application_url": clean_string(row.get("application_url")),
        "application_type": clean_string(row.get("application_type")),
        "expiry": to_datetime(row.get("expiry")),
        "closed_time": to_datetime(row.get("closed_time")),
        "formatted_experience_level": clean_string(row.get("formatted_experience_level")),
        "skills_desc": clean_string(row.get("skills_desc")),
        "listed_time": to_datetime(row.get("listed_time")),
        "posting_domain": clean_string(row.get("posting_domain")),
        "sponsored": to_bool(row.get("sponsored")),
        "work_type": clean_string(row.get("work_type")),
        "currency": clean_string(row.get("currency")),
        "compensation_type": clean_string(row.get("compensation_type")),
        "normalized_salary": to_float(row.get("normalized_salary")),
        "zip_code": clean_string(row.get("zip_code")),
        "fips": clean_string(row.get("fips")),
    }


# =======================================================
# INSERT FUNCTION
# =======================================================

def insert_job(session, payload):
    if not payload["job_posting_url"]:
        logging.warning("Skipping empty URL row.")
        return None

    # Check duplicate
    existing = session.query(JobPosting).filter(JobPosting.job_posting_url == payload['job_posting_url']).first()
    if existing:
        logging.info(f"Already exists: {payload['job_posting_url']}")
        return None

    # Insert
    job = JobPosting(**payload)
    session.add(job)
    session.commit()
    logging.info(f"Inserted {job.id} | {payload['title']}")
    return job.id


# =======================================================
# MAIN
# =======================================================

def main():
    print("📌 Loading CSV...")
    df = pd.read_csv(CSV_PATH)
    total = len(df)
    print(f"🔎 Rows: {total}")

    with SessionLocal() as session:
        batch_number = 0  # 👈 contador de batches

        for i in tqdm(range(0, total, BATCH_SIZE), desc="Processing batches"):
            batch_number += 1

            # 🔥 SOLO PROCESAR 2 BATCHES (200 x 2 = 400 trabajos)
            if batch_number > 1:
                print("🛑 Test mode: stopped after 2 batches.")
                logging.info("Stopped after 2 batches (test mode).")
                break

            batch = df.iloc[i:i+BATCH_SIZE]

            for _, row in batch.iterrows():
                payload = clean_row(row)
                insert_job(session, payload)

    print("🎉 Import completed!")
    logging.info("=== Import finished successfully ===")


if __name__ == "__main__":
    main()
