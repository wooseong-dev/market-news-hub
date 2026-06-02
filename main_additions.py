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
