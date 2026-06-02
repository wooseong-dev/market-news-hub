from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from slugify import slugify
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
import feedparser

from app.models import NewsItem
from app.feeds import FEEDS
from app.classifier import (
    classify_category,
    classify_importance,
    detect_assets,
    detect_certainty,
    make_interpretation,
)
from app.config import get_settings

settings = get_settings()

def clean_html(value: str | None) -> str:
    if not value:
        return ""
    soup = BeautifulSoup(value, "html.parser")
    text = soup.get_text(" ", strip=True)
    return " ".join(text.split())[:600]

def parse_date(entry) -> datetime:
    for key in ["published", "updated", "created"]:
        raw = getattr(entry, key, None)
        if raw:
            try:
                dt = parsedate_to_datetime(raw)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except Exception:
                pass
    return datetime.now(timezone.utc)

def make_unique_slug(db, title: str) -> str:
    base = slugify(title, max_length=100) or "news"
    slug = base
    idx = 2
    while db.query(NewsItem).filter(NewsItem.slug == slug).first():
        slug = f"{base}-{idx}"
        idx += 1
    return slug

def fetch_all_feeds(db) -> dict:
    inserted = 0
    skipped = 0
    errors: list[str] = []

    for feed in FEEDS:
        try:
            parsed = feedparser.parse(feed["url"])
            for entry in parsed.entries[: settings.max_items_per_feed]:
                title = clean_html(getattr(entry, "title", ""))
                url = getattr(entry, "link", "")
                if not title or not url:
                    skipped += 1
                    continue

                summary = clean_html(getattr(entry, "summary", "") or getattr(entry, "description", ""))
                published_at = parse_date(entry)
                category = classify_category(title, summary)
                importance = classify_importance(title, summary)
                assets = detect_assets(title, summary)
                certainty = detect_certainty(title, summary)
                interpretation = make_interpretation(title, category, assets, importance)

                if db.query(NewsItem).filter(NewsItem.url == url).first():
                    skipped += 1
                    continue

                item = NewsItem(
                    title=title,
                    slug=make_unique_slug(db, title),
                    url=url,
                    source=feed["name"],
                    category=category,
                    summary=summary,
                    interpretation=interpretation,
                    importance=importance,
                    assets=assets,
                    certainty=certainty,
                    published_at=published_at,
                )
                db.add(item)
                try:
                    db.commit()
                    inserted += 1
                except IntegrityError:
                    db.rollback()
                    skipped += 1
        except Exception as exc:
            errors.append(f"{feed['name']}: {exc}")

    return {"inserted": inserted, "skipped": skipped, "errors": errors}
