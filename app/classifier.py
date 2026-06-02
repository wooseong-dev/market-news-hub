from __future__ import annotations

CATEGORY_RULES = {
    "crypto": ["bitcoin", "btc", "ethereum", "eth", "crypto", "sec", "cftc", "stablecoin", "blockchain", "digital asset", "coinbase", "binance", "etf approval"],
    "rates": ["fed", "fomc", "rate cut", "rate hike", "treasury", "yield", "inflation", "cpi", "ppi", "payroll", "jobs report", "powell"],
    "oil": ["oil", "brent", "wti", "opec", "energy prices", "crude", "middle east", "iran", "israel"],
    "dollar": ["dollar", "dxy", "yen", "won", "currency", "fx", "foreign exchange"],
    "ai-semis": ["ai", "artificial intelligence", "nvidia", "semiconductor", "chip", "tsmc", "amd", "broadcom", "openai", "data center"],
    "quantum": ["quantum", "qubit", "ionq", "rigetti", "d-wave", "ibm quantum"],
    "korea": ["korea", "kospi", "kosdaq", "samsung", "sk hynix", "bank of korea", "won", "export"],
    "us-market": ["nasdaq", "s&p 500", "dow", "wall street", "stocks", "earnings", "market rally", "selloff"],
}

ASSET_RULES = {
    "BTC/ETH": ["bitcoin", "btc", "ethereum", "eth", "crypto", "stablecoin", "coinbase", "binance"],
    "Nasdaq": ["nasdaq", "tech stocks", "growth stocks", "ai", "semiconductor", "nvidia", "amd"],
    "Rates": ["fed", "fomc", "treasury", "yield", "rate", "inflation", "cpi", "ppi"],
    "Oil": ["oil", "brent", "wti", "opec", "crude", "energy prices"],
    "USD/KRW": ["dollar", "dxy", "won", "yen", "currency", "fx"],
    "Korea": ["korea", "kospi", "kosdaq", "samsung", "sk hynix"],
    "Quantum": ["quantum", "qubit", "ionq", "rigetti", "d-wave", "ibm quantum"],
}

HIGH_WORDS = ["breaking", "surge", "plunge", "war", "attack", "sanction", "fomc", "cpi", "payroll", "rate cut", "rate hike", "sec", "approval", "ban", "tariff"]
MEDIUM_WORDS = ["earnings", "forecast", "guidance", "policy", "inflation", "oil", "yield", "dollar", "ai", "semiconductor"]

OFFICIAL_WORDS = ["announces", "official", "statement", "reports data", "files", "approves", "court", "lawmakers pass", "central bank"]

def _contains_any(text: str, words: list[str]) -> bool:
    return any(w in text for w in words)

def classify_category(title: str, summary: str = "") -> str:
    text = f"{title} {summary}".lower()
    scores = {}
    for category, words in CATEGORY_RULES.items():
        scores[category] = sum(1 for word in words if word in text)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"

def classify_importance(title: str, summary: str = "") -> str:
    text = f"{title} {summary}".lower()
    high_score = sum(1 for w in HIGH_WORDS if w in text)
    medium_score = sum(1 for w in MEDIUM_WORDS if w in text)
    if high_score >= 2:
        return "High"
    if high_score == 1 or medium_score >= 2:
        return "Medium"
    return "Low"

def detect_assets(title: str, summary: str = "") -> str:
    text = f"{title} {summary}".lower()
    assets = [asset for asset, words in ASSET_RULES.items() if _contains_any(text, words)]
    return ", ".join(assets) if assets else "Market"

def detect_certainty(title: str, summary: str = "") -> str:
    text = f"{title} {summary}".lower()
    if _contains_any(text, OFFICIAL_WORDS):
        return "공식/확정성 높음"
    if any(w in text for w in ["may", "could", "reportedly", "sources", "expected", "likely", "rumor"]):
        return "추측/관측성 높음"
    return "보도/관측"

def make_interpretation(title: str, category: str, assets: str, importance: str) -> str:
    base = {
        "crypto": "크립토 정책/수급 심리에 직접 연결될 수 있습니다. BTC·ETH와 거래소/ETF 관련 흐름을 같이 봐야 합니다.",
        "rates": "금리와 달러 기대를 흔드는 재료라 위험자산 전반의 밸류에이션에 영향을 줄 수 있습니다.",
        "oil": "유가 상승은 인플레 재가속 우려로 이어질 수 있어 금리인하 기대와 위험자산 심리에 부담이 될 수 있습니다.",
        "dollar": "달러 강세/약세는 원화, 원자재, 신흥국, 코인 유동성에 같이 영향을 줍니다.",
        "ai-semis": "AI·반도체 테마의 수급과 미국 성장주 심리에 연결될 수 있습니다.",
        "quantum": "양자컴퓨팅은 아직 기대감 비중이 큰 테마라 정책/실적/기술 검증 여부를 분리해서 봐야 합니다.",
        "korea": "한국장 수급과 원화, 반도체·수출주 흐름에 영향을 줄 수 있습니다.",
        "us-market": "미국 지수 방향성은 국내 성장주와 코인 위험선호에도 파급될 수 있습니다.",
        "general": "시장 전체 분위기 확인용 재료입니다. 단독 매매 근거보다는 다른 지표와 같이 봐야 합니다.",
    }.get(category, "시장 전체 분위기 확인용 재료입니다.")

    prefix = "중요도 높음: " if importance == "High" else ""
    return f"{prefix}{base} 관련 자산 태그: {assets}."
