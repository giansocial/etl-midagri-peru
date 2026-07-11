import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "produccion_agricola"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
QUALITY_DIR = DATA_DIR / "quality_reports"

REQUESTS_TIMEOUT = int(os.getenv("REQUESTS_TIMEOUT", "30"))
REQUESTS_RETRY = int(os.getenv("REQUESTS_RETRY", "3"))

USER_AGENT = "ETL-ProduccionAgricola/1.0 (Proyecto academico)"
