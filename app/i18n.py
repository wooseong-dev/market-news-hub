SUPPORTED_LANGS = ["ko", "en"]
DEFAULT_LANG = "ko"

TRANSLATIONS = {
    "ko": {
        "news":"뉴스","rates":"금리","oil":"유가","crypto":"크립토","ai":"AI/반도체","guides":"가이드","about":"소개",
        "hero_title":"오늘 시장을 흔드는 뉴스만 빠르게 보기",
        "hero_desc":"금리, 유가, 달러, AI·반도체, 양자컴퓨팅, 크립토 정책, 한국장 영향 뉴스를 모아 변동성 관점으로 분류합니다.",
        "latest":"최신 뉴스","high":"High Impact Watch","view_all":"전체 보기 →","source":"원문","source_full":"원문 기사 보기",
        "categories":"카테고리","note":"주의","note_body":"이 사이트는 투자 조언이 아니라 시장 뉴스와 변동성 요인을 정리하는 정보 도구입니다.",
        "all_news":"뉴스 전체","search_placeholder":"검색어: oil, BTC, CPI, Nvidia...","all_categories":"전체 카테고리","all_importance":"전체 중요도","filter":"검색",
        "market_interpretation":"시장 해석","summary":"요약","related":"관련 뉴스","no_news":"뉴스가 없습니다.",
        "investment_notice":"투자 판단 주의","investment_notice_body":"이 페이지는 원문 뉴스와 키워드 기반 시장 해석을 함께 보여주는 정보 페이지입니다. 매수·매도 추천이 아닙니다.",
        "ad_slot":"Ad Slot","ad_desc":"애드센스 승인 후 광고 코드가 들어갈 자리.","language":"언어",
        "guides_title":"시장 해석 가이드","guides_desc":"뉴스를 단순히 소비하지 않고, 금리·유가·달러·정책·테마가 시장에 어떻게 연결되는지 정리합니다.","read":"읽기 →",
        "about1":"Market Risk Radar는 개인투자자가 시장을 보기 전 확인할 수 있는 변동성 뉴스 허브입니다.",
        "about2":"금리, 유가, 달러, AI·반도체, 양자컴퓨팅, 크립토 정책, 한국장 영향 같은 재료를 분류해 시장 배경을 빠르게 파악하는 것을 목표로 합니다.",
        "about3":"단순 매수 추천이 아니라 ‘왜 시장이 움직이는가’를 확인하는 도구입니다.",
        "privacy":"이 사이트는 기본적으로 회원가입을 요구하지 않습니다. 방문 통계 분석, 광고 표시, 보안 로그를 위해 쿠키 또는 익명화된 접속 정보가 사용될 수 있습니다.",
        "terms":"이 사이트의 정보는 투자 조언, 매수·매도 추천, 법률·세무 자문이 아닙니다. 뉴스와 시장 해석은 참고용이며 최종 투자 판단과 책임은 이용자 본인에게 있습니다.",
        "contact":"문의, 오류 제보, 제휴 관련 연락은 운영자 이메일을 통해 받을 수 있습니다. 운영자 이메일을 여기에 입력하세요: your-email@example.com",
    },
    "en": {
        "news":"News","rates":"Rates","oil":"Oil","crypto":"Crypto","ai":"AI/Semis","guides":"Guides","about":"About",
        "hero_title":"Track the news moving markets today",
        "hero_desc":"A market risk dashboard for rates, oil, dollar moves, AI and semiconductors, quantum computing, crypto policy, and Korea market impact.",
        "latest":"Latest News","high":"High Impact Watch","view_all":"View all →","source":"Source","source_full":"Read Original Article",
        "categories":"Categories","note":"Note","note_body":"This site is an information tool for market news and volatility factors, not investment advice.",
        "all_news":"All News","search_placeholder":"Search: oil, BTC, CPI, Nvidia...","all_categories":"All categories","all_importance":"All importance","filter":"Filter",
        "market_interpretation":"Market Interpretation","summary":"Summary","related":"Related News","no_news":"No news found.",
        "investment_notice":"Investment Notice","investment_notice_body":"This page provides source news and keyword-based market interpretation. It is not a buy or sell recommendation.",
        "ad_slot":"Ad Slot","ad_desc":"AdSense placement will appear here after approval.","language":"Language",
        "guides_title":"Market Interpretation Guides","guides_desc":"Evergreen guides explaining how rates, oil, the dollar, policy, and major themes connect to market volatility.","read":"Read →",
        "about1":"Market Risk Radar is a market volatility news hub for individual investors.",
        "about2":"It classifies key market drivers such as rates, oil, the dollar, AI and semiconductors, quantum computing, crypto policy, and Korea-related market news.",
        "about3":"The goal is not to give trading calls, but to help users understand why markets are moving.",
        "privacy":"This site does not require user registration by default. Cookies or anonymized access data may be used for analytics, advertising, and security logs.",
        "terms":"The information on this site is not investment advice, buy/sell recommendation, or legal/tax advice. News and interpretation are provided for reference only.",
        "contact":"For inquiries, bug reports, or partnerships, contact the operator. Add your email here: your-email@example.com",
    }
}

