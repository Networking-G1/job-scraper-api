import pandas as pd
import requests
from datetime import datetime

# ==============================
# CONFIG
# ==============================
CSV_PATH = r"H:\UNMSM\Cycle_X\PreProssionalPractice\postings.csv"
BASE_URL = "http://localhost:8000/jobs/"

# ==============================
# HELPERS
# ==============================

def to_bool(x):
    if str(x).lower() in ["true", "1", "yes"]:
        return True
    if str(x).lower() in ["false", "0", "no"]:
        return False
    return None

def to_datetime(x):
    try:
        return datetime.fromtimestamp(int(x)) if str(x).isdigit() else pd.to_datetime(x)
    except:
        return None

# ==============================
# MAIN LOGIC
# ==============================

def main():
    print("Reading CSV...")
    df = pd.read_csv(CSV_PATH)

    print(f"Total rows found: {len(df)}")

    for index, row in df.iterrows():
        print(f"\n➡ Processing row {index + 1}/{len(df)}")

        # Build JSON body according to DB structure
        payload = {
            "company_name": row.get("company_name"),
            "title": row.get("title"),
            "description": row.get("description"),
            "max_salary": row.get("max_salary"),
            "min_salary": row.get("min_salary"),
            "med_salary": row.get("med_salary"),
            "pay_period": row.get("pay_period"),
            "location": row.get("location"),
            "company_id": row.get("company_id"),
            "views": row.get("views"),
            "formatted_work_type": row.get("formatted_work_type"),
            "applies": row.get("applies"),
            "original_listed_time": to_datetime(row.get("original_listed_time")),
            "remote_allowed": to_bool(row.get("remote_allowed")),
            "job_posting_url": row.get("job_posting_url"),
            "application_url": row.get("application_url"),
            "application_type": row.get("application_type"),
            "expiry": to_datetime(row.get("expiry")),
            "closed_time": to_datetime(row.get("closed_time")),
            "formatted_experience_level": row.get("formatted_experience_level"),
            "skills_desc": row.get("skills_desc"),
            "listed_time": to_datetime(row.get("listed_time")),
            "posting_domain": row.get("posting_domain"),
            "sponsored": to_bool(row.get("sponsored")),
            "work_type": row.get("work_type"),
            "currency": row.get("currency"),
            "compensation_type": row.get("compensation_type"),
            "normalized_salary": row.get("normalized_salary"),
            "zip_code": row.get("zip_code"),
            "fips": row.get("fips"),
        }

        # ==============================
        # CHECK IF ALREADY EXISTS
        # ==============================
        check_url = BASE_URL + "?job_posting_url=" + str(row["job_posting_url"])
        exists = requests.get(check_url)

        if exists.status_code == 200 and len(exists.json()) > 0:
            print("⚠ Job already exists in database. Skipping...")
            continue

        # ==============================
        # INSERT INTO API
        # ==============================
        response = requests.post(BASE_URL, json=payload)

        if response.status_code in [200, 201]:
            print("Inserted:", response.json().get("id"))
        else:
            print("Error inserting record:", response.text)

    print("\n🎉 Completed job posting import!")

# Run
if __name__ == "__main__":
    main()
