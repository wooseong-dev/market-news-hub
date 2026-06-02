# Market News Hub FastAPI

구글 색인, 실제 운영, 애드센스 삽입까지 고려한 시장 뉴스 허브 MVP입니다.

핵심 컨셉은 단순 뉴스 복붙 사이트가 아니라 **시장 변동성 해석판**입니다.

## 기능

- FastAPI + Jinja2 웹사이트
- SQLite 저장
- RSS/Google News RSS 수집
- 카테고리 자동 분류
- 관련 자산 태그 자동 생성
- 중요도/확정성 태그
- 기사별 개별 URL 생성
- robots.txt
- sitemap.xml
- privacy / terms / contact / about 페이지
- 애드센스 코드 삽입 위치 준비
- Docker 배포 준비
- 수동 새로고침 엔드포인트 `/admin/refresh?key=...`

## 로컬 실행

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/init_db.py
uvicorn app.main:app --reload
```

브라우저에서:

```text
http://127.0.0.1:8000
```

## 운영용 실행

```bash
docker compose up -d --build
```

## 환경 변수

`.env.example`을 `.env`로 복사해서 수정하세요.

```env
SITE_NAME=Market Risk Radar
SITE_URL=https://example.com
DATABASE_URL=sqlite:///./data/news.db
ADMIN_REFRESH_KEY=change-me
ADSENSE_CLIENT_ID=
GA_MEASUREMENT_ID=
```

애드센스 승인 전에는 `ADSENSE_CLIENT_ID`를 비워두면 광고 영역만 자리표시자로 표시됩니다.

## 구글 등록 기본 순서

1. 도메인 구매
2. VPS 또는 클라우드 서버에 배포
3. `SITE_URL`을 실제 도메인으로 변경
4. `/robots.txt` 확인
5. `/sitemap.xml` 확인
6. Google Search Console에 도메인 등록
7. sitemap 제출
8. 콘텐츠가 충분히 쌓이면 AdSense 신청

## 주의

RSS 뉴스 원문 전체를 복사하지 마세요. 이 프로젝트는 제목, 짧은 요약, 원문 링크, 자체 해석 태그 중심으로 구성되어 있습니다.
광고 수익화를 노릴수록 직접 작성한 시장 해석/가이드/설명 콘텐츠 비중을 늘려야 합니다.
