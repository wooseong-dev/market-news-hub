from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.rss_fetcher import fetch_all_feeds
from app.config import get_settings

settings = get_settings()
scheduler = BackgroundScheduler()

def scheduled_fetch():
    db = SessionLocal()
    try:
        fetch_all_feeds(db)
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            scheduled_fetch,
            "interval",
            minutes=settings.fetch_interval_minutes,
            id="fetch_news",
            replace_existing=True,
        )
        scheduler.start()
