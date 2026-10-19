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

## 2026-10-14 0~2단계

- 기준 커밋: `35b7b85`. 태그 `v1.0-final`은 그대로 둠. `0962ab1`로 되돌리지 않음.
- 현재 브랜치: `docs/closeout-baseline-02`. 원격 추적 브랜치는 아직 없음.
- 보존: `C:\JY-Backup\2026-10-14`. 워크북, `users-before.json`, `users-after-f01.json`, `users-diff.json`, `jy-doc02-copy.txt` 해시는 MATCH. 사본의 파일 수와 열람 여부는 이 기록에 없음.
- 공유: Drive 원본 폴더의 접근 제한은 하지 않음. 제출은 차단. 비밀값은 적지 않음.
- 문서: 기존 9개 문서에 현재 기준 문장을 넣음. ADR-015는 `docs/DECISION_LOG.md`에 있음. 점검 판정은 바꾸지 않음.
- 3단계: 오늘 Docker와 Zammad를 다시 보지 않음. 2026-10-08 버전을 오늘 관측으로 바꾸지 않음.
- 다음: 보존 기록, 대조 기록, 요구대장을 새 파일로 저장한 뒤 `git status`와 `git diff --stat`을 확인한다. 커밋 번호는 커밋 뒤에 적는다.

## 2026-10-14 3단계

- 검사: Git 2.54.0.windows.1, Python 3.13.14. Docker Desktop 4.90.0, Engine 29.7.2, Compose v5.5.1. 엔진이 꺼져 있을 때 첫 `docker version`은 실패했고, Desktop을 켠 뒤 성공했다.
- Zammad: `C:\JY-Lab\zammad-runtime` 커밋 `27944f87`. 컨테이너는 4주 전 생성이고 관측 시 `Up 2 minutes`. nginx는 `127.0.0.1:8080`. 이미지는 `ghcr.io/zammad/zammad:7.1.3-0011`, ID `e65123a43ecc`.
- 화면: `http://127.0.0.1:8080/#login` 로그인 화면은 열림. 버전 문자열은 없음. 2026-10-08 관리 영역 버전은 오늘 다시 열지 않음.
- `tmp-set-group.rb`는 미추적. 실행하지 않았고 Git에 넣지 않음. `up`과 `down -v`는 하지 않음.
- 현재 브랜치: `docs/closeout-baseline-02`
- 다음: 이 관측을 커밋한 뒤 기준선 풀 리퀘스트를 연다.

## 2026-10-14 4단계

- 법률·시행령·고시 머리글은 2026-10-08과 같음. 조문 재독은 아님. 입법예고안 표시는 적용 판을 바꾸지 않음.
- ISMS-P 19번: 인증기준 안내서(2023.11) 수정게시, 2023-11-23. 2.5.1 87쪽, 2.6.3 105쪽, 3.4.1 240쪽.
- S-L04 시행일에서 게시일 2026-04-23을 뺌. S-L04 확인일 2026-09-21은 유지.
- Controls D2:D4와 docs/check-control-mapping.csv를 채움. Checks 판정은 바꾸지 않음.
- 현재 브랜치: docs/closeout-controls-02
- 다음: 증적 해시. 커밋 번호는 커밋 뒤에 적음.

## 2026-10-14 5단계 해시

- 4단계 커밋은 `271a9b6`. 푸시하지 않음.
- users-before.json, users-after-f01.json, users-diff.json, jy-doc02-copy.txt, ENV-01-system-base.png, ENV-01-version.txt, ENV-02-local-port.txt는 2026-10-12 해시와 같음.
- docs/data-flow.pdf SHA256은 d94f7cb9cf1191f79a34df5c13061239aa5fdb0f884ada71483c7743c69f023f. 이전 목록에 없었음.
- Evidence H2:H5를 보완 시점 계산으로 채움. 판정은 바꾸지 않음.
- 현재 브랜치: docs/closeout-controls-02
- 다음: 공개 가공본. 커밋 번호는 커밋 뒤에 적음.

## 2026-10-15 5단계 가공본

