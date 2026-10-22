# PROJECT_STATE

상태 갱신일: 2026-10-22
수행 위치: `C:\JY-Lab\JY-Group-Privacy-Audit`
수행자: 김준영 (고객 역할과 컨설턴트 역할을 겸함. 실제 고객 인터뷰가 아님)
현재 작업 브랜치: `docs/project-state-15`. 이 파일의 상태 갱신을 기록하는 브랜치다.
main: `28f8aac`. Merge pull request #11. 이전 main은 `56696f3`이고, 그 커밋은 2026-10-16 풀 리퀘스트 #10이다.
태그: `v1.0-final`은 `35b7b85`에 그대로 둔다. 검수 후 태그 `v1.0-final.1`은 `28f8aac`에 있다.
보완 PR: #11은 완료다. 그 커밋의 CI는 python-quality와 secret-scan이 통과했다. 이전 실습 PR #2도 완료된 상태다.
Word, PDF, PPT: `reports/JY-Final-Report.docx`, `reports/JY-Final-Report.pdf`, `reports/JY-Briefing.pptx`가 있다.
Workbook: 기본 11시트와 Incident가 있다. 시트 탭에는 FinalReview도 있어 시트는 13개다.
Controls 확인 범위: `docs/control-notes.md`와 `docs/sources.csv`의 S-L01부터 S-L07이다.
JSON-F01-DIFF와 E-D03-A01은 Evidence에 해시를 기입했다. 원본은 Git 밖에 있다.
ENV 해시: ENV-01과 ENV-02는 공란이다. 원본은 Git 밖에 있다.
결정: ADR-015. 본문은 `docs/DECISION_LOG.md`
GitHub: https://github.com/jxxnk/JY-Group-Privacy-Audit.git
Zammad 런타임: `C:\JY-Lab\zammad-runtime`
Zammad compose 커밋: `27944f87aed91420242dfa97038ff96555d7cbe7`
접속: http://127.0.0.1:8080 (한국어 UI)
원본 증적: `C:\JY-Lab\private-evidence\` (Git 제외)
참고 PDF: `C:\JY-Lab\reference\`

## 2026-10-19 기록

- Workbook은 기본 11시트에 `Incident`를 더한 상태다. 시트 탭에는 `FinalReview`도 있다.
- Checks E02 증적ID는 `E-F03-B01`이다. 판정 `적합`은 유지했다.
- Checks A02 증적ID는 `S-L01~S-L07`이다. 법·시행령·고시·ISMS-P·ISO·KISA 범위를 관측결과와 한계에 구분했다. 판정 `적합`은 유지했다.
- `tools/list_zammad.py`는 `http://127.0.0.1:8080`과 `http://localhost:8080`만 허용한다. 프록시와 리다이렉트를 차단한다.
- `docs/15-rights-request-simulation.md`에 RR-01 모의 기록이 있다. 실제 이메일은 보내지 않았다. Checks B04는 `미확인`이다.
- 환경 버전은 `docs/environment.md`의 2026-10-19 관측이다. Windows 11 Home 25H2, OS 빌드 26200.9711. Zammad 이미지는 이날 다시 확인하지 못했다.
- v1 `tools/jy_evidence.py`에는 `diff` 명령이 없다. `users-diff.json`은 `private-evidence/after`에만 있고 S05 active True→False만 기록되어 있다. 현재 수집기는 `tools/jy_evidence_v2.py`이며 명령은 `collect`, `diff`, `verify`다.

## Checks 요약 (2026-10-19, 덮어쓰지 말 것)

적합: A01 A02 A03 A04 B01 C01 E02 F01
미흡: B02 B03 C02 C03 C04 D01 D02 D03 D04 E01 E03 F02 F04
미확인: B04 E04
적용 제외: F03

판정 수: 적합 8, 미흡 13, 미확인 2, 적용 제외 1, 합계 24.

## 아직 하지 않은 것

- Sessions 기존 세션 회수
- E04 백업 복구 실측
- CR-04/A-03. T12 참조 파기와 사본·백업 검색
- 실제 교육 서명, 실제 수탁 감독 실적, 실제 권리 이메일
- 2026-10-19 Zammad 이미지 재확인. Docker Desktop 엔진이 중지되어 있었음

## 다음 세 가지 행동

1. 이 파일을 저장하고 브랜치 `docs/project-state-15`에 커밋한다. 이 커밋은 패키지 커밋 `28f8aac`를 바꾸지 않는다.
2. `docs/project-state-15`에서 `main`으로 보내는 풀 리퀘스트를 만든다. `main`에 직접 커밋하지 않는다.
3. 태그 `v1.0-final`은 `35b7b85`에, `v1.0-final.1`은 `28f8aac`에 그대로 둔다. 이 기록에는 새 태그를 만들지 않는다.

## 금지사항

- docker compose down -v
- 원본 증적·토큰·.env를 GitHub에 올리기
- T12를 Scheduler 미리보기 1건 없이 삭제
- T15·조직 JY-Lab-Customers 삭제
- Checks 초기 미흡을 재점검 성공만으로 적합으로 덮기
- 확인하지 않은 백업 복구·물리보안·웹 취약점 전체를 완료로 표시
- 실제 사고 신고, 실제 메일 발송, 외부 AI에 상담문 전송
- 가이드 PDF를 결과보고서인 것처럼 제출

