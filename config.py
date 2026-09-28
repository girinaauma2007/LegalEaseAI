import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "LegalEase")
    company_name: str = os.getenv("COMPANY_NAME", "LegalEase")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    backend_url: str = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    host: str = os.getenv("APP_HOST", "127.0.0.1")
    port: int = int(os.getenv("APP_PORT", "8000"))

settings = Settings()