- 공개 캡처 10장을 evidence/sanitized에 넣음. 해시는 2026-10-12 원본과 같음.
- Evidence G열에 공개경로 또는 공개 제외 이유를 넣음. J~N열을 추가함.
- JSON-F01-B 수집시각은 2026-09-26 15:40:14 KST, JSON-F01-A는 2026-10-06 10:54:56 KST. DIFF 생성시각은 미기록.
- 원본 JSON과 비공개 화면은 Git에 넣지 않음. 판정은 바꾸지 않음.
- 현재 브랜치: docs/closeout-controls-02
- 다음: 직원ID·active 요약. 커밋 번호는 커밋 뒤에 적음.

## 2026-10-15 계정 active 요약

- 전후 JSON의 login과 active만 확인. 이메일은 공개 요약에 넣지 않음.
- Accounts와 대조하면 변경은 S05뿐. true에서 false.
- 파일: evidence/sanitized/users-active.csv
- 현재 브랜치: docs/closeout-controls-02
- 다음: 재점검 한계. 커밋 번호는 커밋 뒤에 적음.

## 2026-10-15 6단계 재점검 한계

Retest 판정은 유지하고 잔여위험에 한계 문장을 붙였다. A-03 기한은 2026-10-06 그대로 두고 상태를 기한 경과/미완료로 바꿨다. 새 실험은 없다. T12·T15는 삭제하지 않았다.

## 2026-10-15 7단계 티켓 목록

docs/ticket-inventory.csv를 추가했다. T02 #52020과 #52003, T12 #52029와 #52014를 다른 행으로 뒀다. #52020의 내부ID는 미확인이다. tickets.csv는 그대로 뒀다. 티켓은 삭제하지 않았다.

## 2026-10-15 8단계 위험 척도

14장을 현재 척도로 다시 썼다. F-01 전 화면은 T02 #52020이다. Findings 위험점수 3은 유지했다. F-02a와 F-02b 초기 점수는 6, 우선순위는 계획이다. F-03 초기와 잔여는 9, 우선이다. A-03은 기한 경과/미완료다.

## 2026-10-15 8단계 예외대장

14장 예외대장을 다시 썼다. EX-04는 시험보존이다. EX-03과 EX-09는 같은 T12 계획이다. 위험수용으로 연 예외는 없다. 다음 재검토일과 만료일은 미정이다.

## 2026-10-15 8단계 변경요청

14장 변경요청서를 다시 썼다. CR-01부터 CR-03의 즉시조치는 완료다. 근본조치는 미완료이고 새 기한은 미정이다. CR-04는 기한 2026-10-06 경과, 미완료다. 삭제를 승인하지 않았다.

## 2026-10-15 8단계 처리방침 초안

15장 처리방침 초안을 다시 썼다. 대외 문안에서 티켓 번호, 예외 번호, 로컬 경로를 빼 내부 검토로 옮겼다. B02는 미흡, B04는 미확인으로 남겼다. 보유 기간 숫자는 만들지 않았다.

## 2026-10-15 8단계 수탁 점검표

15장 수탁 점검표를 다시 썼다. 계약 검토와 2026-10-06 권한 확인을 나눴다. 계약서와 연간 실적은 없다. B03, D01, D02는 미흡으로 남겼다. 한시 권한은 양식만 있고 실행하지 않았다.

## 2026-10-15 8단계 교육 1장

15장 교육 1장을 다시 썼다. 본문은 계정, 기입, 사본, 권리 전달, 사고 창구다. Docker, Git, 티켓 주소는 부록으로 옮겼다. 서명과 출석은 없다. D04는 미흡으로 남겼다.

## 2026-10-15 8단계 30/90 계획

15장 30/90 계획을 다시 썼다. 16장 훈련, 17장 자기재검토, 18장 보고서 초안은 문서 작성으로 고쳤다. 교육 이수, 정기 권한 점검, 백업 시험은 예정 또는 미확인으로 남겼다. T12 파기는 기한 경과, 미완료다.

## 2026-10-15 8단계 처리 현황