## 2026-10-06 메모

이 절은 2026-10-06에 적어 둔 메모다. 현재 작업 지시가 아니다. 2026-10-14 머리글은 기준 커밋을 `main` `35b7b85`로 적었고, 현재 결정을 ADR-015로 적었다.

프로젝트명: JY그룹 개인정보 보호 컨설팅 실습 (단일 Zammad)
가이드: JY-Group-Privacy-Audit-Execution-Guide / 작성 기준일 2026-09-09 / 실행 중심 개정판
상태 갱신일: 2026-10-06
현재 브랜치: feat/linux-evidence-collector
마지막 커밋: 당시 미기입
Zammad compose 커밋: 당시 미기입

### 완료한 단계

- 2~4장: Windows·Docker·공식 zammad-docker-compose, localhost:8080. `down -v` 사용 안 함.
- 5~6장: 직원 S01~S06, 고객 C01~C10, 그룹 JY-General/JY-Restricted, 조직 JY-Lab-Customers(초기 Shared Yes). 합성 티켓·첨부. 일부 티켓은 재생성되어 T01/T11/T12/T15가 두 벌임.
- 7장: docs/client-before 6종, scope.md.txt, interview.md.txt, data-flow.pdf.
- 8장: docs/sources.csv, docs/control-notes.md. Controls 항·호는 원문 추가 전.
- 9장: reports/JY-Audit-Workbook.xlsx 11시트. Checks 24행 판정 완료(미실시 없음).
- 10장: tools/jy_evidence.py collect → users-before.json, users-after-f01.json. 단위테스트 수행. **diff(users-diff.json)는 아직 없음.**
- 11장 F-01: S05 종료 후 활성·T02 열람 → Active=false, 새 로그인 차단. 증적 E-F01-B01, E-F01-A01. Sessions 기존 세션 종료는 미확인.
- 12장 F-02: S04·S06 T11 과다권한, C02가 T01 열람 → S04 General만, S06 그룹 없음, Shared No. 재점검 적합(R-02a/b).
- 13장 F-03 13.1~13.3: C01 자료 보안 미리보기 T01·T11 4건, 조직 미삭제, 완료 후 C01/T01/T11 없음, T12 마커 잔존, T15 보존. **13.4 T16·Scheduler T12 삭제는 미실행(예정).**
- GitHub feat/linux-evidence-collector에 엑셀·문서·명부·헬퍼 푸시. 원본 PNG/JSON은 비공개 폴더만.

### 실제 생성 수 (관측)

- 직원 6, 고객 삭제 전 10(C01 삭제 후 고객 9 예상)
- 티켓: 원본 15 + 재생성분. C01 소유 T01·T11은 자료 보안으로 삭제됨.
- 핵심 ID: T02 id=3 #52003; T11 시험 id=29 #52028; T12 id=14 #52014; T15 id=17 #52017
- 복제(참고): T01 18/52018, T11 13/52013, T12 30/52029, T15 33/52032

### 당시 Checks 요약

적합: A01 A02 A03 A04 B01 C01 E02 F01
미흡: B02 B03 C02 C03 C04 D01 D02 D04 E01 E03 F02 F04
미확인: B04 D03 E04
적용 제외: F03 (외부 AI 미연결, 공격시험 안 함)

### 당시 증적ID

E-F01-B01, E-F01-A01, JSON-F01-B, JSON-F01-A
E-F02-B01~B03, E-F02-A01, E-F02-A01b, E-F02-A02, E-F02-A03
E-F03-B01~B03, E-F03-A01, E-F03-A02
SHA256은 Workbook Evidence 시트에 기입함. ENV-01/02 해시는 미기입.

### 당시 열려 있는 발견사항

- F-01: 조치 완료, 재점검 적합. 기존 세션 회수·외부 토큰 미확인.
- F-02a/b: 조치 완료, 재점검 적합. 다운로드 사본은 권한 회수로 안 지워짐.
- F-03: 계정·본인티켓 삭제 적합(E02). T12 참조·사본 잔존 미흡(E03). A-03 예정.

### 당시 미완료 단계

1. 10.4 `jy_evidence.py diff` → users-diff.json
2. F-01 기존 세션 vs 새 로그인 구분 기록 (Sessions 없으면 미확인 유지)
3. D03: T12 jy-doc02.txt 로컬 사본 존재 확인
4. tickets.csv에 actual_id / actual_number
5. 14장 위험평가·이행계획·변경요청서·예외대장
6. 15장 처리방침 개선본·위탁 점검표·교육 1장·중장기 계획
7. 16장 사고 도상훈련·모의 통지문·AI 검토서(연결 없음)
8. 17장 모의심사 6항목·보완조치 내역서·미확인 목록
9. 18장 Word 최종보고서 PDF, PPT 7장, README, Issue/PR, Gitleaks, (선택) 태그
10. docs/environment.md, DECISION_LOG.md, START_HERE_NEW_CHAT.md
11. Controls 법령 항·호는 원문 확인 후에만

### 당시 다음 행동

1. 이 파일을 저장하고 feat/linux-evidence-collector에 커밋·푸시한다.
2. 10.4 diff를 실행해 users-diff.json을 private-evidence/after에만 둔다 (Git 금지).
3. 14장 위험점수와 변경요청서 초안을 작성한다.