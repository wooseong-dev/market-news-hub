from datetime import datetime, timezone

from fastapi import FastAPI, Depends, Request, HTTPException, Query, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc as sa_desc, or_

from app.config import get_settings
from app.database import Base, engine, get_db, SessionLocal
from app.models import NewsItem
from app.rss_fetcher import fetch_all_feeds
from app.scheduler import start_scheduler
from app.i18n import tx, lang_of_path, localize, alt_paths, cat_label, interp_item, GUIDES


settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.site_name)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# 템플릿에서 쓰는 함수 등록
templates.env.globals["localize"] = localize
templates.env.globals["localized_path"] = localize
templates.env.globals["cat_label"] = cat_label
templates.env.globals["category_label"] = cat_label
templates.env.globals["interp_item"] = interp_item
templates.env.globals["interpret_item"] = interp_item

# app/main.py 안에서 templates.env.globals 등록하는 부분 아래에 붙여넣기

CATEGORY_UI = {
    "general": {"icon": "◎", "ko": "시장", "en": "Market"},
    "us-market": {"icon": "US", "ko": "미국장", "en": "US Market"},
    "rates": {"icon": "%", "ko": "금리", "en": "Rates"},
    "oil": {"icon": "OIL", "ko": "유가", "en": "Oil"},
    "dollar": {"icon": "$", "ko": "달러", "en": "Dollar"},
    "ai-semis": {"icon": "AI", "ko": "AI/반도체", "en": "AI/Semis"},
    "quantum": {"icon": "Q", "ko": "양자컴퓨팅", "en": "Quantum"},
    "crypto": {"icon": "₿", "ko": "크립토", "en": "Crypto"},
    "korea": {"icon": "KR", "ko": "한국장", "en": "Korea"},
}

def split_tags(value: str):
    if not value:
        return []
    return [tag.strip() for tag in str(value).split(",") if tag.strip()]

def category_icon(category: str) -> str:
    return CATEGORY_UI.get(category, CATEGORY_UI["general"])["icon"]

def category_name(category: str, lang: str = "ko") -> str:
    meta = CATEGORY_UI.get(category, CATEGORY_UI["general"])
    return meta.get(lang, meta["ko"])

def importance_label(value: str, lang: str = "ko") -> str:
    labels = {
        "ko": {"High": "높음", "Medium": "보통", "Low": "낮음"},
        "en": {"High": "High", "Medium": "Medium", "Low": "Low"},
    }
    return labels.get(lang, labels["ko"]).get(value, value)

templates.env.globals["split_tags"] = split_tags
templates.env.globals["category_icon"] = category_icon
templates.env.globals["category_name"] = category_name
templates.env.globals["importance_label"] = importance_label

CATEGORIES = [
    "general",
    "us-market",
    "rates",
    "oil",
    "dollar",
    "ai-semis",
    "quantum",
    "crypto",
    "korea",
]


