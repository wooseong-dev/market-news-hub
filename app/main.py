from datetime import datetime, timezone
from fastapi import FastAPI, Depends, Request, HTTPException, Query, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from app.config import get_settings
from app.database import Base, engine, get_db, SessionLocal
from app.models import NewsItem
from app.rss_fetcher import fetch_all_feeds
from app.scheduler import start_scheduler

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.site_name)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

CATEGORIES = ["general", "us-market", "rates", "oil", "dollar", "ai-semis", "quantum", "crypto", "korea"]

@app.on_event("startup")
def on_startup():
    start_scheduler()
    db = SessionLocal()
    try:
        if db.query(NewsItem).count() == 0:
            fetch_all_feeds(db)
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    latest = (
        db.query(NewsItem)
        .filter(NewsItem.is_hidden == False)
        .order_by(desc(NewsItem.published_at))
        .limit(30)
        .all()
    )
    high = [item for item in latest if item.importance == "High"][:5]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings,
            "items": latest,
            "high_items": high,
            "categories": CATEGORIES,
            "now": datetime.now(timezone.utc),
            "page_title": settings.site_name,
            "page_description": "시장 변동성 뉴스, 금리, 유가, 달러, AI, 반도체, 크립토 정책 뉴스를 한 화면에서 확인합니다.",
        },
    )

@app.get("/news", response_class=HTMLResponse)
def news_list(
    request: Request,
    q: str = "",
    category: str = "",
    importance: str = "",
    db: Session = Depends(get_db),
):
    query = db.query(NewsItem).filter(NewsItem.is_hidden == False)

    if q:
        like = f"%{q}%"
        query = query.filter(or_(NewsItem.title.ilike(like), NewsItem.summary.ilike(like), NewsItem.assets.ilike(like)))
    if category:
        query = query.filter(NewsItem.category == category)
    if importance:
        query = query.filter(NewsItem.importance == importance)

    items = query.order_by(desc(NewsItem.published_at)).limit(100).all()

    return templates.TemplateResponse(
        "news_list.html",
        {
            "request": request,
            "settings": settings,
            "items": items,
            "categories": CATEGORIES,
            "q": q,
            "selected_category": category,
            "selected_importance": importance,
            "page_title": "뉴스 전체",
            "page_description": "시장 뉴스 전체 목록과 카테고리별 필터.",
        },
    )

@app.get("/news/{category}", response_class=HTMLResponse)
def news_by_category(category: str, request: Request, db: Session = Depends(get_db)):
    if category not in CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")

    items = (
        db.query(NewsItem)
        .filter(NewsItem.is_hidden == False, NewsItem.category == category)
        .order_by(desc(NewsItem.published_at))
        .limit(80)
        .all()
    )
    return templates.TemplateResponse(
        "news_list.html",
        {
            "request": request,
            "settings": settings,
            "items": items,
            "categories": CATEGORIES,
            "q": "",
            "selected_category": category,
            "selected_importance": "",
            "page_title": f"{category} 뉴스",
            "page_description": f"{category} 관련 시장 뉴스.",
        },
    )

@app.get("/article/{slug}", response_class=HTMLResponse)
def news_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    item = db.query(NewsItem).filter(NewsItem.slug == slug, NewsItem.is_hidden == False).first()
    if not item:
        raise HTTPException(status_code=404, detail="Article not found")

    related = (
        db.query(NewsItem)
        .filter(NewsItem.is_hidden == False, NewsItem.category == item.category, NewsItem.id != item.id)
        .order_by(desc(NewsItem.published_at))
        .limit(6)
        .all()
    )

    return templates.TemplateResponse(
        "news_detail.html",
        {
            "request": request,
            "settings": settings,
            "item": item,
            "related": related,
            "page_title": item.title,
            "page_description": item.interpretation[:150],
        },
    )

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "settings": settings, "page_title": "About", "page_description": "사이트 소개"})

@app.get("/privacy", response_class=HTMLResponse)
def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request, "settings": settings, "page_title": "Privacy Policy", "page_description": "개인정보 처리방침"})

@app.get("/terms", response_class=HTMLResponse)
def terms(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request, "settings": settings, "page_title": "Terms", "page_description": "이용약관"})

@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "settings": settings, "page_title": "Contact", "page_description": "문의"})

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    body = f"""User-agent: *
Allow: /

Sitemap: {settings.site_url}/sitemap.xml
"""
    return body

@app.get("/sitemap.xml")
def sitemap(db: Session = Depends(get_db)):
    items = (
        db.query(NewsItem)
        .filter(NewsItem.is_hidden == False)
        .order_by(desc(NewsItem.published_at))
        .limit(1000)
        .all()
    )
    static_urls = ["", "/news", "/about", "/privacy", "/terms", "/contact"]
    urls = []
    for path in static_urls:
        urls.append((f"{settings.site_url}{path}", datetime.now(timezone.utc).date().isoformat()))
    for category in CATEGORIES:
        urls.append((f"{settings.site_url}/news/{category}", datetime.now(timezone.utc).date().isoformat()))
    for item in items:
        lastmod = item.published_at.date().isoformat() if item.published_at else datetime.now(timezone.utc).date().isoformat()
        urls.append((f"{settings.site_url}/article/{item.slug}", lastmod))

    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in urls:
        xml.append(f"<url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), media_type="application/xml")

@app.get("/admin/refresh")
def admin_refresh(key: str = Query(...), db: Session = Depends(get_db)):
    if key != settings.admin_refresh_key:
        raise HTTPException(status_code=403, detail="Invalid key")
    result = fetch_all_feeds(db)
    return result
