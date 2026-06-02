# Multilingual Update Patch

이 패치는 Market News Hub에 한국어/영어 다국어 구조를 추가합니다.

## 추가 기능

- `/` 한국어 메인
- `/en` 영어 메인
- `/news`, `/en/news`
- `/article/{slug}`, `/en/article/{slug}`
- `/guides`, `/en/guides`
- 언어 전환 버튼
- `hreflang` 태그
- sitemap에 한국어/영어 URL 포함
- 시장 해석 가이드 4개 한국어/영어 샘플 추가

## 적용 방법

기존 `market_news_hub_fastapi` Git 저장소 폴더에 압축 안의 파일들을 덮어씁니다.

단, `templates/base.html` 안의 Google Search Console 인증 태그는 기존 실제 토큰으로 유지하세요.

```html
<meta name="google-site-verification" content="REPLACE_WITH_YOUR_GOOGLE_SEARCH_CONSOLE_TOKEN">
```

`static/styles.css.append` 안의 내용은 기존 `static/styles.css` 맨 아래에 붙여넣으세요.
그 뒤 `static/styles.css.append` 파일은 삭제해도 됩니다.

## 배포

```bash
git add .
git commit -m "Add multilingual support"
git push
```

Render가 자동 재배포합니다.

## 확인 주소

```text
https://market-news-hub.onrender.com/
https://market-news-hub.onrender.com/en
https://market-news-hub.onrender.com/guides
https://market-news-hub.onrender.com/en/guides
https://market-news-hub.onrender.com/sitemap.xml
```