def ctx(request: Request, page_title: str, page_description: str, **kwargs):
    lang = lang_of_path(request.url.path)
    paths = alt_paths(request.url.path)
    texts = tx(lang)

    base = {
        "request": request,
        "settings": settings,
        "lang": lang,
        "text": texts,
        "t": texts,
        "categories": CATEGORIES,
        "page_title": page_title,
        "page_description": page_description,
        "ko_path": paths["ko"],
        "en_path": paths["en"],
        "now": datetime.now(timezone.utc),
    }
    base.update(kwargs)
    return base


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
@app.get("/en", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    lang = lang_of_path(request.url.path)

    latest = (
        db.query(NewsItem)
        .filter(NewsItem.is_hidden == False)
        .order_by(sa_desc(NewsItem.published_at))
        .limit(30)
        .all()
    )

    high = [item for item in latest if item.importance == "High"][:5]

    title = (
        settings.site_name
        if lang == "ko"
        else f"{settings.site_name} - Market Volatility Radar"
    )

    description = (
        "시장 변동성 뉴스, 금리, 유가, 달러, AI, 반도체, 크립토 정책 뉴스를 한 화면에서 확인합니다."
        if lang == "ko"
        else "Track market-moving news across rates, oil, the dollar, AI, semiconductors, crypto policy, and Korea markets."
    )

    return templates.TemplateResponse(
        "index.html",
        ctx(
            request,
            title,
            description,
            items=latest,
            high_items=high,
        ),
    )


@app.get("/news", response_class=HTMLResponse)
@app.get("/en/news", response_class=HTMLResponse)
def news_list(
    request: Request,
    q: str = "",
    category: str = "",
    importance: str = "",
    db: Session = Depends(get_db),
):
    lang = lang_of_path(request.url.path)

    query = db.query(NewsItem).filter(NewsItem.is_hidden == False)

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                NewsItem.title.ilike(like),
                NewsItem.summary.ilike(like),
                NewsItem.assets.ilike(like),
            )
        )

    if category:
        query = query.filter(NewsItem.category == category)

    if importance:
        query = query.filter(NewsItem.importance == importance)

    items = (
        query.order_by(sa_desc(NewsItem.published_at))
        .limit(100)
        .all()
    )

    title = "뉴스 전체" if lang == "ko" else "All News"
    description = (
        "시장 뉴스 전체 목록과 카테고리별 필터."
        if lang == "ko"
        else "All market news with category and impact filters."
    )

    return templates.TemplateResponse(
        "news_list.html",
        ctx(
            request,
            title,
            description,
            items=items,
            q=q,
            selected_category=category,
            selected_importance=importance,
        ),
    )


@app.get("/news/{category}", response_class=HTMLResponse)
@app.get("/en/news/{category}", response_class=HTMLResponse)
def news_by_category(
    category: str,
    request: Request,
    db: Session = Depends(get_db),
):
    lang = lang_of_path(request.url.path)

    if category not in CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")

    items = (
        db.query(NewsItem)
        .filter(
            NewsItem.is_hidden == False,
            NewsItem.category == category,
        )
        .order_by(sa_desc(NewsItem.published_at))
        .limit(80)
        .all()
    )

    label = cat_label(category, lang)

    title = f"{label} 뉴스" if lang == "ko" else f"{label} News"
    description = (
        f"{label} 관련 시장 뉴스."
        if lang == "ko"
        else f"Market news related to {label}."
    )

    return templates.TemplateResponse(
        "news_list.html",
        ctx(
            request,
            title,
            description,
            items=items,
            q="",
            selected_category=category,
            selected_importance="",
        ),
    )


