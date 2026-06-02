# Deploy Checklist

## 1. 서버 준비

Ubuntu VPS 기준:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin nginx certbot python3-certbot-nginx git
```

## 2. 프로젝트 업로드

```bash
git clone <your-repo>
cd market_news_hub_fastapi
cp .env.example .env
nano .env
```

`SITE_URL`을 실제 도메인으로 바꿉니다.

## 3. Docker 실행

```bash
docker compose up -d --build
```

## 4. Nginx 연결

`nginx.conf.example` 참고해서 `/etc/nginx/sites-available/도메인`에 설정 후:

```bash
sudo ln -s /etc/nginx/sites-available/도메인 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 5. SSL

```bash
sudo certbot --nginx -d example.com -d www.example.com
```

## 6. 확인 주소

```text
https://example.com
https://example.com/robots.txt
https://example.com/sitemap.xml
```

## 7. Google Search Console

- 도메인 속성 추가
- DNS TXT 인증
- sitemap.xml 제출

## 8. AdSense

- privacy / terms / contact / about 페이지 확인
- 원문 복붙이 아니라 자체 해석 콘텐츠가 충분히 쌓였는지 확인
- 승인 후 `.env`에 `ADSENSE_CLIENT_ID` 입력