CATEGORY_LABELS = {
    "ko": {"general":"일반","us-market":"미국장","rates":"금리","oil":"유가","dollar":"달러","ai-semis":"AI/반도체","quantum":"양자컴퓨팅","crypto":"크립토","korea":"한국장"},
    "en": {"general":"General","us-market":"US Market","rates":"Rates","oil":"Oil","dollar":"Dollar","ai-semis":"AI/Semis","quantum":"Quantum","crypto":"Crypto","korea":"Korea"},
}

INTERP = {
    "ko": {
        "crypto":"크립토 정책/수급 심리에 직접 연결될 수 있습니다. BTC·ETH와 거래소/ETF 관련 흐름을 같이 봐야 합니다.",
        "rates":"금리와 달러 기대를 흔드는 재료라 위험자산 전반의 밸류에이션에 영향을 줄 수 있습니다.",
        "oil":"유가 상승은 인플레 재가속 우려로 이어질 수 있어 금리인하 기대와 위험자산 심리에 부담이 될 수 있습니다.",
        "dollar":"달러 강세/약세는 원화, 원자재, 신흥국, 코인 유동성에 같이 영향을 줍니다.",
        "ai-semis":"AI·반도체 테마의 수급과 미국 성장주 심리에 연결될 수 있습니다.",
        "quantum":"양자컴퓨팅은 아직 기대감 비중이 큰 테마라 정책/실적/기술 검증 여부를 분리해서 봐야 합니다.",
        "korea":"한국장 수급과 원화, 반도체·수출주 흐름에 영향을 줄 수 있습니다.",
        "us-market":"미국 지수 방향성은 국내 성장주와 코인 위험선호에도 파급될 수 있습니다.",
        "general":"시장 전체 분위기 확인용 재료입니다. 단독 매매 근거보다는 다른 지표와 같이 봐야 합니다.",
    },
    "en": {
        "crypto":"This can directly affect crypto policy expectations, liquidity, and sentiment. Watch BTC, ETH, exchanges, and ETF-related flows together.",
        "rates":"This can reshape expectations for interest rates and the dollar, affecting valuations across risk assets.",
        "oil":"Higher oil prices can revive inflation concerns, potentially weighing on rate-cut expectations and risk appetite.",
        "dollar":"Dollar strength or weakness can affect FX, commodities, emerging markets, and crypto liquidity.",
        "ai-semis":"This can influence AI and semiconductor flows, as well as sentiment toward US growth stocks.",
        "quantum":"Quantum computing remains a theme with heavy expectation risk. Separate policy, earnings, and technical validation.",
        "korea":"This may affect Korea market flows, the won, semiconductors, and export-sensitive stocks.",
        "us-market":"US index direction can spill over into Korea growth stocks and crypto risk appetite.",
        "general":"This is a broad market context item. Treat it as background rather than a standalone trading signal.",
    }
}

