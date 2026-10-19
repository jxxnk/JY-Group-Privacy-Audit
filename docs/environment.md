# 실습 환경

작성일: 2026-10-07
최종 관측일: 2026-10-19
수행자: 김준영

## 경로

| 구분 | 경로 |
| --- | --- |
| 프로젝트 Git | `C:\JY-Lab\JY-Group-Privacy-Audit` |
| GitHub | `https://github.com/jxxnk/JY-Group-Privacy-Audit.git` |
| 2026-10-07 기록 | `feat/linux-evidence-collector`에서 작성. 이 문장은 현재 작업 지시가 아님 |
| 2026-10-08 확인 | `main`이 `origin/main`과 일치. 이 수정은 `docs/closeout-baseline`에서 수행 |
| 2026-10-14 확인 | `docs/closeout-baseline-02`. 버전 숫자는 아래 2026-10-08 표와 같음 |
| 2026-10-19 확인 | `docs/closeout-deliverables-02`. 기준 commit `06d6ff5`. main 머지 전이며 최종 tag 없음 |
| Zammad compose | `C:\JY-Lab\zammad-runtime` (공식 zammad-docker-compose) |
| 증적 원본 | `C:\JY-Lab\private-evidence\` (Git 제외) |
| 가이드 PDF | `C:\JY-Lab\reference\` |

## 접속

- URL: `http://127.0.0.1:8080` (주소창. 검색창에 넣지 않음)
- UI: 한국어
- 관리자: `admin@jy.example.test` (AJ)
- 티켓 줌: 내부 id. 예: T12 → `http://127.0.0.1:8080/#ticket/zoom/14`
- Ticket# 예: T02 `#52003`, T12 `#52014`. 번호로 줌하면 “찾을 수 없음”

## 계정 (합성)

S01 admin@jy.example.test · S02 privacy@jy.example.test · S03 lead@service.example.test
S04 agent@service.example.test · S05 former@service.example.test (종료 2026-09-14, Active=false)
S06 maint@vendor.example.test
그룹: JY-General, JY-Restricted. 조직: JY-Lab-Customers (공유=아니오)

## 수집기

`tools/jy_evidence.py`는 `127.0.0.1:8080` GET만 사용한다. 토큰은 화면에 한 번만 보이는 값이며 `.env`에 커밋하지 않는다. 이 도구에는 `diff` 서브커맨드가 없다. 전후 JSON 비교는 동일 staff.csv, 동일 Zammad 인스턴스, 동일 직원 ID를 기준으로 수동 검증했고, `users-diff.json`에는 S05 active True→False만 기록되어 있다. 그 파일은 `private-evidence/after`에만 둔다. 현재 저장소 도구에는 원 가이드 부록의 전체 diff 방어 기능이 없으므로 자동화 전체 구현 완료로 주장하지 않는다.

## 2026-10-08 보완 시점 관측

아래 값은 2026-10-08에 직접 확인한 상태다. 2026-10-06 실습 당시 버전을 소급해서 증명하지 않는다. 2026-10-14에 다시 본 Git, Python, Docker, Compose, compose 커밋, Zammad 이미지 태그와 ID도 이 표와 같았다.

| 항목 | 관측값 |
| --- | --- |
| OS | Windows |
| Git | 2.54.0.windows.1 |
| Python | 3.13.14 |
| Docker Desktop | 4.90.0 (238679) |
| Docker Engine | 29.7.2 |
| Compose | v5.5.1 |
| compose commit | `27944f87aed91420242dfa97038ff96555d7cbe7` |
| Zammad 이미지 | `ghcr.io/zammad/zammad:7.1.3-0011` |
| Zammad 이미지 ID | `e65123a43ecc` |
| 화면 표시 버전 | `7.1.3-ed9434c4.docker` |
| 접속 바인딩 | `127.0.0.1:8080->8080/tcp` |
| Elasticsearch | 9.5.3, `78728a98651e` |
| Memcached | 1.6.45-alpine, `c29847751abb` |
| PostgreSQL | 17.11-alpine, `18cfe3ef5e68` |
| Redis | 8.10.1-alpine, `becdda6c7f4b` |

2026-10-08 실행 상태에서는 Memcached, PostgreSQL, Rails, Redis가 `healthy`였고 nginx는 포트가 연결된 `Up` 상태였다. 관리자 로그인과 관리 영역의 버전 화면을 확인했다. `zammad-runtime`에는 미추적 파일 `tmp-set-group.rb`가 있다. 이 파일은 감사 저장소에 포함하지 않는다.

보존 파일 `ENV-01-version.txt`와 `ENV-02-local-port.txt`의 이미지 ID와 포트는 2026-10-08 조회 결과와 같다. 두 파일에는 달력 날짜가 없고 상대 시간만 있으므로, 그 상대 시간을 특정 날짜로 바꾸지 않는다.

## 2026-10-14 관측

버전 숫자는 위 표에만 둔다. Docker Desktop을 켜기 전에는 엔진 파이프가 없어 `docker version`이 실패했다. 엔진이 준비된 뒤 다시 확인했다. `docker compose up`과 `docker compose down -v`는 실행하지 않았다.

| 항목 | 관측값 |
| --- | --- |
| 엔진 첫 시도 | 파이프 없음. `docker version` 실패 |
| 컨테이너 생성 | 4주 전 |
| 관측 시 상태 | `Up 2 minutes` |
| healthy | Memcached, PostgreSQL, Rails, Redis |
| Up | nginx, backup, Elasticsearch, scheduler, websocket |
| nginx 바인딩 | `127.0.0.1:8080->8080/tcp` |
| 로그인 화면 | `http://127.0.0.1:8080/#login`에서 열림 |
| 로그인 화면 버전 | 없음. 하단은 Powered by Zammad |
| 관리 영역 버전 | `7.1.3-ed9434c4.docker`는 2026-10-08에만 확인 |
| `tmp-set-group.rb` | 미추적. 이 날 실행하지 않음. 감사 저장소에 넣지 않음 |

## 2026-10-19 관측

Windows 버전과 WSL 상태를 새로 확인했다. Git, Python, Docker Engine, Compose, compose commit은 2026-10-08 표와 같았다. Docker Desktop 엔진이 중지되어 이미지 태그와 컨테이너 상태는 오늘 다시 확인하지 못했다. `docker compose up`과 `docker compose down -v`는 실행하지 않았다. winver 창의 메일 주소는 기록하지 않았다.

| 항목 | 관측값 |
| --- | --- |
| Windows | Windows 11 Home, 버전 25H2 (OS 빌드 26200.9711) |
| Git | 2.54.0.windows.1 |
| Python | 3.13.14 |
| Docker Engine | 29.7.2, build a7dcaa6 |
| Compose | v5.5.1 |
| WSL | Ubuntu Stopped 2, docker-desktop Stopped 2 |
| compose commit | `27944f87aed91420242dfa97038ff96555d7cbe7` |
| Zammad 이미지 | 미확인. `docker compose images`가 엔진 파이프 연결에 실패 |
| URL | `http://127.0.0.1:8080` |
| UI 언어 | 한국어 |
| 브랜치 | `docs/closeout-deliverables-02` |
| 기준 commit | `06d6ff5`. main 머지 전 |
| 최종 tag | 없음 |