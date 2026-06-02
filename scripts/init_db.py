from app.database import Base, engine, SessionLocal
from app.rss_fetcher import fetch_all_feeds

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    result = fetch_all_feeds(db)
    print(result)
finally:
    db.close()
