# 작업 기록

## 2026-10-08

- 완료 단계: 1 보존, 2 GitHub 대조, 3 환경 관측
- 현재 브랜치: docs/closeout-baseline
- 시작 기준 커밋: 0962ab1db1f19bec501ad31a32e9909616888965
- 검사: 로컬 main과 origin/main의 파일 차이 없음. Git 2.54.0.windows.1, Python 3.13.14, Docker Desktop 4.90.0, Engine 29.7.2, Compose v5.5.1. nginx가 127.0.0.1:8080에 연결되고 관리자 로그인을 확인함.
- 화면 표시 버전: 7.1.3-ed9434c4.docker
- 남은 작업: 환경 기록 푸시와 PR 병합 후 4단계 법령·출처 확인

## 2026-10-08 4단계

- 완료: 환경 기록은 main `2553ae2`에 병합됨. 시행일 정정, 적용 조문, 안전성 확보조치 기준 제5조·제6조의 확인 범위를 기록함.
- 이번 기록: ISMS-P 인증기준 안내서(2023.11, 게시 2023-11-23)를 S-L05와 CT-F01·CT-F02·CT-F03에 참고 연결함. 인증심사가 아니며 점검 판정은 바꾸지 않음.
- 이번 기록: ISO/IEC 27701:2025 제2판(발행 2025-10-14, 64쪽)의 공개 서지정보를 S-L06에 기록함. 표준 본문은 보지 않았고 조항 연결과 충족은 쓰지 않음.
- 현재 브랜치: docs/closeout-controls
- 남은 작업: 주통기 범위, 처리방침 안내서

## 2026-10-12 4단계

- 이번 기록: KISA 주요정보통신기반시설 기술적 취약점 분석·평가 방법 상세가이드(게시 2025-12-24)를 S-L07에 기록함. 정보통신기반 보호법 제9조의 관리기관 업무이며, 이번 실습의 직접 기술 범위가 아님. 점검 판정은 바꾸지 않음.
- 이번 기록: 개인정보 처리방침 작성지침의 문서 종류는 작성지침, 개정판은 2026.4.이며 작성일은 2026-04-23이다. S-L04와 워크북에 기록함. 기존 확인일 2026-09-21은 이력으로 유지함. 초기 02문서의 보유·위탁·권리는 불충분하며 점검 판정은 바꾸지 않음.
- 워크북 날짜: S-L04 공포발표일을 2026-04-23으로, S-L05 공포발표일을 2023-11-23으로 sources.csv와 맞춤.
- 이번 기록: S-L01부터 S-L07의 문서유형과 개정판을 sources.csv와 워크북 Sources에 같은 값으로 채움. S-L02 개정판은 대통령령 제36671호. 점검 판정은 바꾸지 않음.
- 현재 브랜치: docs/closeout-controls

## 2026-10-12 5단계

- 이번 기록: private-evidence 21개 파일의 SHA256을 docs/evidence-hashes.md에 기록함. 원본 PNG·JSON·jy-doc02-copy.txt는 Git에 넣지 않음.
- 대조: users-before.json과 users-after-f01.json은 기존 .sha256 파일과 값이 같음. users-diff.json은 수집기에 diff 명령이 없어 옆자리 해시 파일이 없음.
- 이번 기록: 2026-10-06 재점검 범위를 docs/retest-scope.md에 적음. R-01·R-02a·R-02b는 적합이고 E02는 T01·T11 삭제 범위만 적합이다. R-03·T12·사본·백업은 재점검 완료가 아니다. Checks 판정은 바꾸지 않음.
- 이번 기록: 관측된 티켓만 docs/ticket-inventory.md에 적음. T02=3/52003, T11 시험본=29/52028(삭제), T12=14/52014(유지), T15=17/52017(보존). T03~T10·T13·T14는 공란. 오늘 Zammad를 다시 조회하지 않음.
- 이번 기록: 위험·조치·운영 상태를 docs/operations-status.md에 적음. F-01은 6, F-02a·F-02b는 9, F-03 잔여는 9. CR-01~03은 완료, CR-04와 A-03은 예정. EX-01~EX-09는 유효. 로컬 사본은 해시만 기록하고 파기하지 않음.
- 현재 브랜치: docs/closeout-controls
- 남은 작업: 수집기 부록

