import requests
import pandas as pd
import logging
import math
from datetime import datetime

# =========================
# CONFIGURACIÓN
# =========================
BASE_URL = "http://localhost:8001"
CSV_PATH = r"/media/ubuntu/TOSHIBA EXT/UNMSM/Cycle_X/PreProssionalPractice/postings.csv"
# CSV_PATH = r"H:\UNMSM\Cycle_X\PreProssionalPractice\postings.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# LIMPIADORES
# =========================

def to_bool_required(x):
    if pd.isna(x): 
        return False
    val = str(x).strip().lower()
    if val in ["true", "1", "yes"]: return True
    return False

def to_int_required(x):
    try:
        return int(x)
    except:
        return 0

def to_str_required(x):
    if pd.isna(x) or x is None:
        return "UNKNOWN"
    s = str(x).strip()
    return s if s else "UNKNOWN"

def clean_string(x):
    """
    Devuelve un string limpio o None si está vacío.
    """
    if pd.isna(x) or x is None:
        return None
    s = str(x).strip()
    return s if s else None

def to_bool(x):
    """Convierte a bool si es posible, caso contrario None."""
    if pd.isna(x): 
        return None
    val = str(x).strip().lower()
    if val in ["true", "1", "yes"]: return True
    if val in ["false", "0", "no"]: return False
    return None

    
def to_float(val):
    """Convierte a float seguro (None si falla)."""
    try:
        if val is None or val == "" or pd.isna(val):
            return None
        f = float(val)
        if math.isinf(f) or math.isnan(f):
            return None
        return f
    except:
        return None


def to_int(val):
    """Convierte a int seguro (None si falla)."""
    try:
        if val is None or val == "" or pd.isna(val):
            return None
        return int(val)
    except:
        return None


def to_str(val):
    """Convierte strings vacíos/NaN en None."""
    if val is None or val == "" or pd.isna(val):
        return None
    return str(val)


def to_datetime(val):
    """Convierte timestamps en ISO8601 o None."""
    if val is None or val == "" or pd.isna(val):
        return None
    try:
        ts = pd.to_datetime(val, errors="coerce")
        if pd.isna(ts):
            return None
        return ts.isoformat()
    except:
        return None


def sanitize_payload(payload):
    """Asegura que nada sea NaN, inf o NaT."""
    clean = {}
    for k, v in payload.items():

        if v is None:
            clean[k] = None
            continue

        if isinstance(v, float):
            if math.isnan(v) or math.isinf(v):
                clean[k] = None
                continue

        clean[k] = v

    return clean


# =========================
# MAPEO CSV → API
# =========================

def clean_row(row):
    return {
        "company_name": clean_string(row.get("company_name")),
        "title": clean_string(row.get("title")),
        "description": clean_string(row.get("description")),
        "location": clean_string(row.get("location")),
        "job_posting_url": clean_string(row.get("job_posting_url")),
        
        # OBLIGATORIOS
        "remote_allowed": to_bool_required(row.get("remote_allowed")),
        "applies": to_int_required(row.get("applies")),
        "currency": to_str_required(row.get("currency")),

        # Opcionales
        "min_salary": to_float(row.get("min_salary")),
        "max_salary": to_float(row.get("max_salary")),
        "med_salary": to_float(row.get("med_salary")),
        "pay_period": clean_string(row.get("pay_period")),
        "company_id": clean_string(row.get("company_id")),
        "views": to_int(row.get("views")),
        "formatted_work_type": clean_string(row.get("formatted_work_type")),
        "original_listed_time": to_datetime(row.get("original_listed_time")),
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
        "compensation_type": clean_string(row.get("compensation_type")),
        "normalized_salary": to_float(row.get("normalized_salary")),
        "zip_code": clean_string(row.get("zip_code")),
        "fips": clean_string(row.get("fips")),
    }



# =========================
# IMPORTADOR PRINCIPAL
# =========================

def job_exists(url: str) -> bool:
    """Busca manualmente la URL entre los trabajos existentes."""
    try:
        resp = requests.get(f"{BASE_URL}/jobs/?limit=5000")  # trae muchos
        if resp.status_code != 50:
            return False

        jobs = resp.json()
        for job in jobs:
            if job.get("job_posting_url") == url:
                return True

        return False

    except Exception as e:
        logging.error(f"Error buscando existencia: {e}")
        return False




def main():
    df = pd.read_csv(CSV_PATH)
    logging.info(f"CSV cargado con {len(df)} registros")

    inserted = 0

    for idx, row in df.iterrows():

        url = to_str(row.get("job_posting_url"))
        if not url:
            logging.info(f"Fila {idx}: sin URL → se omite")
            continue

        if job_exists(url):
            logging.info(f"Ya existe en BD → skip: {url}")
            continue

        payload = sanitize_payload(clean_row(row))

        try:
            resp = requests.post(
                f"{BASE_URL}/jobs/",
                json=payload,
                timeout=10
            )

            if resp.status_code == 200:
                inserted += 1
                logging.info(f"[OK] Insertado #{inserted} → {url}")
            else:
                logging.error(f"[ERROR {resp.status_code}] no insertó {url}")
                logging.error(resp.text)

        except Exception as e:
            logging.error(f"Error insertando {url}: {e}")

        # Solo 200 por ahora
        if inserted >= 200:
            break

    logging.info(f"=== FIN IMPORT === total insertados: {inserted}")


if __name__ == "__main__":
    main()