GUIDES = {
    "ko": [
        {"slug":"fomc-cpi-market-impact","title":"FOMC와 CPI가 나스닥·코인에 미치는 영향","description":"금리 기대와 인플레이션 지표가 왜 성장주와 위험자산을 흔드는지 정리합니다.","body":["FOMC와 CPI는 시장이 앞으로의 금리 경로를 다시 가격에 반영하게 만드는 핵심 이벤트입니다.","CPI가 예상보다 높으면 금리 인하 기대가 약해지고, 달러와 금리가 강해지면서 나스닥·코인 같은 위험자산에는 부담이 될 수 있습니다.","반대로 물가 둔화가 확인되면 할인율 부담이 낮아져 성장주와 위험자산 심리가 개선될 수 있습니다."]},
        {"slug":"oil-inflation-rates","title":"유가 상승은 왜 증시와 코인에 부담이 될까?","description":"유가, 인플레이션, 금리 기대, 위험자산 심리의 연결고리를 봅니다.","body":["유가는 물가와 기업 비용에 동시에 영향을 주는 대표적인 매크로 변수입니다.","유가가 빠르게 오르면 시장은 인플레이션 재가속 가능성을 의식하고, 이는 금리 인하 기대를 낮출 수 있습니다.","금리 기대가 높아지면 성장주와 코인처럼 유동성에 민감한 자산은 단기 부담을 받을 수 있습니다."]},
        {"slug":"crypto-policy-sec-cftc","title":"SEC·CFTC 정책 뉴스는 크립토 시장에 왜 중요할까?","description":"규제 명확성, 기관 진입, ETF 기대가 BTC·ETH에 미치는 영향을 설명합니다.","body":["크립토 시장은 기술 자체뿐 아니라 제도권 편입 기대에 크게 반응합니다.","SEC와 CFTC의 역할 구분, ETF 승인, 스테이블코인 법안, 거래소 규제는 기관 자금의 진입 가능성과 연결됩니다.","정책 뉴스는 확정 발표인지, 법안 통과 전 단계인지, 단순 보도인지 구분하는 것이 중요합니다."]},
        {"slug":"ai-semiconductor-cycle","title":"AI 반도체 뉴스가 나스닥을 움직이는 이유","description":"AI 투자 사이클, 데이터센터, GPU 수요가 성장주 심리에 미치는 영향을 봅니다.","body":["AI와 반도체는 최근 미국 성장주 수급의 핵심 축입니다.","GPU, 데이터센터, 클라우드 투자, 전력 인프라 뉴스는 단순 기업 뉴스가 아니라 나스닥 전체 심리와 연결될 수 있습니다.","AI 뉴스는 기술 기대와 실제 매출 성장, 밸류에이션 부담을 분리해서 보는 것이 좋습니다."]},
    ],
    "en": [
        {"slug":"fomc-cpi-market-impact","title":"How FOMC and CPI Move Nasdaq and Crypto","description":"Why rate expectations and inflation data can move growth stocks and risk assets.","body":["FOMC meetings and CPI releases force markets to reprice the expected path of interest rates.","When CPI comes in hotter than expected, rate-cut expectations can weaken, pushing yields and the dollar higher. That can pressure Nasdaq and crypto.","When inflation cools, discount-rate pressure may ease, improving sentiment toward growth stocks and risk assets."]},
        {"slug":"oil-inflation-rates","title":"Why Higher Oil Prices Can Pressure Stocks and Crypto","description":"The link between oil, inflation, rate expectations, and risk appetite.","body":["Oil is a key macro variable because it affects both inflation and corporate costs.","When oil rises quickly, markets may worry about renewed inflation pressure, which can reduce rate-cut expectations.","Higher rate expectations can weigh on assets that are sensitive to liquidity and future growth, including growth stocks and crypto."]},
        {"slug":"crypto-policy-sec-cftc","title":"Why SEC and CFTC Policy News Matters for Crypto","description":"How regulatory clarity, institutional access, and ETF expectations affect BTC and ETH.","body":["Crypto markets react not only to technology, but also to expectations of institutional adoption.","SEC/CFTC jurisdiction, ETF approvals, stablecoin rules, and exchange regulation all influence whether large institutions can participate more easily.","Always separate confirmed policy decisions from draft bills, negotiations, and media reports."]},
        {"slug":"ai-semiconductor-cycle","title":"Why AI Semiconductor News Moves Nasdaq","description":"How AI capex, data centers, and GPU demand shape growth-stock sentiment.","body":["AI and semiconductors have become major drivers of US growth-stock flows.","GPU demand, data-center spending, cloud capex, and power-infrastructure news can affect broader Nasdaq sentiment.","AI headlines should be read by separating technical excitement, actual revenue growth, and valuation pressure."]},
    ],
}

def lang_of_path(path):
    return "en" if path == "/en" or path.startswith("/en/") else "ko"

def tx(lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG])

def cat_label(category, lang):
    return CATEGORY_LABELS.get(lang, CATEGORY_LABELS[DEFAULT_LANG]).get(category, category)

def interp_item(item, lang):
    category = getattr(item, "category", "general")
    importance = getattr(item, "importance", "")
    assets = getattr(item, "assets", "Market")
    prefix = "중요도 높음: " if lang == "ko" and importance == "High" else "High impact: " if lang == "en" and importance == "High" else ""
    tail = f" 관련 자산 태그: {assets}." if lang == "ko" else f" Related asset tags: {assets}."
    return prefix + INTERP.get(lang, INTERP[DEFAULT_LANG]).get(category, INTERP[lang]["general"]) + tail

def localize(path, lang):
    if lang == "en":
        return "/en" if path == "/" else "/en" + path
    return path

def alt_paths(path):
    if path == "/en":
        return {"ko":"/", "en":"/en"}
    if path.startswith("/en/"):
        return {"ko":path[3:] or "/", "en":path}
    return {"ko":path, "en":"/en" if path == "/" else "/en" + path}