## 2026-10-12 9단계

- 이번 기록: 수집기 부록을 `docs/collector-appendix.md`에 적음. 실습 JSON을 만든 도구는 `tools/jy_evidence.py`이며 명령은 `collect`와 `hash`다. `diff` 명령은 없다. `collector/`는 0.0.0 골격이다. 오늘 수집기와 테스트를 다시 실행하지 않았고 Checks 판정은 바꾸지 않음.
- 현재 브랜치: fix/evidence-validation
- 남은 작업: CI 확장

## 2026-10-12 10단계

- 이번 기록: `collector/tests/test_evidence_register.py`를 추가함. 공개 해시 목록 21개, 실습 JSON 경로, 토큰 문자열이 없는지를 확인한다. 비공개 증적과 Zammad는 열지 않음.
- 로컬 검사: `.venv`의 Python 3.13.14, pytest 8.4.2로 `collector/tests`와 `tools/test_jy_evidence.py`를 실행해 12 passed.
- CI: `.github/workflows/quality.yml`의 테스트 단계가 같은 두 경로를 실행하도록 바꿈. GitHub Actions 결과는 이 브랜치의 풀 리퀘스트에서 확인한다.
- 현재 브랜치: fix/evidence-validation
- 남은 작업: 이 브랜치의 풀 리퀘스트

## 2026-10-13 11단계

- 이번 기록: 산출물 상태를 `docs/deliverable-status.md`에 적음. 사고 도상훈련 JY-INC-2026-01, 모의 통지문, AI 미연결, 처리방침 초안은 2026-10-07 문서 그대로다. B04·E04는 미확인이고 F02·B02는 미흡, F03은 적용 제외로 남긴다. 오늘 메일·재시험·게시는 하지 않음.
- 현재 브랜치: docs/closeout-deliverables
- 남은 작업: 보고서와 PPT

## 2026-10-13 12단계

- 이번 기록: 보고서·발표자료 상태를 `docs/report-pack-status.md`에 적음. 원고는 `docs/18-final-report.md`(JY-FINAL-2026-10)와 `docs/18-slides.md`다. `reports/`에 docx, pdf, pptx, 워크북이 있다. `reports/final/`은 `.gitkeep`만 있다. 오늘 파일을 다시 만들거나 열지 않았고 Checks 판정은 바꾸지 않음.
- 현재 브랜치: docs/closeout-deliverables
- 남은 작업: 이 브랜치의 풀 리퀘스트

## 2026-10-13 13단계

- 이번 기록: 인수인계 상태를 `docs/handover-status.md`에 적음. 기준 커밋은 main `2b724e8`이다. START_HERE와 README의 2026-10-07 문장은 덮어쓰지 않음. `down -v`, T12·T15·조직 삭제, 원본 증적 커밋, Checks 판정 변경은 하지 않음.
- 현재 브랜치: docs/closeout-handover
- 남은 작업: 비밀 검사

## 2026-10-13 14단계

- 이번 기록: 비밀 검사를 `docs/secret-review.md`에 적음. `.env`와 `private-evidence`는 Git 추적 목록에 없다. `ZAMMAD_TOKEN=`, 개인 키 시작 문장, `ghp_`, `github_pat_`는 현재 추적 파일에서 찾지 못했다. 로컬 Gitleaks는 실행하지 않음. 풀 리퀘스트 #6의 secret-scan은 통과 기록만 인용함.
- 현재 브랜치: docs/closeout-handover
- 남은 작업: 이 브랜치의 풀 리퀘스트