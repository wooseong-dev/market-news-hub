from functools import lru_cache
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    site_name: str = os.getenv("SITE_NAME", "Market Risk Radar")
    site_url: str = os.getenv("SITE_URL", "http://127.0.0.1:8000").rstrip("/")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/news.db")
    admin_refresh_key: str = os.getenv("ADMIN_REFRESH_KEY", "change-me")
    adsense_client_id: str = os.getenv("ADSENSE_CLIENT_ID", "")
    ga_measurement_id: str = os.getenv("GA_MEASUREMENT_ID", "")
    fetch_interval_minutes: int = int(os.getenv("FETCH_INTERVAL_MINUTES", "30"))
    max_items_per_feed: int = int(os.getenv("MAX_ITEMS_PER_FEED", "15"))

@lru_cache
def get_settings() -> Settings:
    return Settings()
