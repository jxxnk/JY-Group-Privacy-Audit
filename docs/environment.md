# 실습 환경

작성일: 2026-10-07
수행자: 김준영

## 경로

| 구분 | 경로 |
| --- | --- |
| 프로젝트 Git | `C:\JY-Lab\JY-Group-Privacy-Audit` |
| GitHub | `https://github.com/jxxnk/JY-Group-Privacy-Audit.git` |
| 브랜치 | `feat/linux-evidence-collector` (새 브랜치 만들지 않음) |
| Zammad compose | `C:\JY-Lab\zammad-runtime` (공식 zammad-docker-compose) |
| 증적 원본 | `C:\JY-Lab\private-evidence\` (Git 제외) |
| 가이드 PDF | `C:\JY-Lab\reference\` |

## 접속

- URL: `http://127.0.0.1:8080` (주소창. 검색창에 넣지 않음)
- UI: 한국어
- 관리자: `admin@jy.example.test` (AJ)
- 티켓 줌: 내부 id. 예: T12 → `http://127.0.0.1:8080/#ticket/zoom/14`
- Ticket# 예: T02 `#52003`, T12 `#52014`. 번호로 줌하면 “찾을 수 없음”

## Zammad 시작 (다음날)

Docker Desktop Engine 실행 후:

```powershell
Set-Location C:\JY-Lab\zammad-runtime
docker compose ps
docker compose start
docker compose ps
```

nginx/railsserver가 healthy일 때까지 기다린 뒤 브라우저. **금지:** `docker compose down -v`

## 계정 (합성)

S01 admin@jy.example.test · S02 privacy@jy.example.test · S03 lead@service.example.test  
S04 agent@service.example.test · S05 former@service.example.test (종료 2026-09-14, Active=false)  
S06 maint@vendor.example.test  
그룹: JY-General, JY-Restricted. 조직: JY-Lab-Customers (공유=아니오)

## 수집기

`tools/jy_evidence.py` — `127.0.0.1:8080` GET만. 토큰은 화면에 한 번만 보이는 값. `.env` 커밋 금지. `diff` 서브커맨드는 없음. `users-diff.json`은 private-evidence/after에만.