@app.get("/article/{slug}", response_class=HTMLResponse)
@app.get("/en/article/{slug}", response_class=HTMLResponse)
def news_detail(
    slug: str,
    request: Request,
    db: Session = Depends(get_db),
):
    lang = lang_of_path(request.url.path)

    item = (
        db.query(NewsItem)
        .filter(
            NewsItem.slug == slug,
            NewsItem.is_hidden == False,
        )
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Article not found")

    related = (
        db.query(NewsItem)
        .filter(
            NewsItem.is_hidden == False,
            NewsItem.category == item.category,
            NewsItem.id != item.id,
        )
        .order_by(sa_desc(NewsItem.published_at))
        .limit(6)
        .all()
    )

    return templates.TemplateResponse(
        "news_detail.html",
        ctx(
            request,
            item.title,
            interp_item(item, lang)[:150],
            item=item,
            related=related,
        ),
    )


@app.get("/guides", response_class=HTMLResponse)
@app.get("/en/guides", response_class=HTMLResponse)
def guides(request: Request):
    lang = lang_of_path(request.url.path)

    title = (
        "시장 해석 가이드"
        if lang == "ko"
        else "Market Interpretation Guides"
    )

    description = (
        "시장 변동성을 이해하기 위한 고정 가이드."
        if lang == "ko"
        else "Evergreen guides for understanding market volatility."
    )

    return templates.TemplateResponse(
        "guides.html",
        ctx(
            request,
            title,
            description,
            guides=GUIDES[lang],
        ),
    )


@app.get("/guides/{slug}", response_class=HTMLResponse)
@app.get("/en/guides/{slug}", response_class=HTMLResponse)
def guide_detail(slug: str, request: Request):
    lang = lang_of_path(request.url.path)

    guide = next((g for g in GUIDES[lang] if g["slug"] == slug), None)

    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    guide_description = guide.get("description") or guide.get("sa_description") or ""

    return templates.TemplateResponse(
        "guide_detail.html",
        ctx(
            request,
            guide["title"],
            guide_description,
            guide=guide,
        ),
    )


@app.get("/about", response_class=HTMLResponse)
@app.get("/en/about", response_class=HTMLResponse)
def about(request: Request):
    lang = lang_of_path(request.url.path)

    return templates.TemplateResponse(
        "about.html",
        ctx(
            request,
            "About",
            "사이트 소개" if lang == "ko" else "About this site",
        ),
    )


@app.get("/privacy", response_class=HTMLResponse)
@app.get("/en/privacy", response_class=HTMLResponse)
def privacy(request: Request):
    lang = lang_of_path(request.url.path)
    body = tx(lang).get("privacy") or tx(lang).get("privacy_body") or ""

    return templates.TemplateResponse(
        "simple.html",
        ctx(
            request,
            "Privacy Policy",
            "개인정보 처리방침" if lang == "ko" else "Privacy Policy",
            heading="Privacy Policy",
            body=body,
        ),
    )


@app.get("/terms", response_class=HTMLResponse)
@app.get("/en/terms", response_class=HTMLResponse)
def terms(request: Request):
    lang = lang_of_path(request.url.path)
    body = tx(lang).get("terms") or tx(lang).get("terms_body") or ""

    return templates.TemplateResponse(
        "simple.html",
        ctx(
            request,
            "Terms",
            "이용약관" if lang == "ko" else "Terms of Use",
            heading="Terms",
            body=body,
        ),
    )


@app.get("/contact", response_class=HTMLResponse)
@app.get("/en/contact", response_class=HTMLResponse)
def contact(request: Request):
    lang = lang_of_path(request.url.path)
    body = tx(lang).get("contact") or tx(lang).get("contact_body") or ""

    return templates.TemplateResponse(
        "simple.html",
        ctx(
            request,
            "Contact",
            "문의" if lang == "ko" else "Contact",
            heading="Contact",
            body=body,
        ),
    )


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return f"""User-agent: *
Allow: /

Sitemap: {settings.site_url}/sitemap.xml
"""


@app.get("/sitemap.xml")
def sitemap(db: Session = Depends(get_db)):
    items = (
        db.query(NewsItem)
        .filter(NewsItem.is_hidden == False)
        .order_by(sa_desc(NewsItem.published_at))
        .limit(1000)
        .all()
    )

    today = datetime.now(timezone.utc).date().isoformat()
    urls = []

    static_paths = [
        "",
        "/news",
        "/about",
        "/privacy",
        "/terms",
        "/contact",
        "/guides",
    ]

    for path in static_paths:
        urls.append((f"{settings.site_url}{path}", today))

        en_path = "/en" if path == "" else f"/en{path}"
        urls.append((f"{settings.site_url}{en_path}", today))

    for category in CATEGORIES:
        urls.append((f"{settings.site_url}/news/{category}", today))
        urls.append((f"{settings.site_url}/en/news/{category}", today))

    for guide_lang in ["ko", "en"]:
        prefix = "" if guide_lang == "ko" else "/en"

        for guide in GUIDES[guide_lang]:
            urls.append(
                (
                    f"{settings.site_url}{prefix}/guides/{guide['slug']}",
                    today,
                )
            )

    for item in items:
        lastmod = (
            item.published_at.date().isoformat()
            if item.published_at
            else today
        )

        urls.append((f"{settings.site_url}/article/{item.slug}", lastmod))
        urls.append((f"{settings.site_url}/en/article/{item.slug}", lastmod))

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for loc, lastmod in urls:
        xml.append(f"<url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>")

    xml.append("</urlset>")

    return Response("\n".join(xml), media_type="application/xml")


@app.get("/admin/refresh")
def admin_refresh(key: str = Query(...), db: Session = Depends(get_db)):
    if key != settings.admin_refresh_key:
        raise HTTPException(status_code=403, detail="Invalid key")

    return fetch_all_feeds(db)