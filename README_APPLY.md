# Market News Hub UI Patch

최신 뉴스 카드에 대표 썸네일 느낌의 카테고리 박스와 보기 좋은 태그 배지를 추가하는 패치입니다.

## 적용 순서

1. `app/main.py`에 `main_additions.py` 내용을 붙여넣기
2. `templates/index.html`을 이 패치의 `templates/index.html`로 교체
3. `templates/news_list.html`을 이 패치의 `templates/news_list.html`로 교체
4. `static/styles.css` 맨 아래에 `styles_append.css` 내용을 붙여넣기
5. 로컬 테스트
6. git push

## 로컬 테스트

```bash
PYTHONPATH=. uvicorn app.main:app --reload
```

확인:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/en
http://127.0.0.1:8000/news
http://127.0.0.1:8000/en/news
```

## 배포

```bash
git add .
git commit -m "Improve news cards and tag UI"
git push
```