워크북 Processing 시트를 고쳤다. 종료조건, 보존사유, 기산점, 필요기간, 파기 책임, 예외를 넣었다. P-04는 실습 증적이다. 기간 숫자는 없다. E01은 미흡이다. 다른 시트는 바꾸지 않았다.

## 2026-10-16 8단계 위험척도 ADR

ADR-016을 추가했다. 위험점수는 가능성 1–3 × 영향 1–3이고, 가능한 점수는 1, 2, 3, 4, 6, 9다. 예전 6–9 높음 구간은 현재 척도가 아니다. Findings의 기존 점수 3은 초기 등급으로 둔다. ADR-011과 Checks 판정은 그대로다.

## 2026-10-16 해시 개수 검사

PR #9의 python-quality가 실패했다. evidence-hashes.md의 2026-10-12 첫 표는 21개다. 재계산 7개와 가공본 10개는 같은 해시의 반복이고, 새 값은 data-flow.pdf와 users-active.csv다. 출현은 40, 고유는 23이다. 해시 행은 그대로 둔다. 검사는 첫 표 21개를 세고, 2026-10-14 이후 새 해시는 이 둘만 허용한다. secret-scan은 통과했다. 병합은 이 검사 통과 뒤에 한다.

## 2026-10-16 9단계 수집기 v2

jy_evidence_v2.py, test_jy_evidence_v2.py, jy_closeout.py, test_jy_closeout.py를 tools에 넣었다. SHA256은 부록 E와 같다. py -3 unittest는 v2 20건 OK, closeout 10건 OK다. 두 --help도 정상이다. 실제 토큰과 Zammad 수집은 하지 않았다. jy_evidence.py와 list_zammad.py는 이력으로 남긴다. v2는 직원 6명의 active만 다룬다.

## 2026-10-16 10단계 도구 검사

ruff를 0.12.12로 고정했다. 예전 도구 4개를 그 버전으로 포맷하고 list_zammad.py의 import를 나눴다. v2 파일은 그대로 뒀다. venv에서 v2 20건, closeout 10건, pytest 42건이 통과했다. 실제 토큰과 Zammad 수집은 하지 않았다. quality.yml은 collector와 tools를 함께 검사하도록 바꾼다.

## 2026-10-16 11단계 사고 기록

16장을 전체 다시 썼다. 2026-10-07의 JY-INC-2026-01 사실은 유지했다. T0부터 T+60은 목표시간으로 분리했다. 제34조 제1항만 시행 2026-09-11 조문 화면에서 옮겼다. 유출등 해당 여부와 신고 기한 숫자는 미확인이다. 발송과 신고는 없다. F02는 미흡이다.

## 2026-10-16 11단계 권리 모의

`docs/rights-request-simulation.md`를 새로 썼다. 요청ID는 JY-RR-2026-01이고 접수일은 2026-10-16이다. 유형은 삭제다. 2026-10-06 자료 보안은 참조만 했고, 본인확인과 회신을 소급하지 않았다. 처리기한 숫자는 비웠다. B04는 미확인이다. 메일은 보내지 않았다.

## 2026-10-19 11단계 처리방침

reports/policy에 Before, After, Tracked 문서와 After, Tracked PDF를 넣었다. 원문 시점은 미기재이고 Word 변환일은 2026-10-19이다. After에는 티켓 번호와 로컬 경로를 넣지 않았다. Tracked에는 초기 문장 삭제, 새 문안 삽입, 메모 5개가 있다. B02 판정은 바꾸지 않았다.

## 2026-10-19 11단계 수탁 점검표

reports/outsourcing/JY-Outsourcing-Checklist.xlsx를 넣었다. 시트는 문서정보, 수탁목록, 표본점검이다. V-01과 V-02의 계약, 권한, 파기, 교육을 채웠다. 계약 체결과 연간 감독 실적은 없다. D01은 미흡이다.

## 2026-10-19 11단계 교육 1장

reports/training/JY-Privacy-Training.docx와 JY-Privacy-Training.pdf를 넣었다. 원문은 docs/15-training-one-pager.md이다. 상담원, 유지보수, 관리자가 지킬 행동을 1쪽에 넣었다. 서명과 출석은 없다. D04는 미흡이다.