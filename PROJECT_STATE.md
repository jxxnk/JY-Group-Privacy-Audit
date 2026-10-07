# PROJECT_STATE

프로젝트명: JY그룹 개인정보 보호 컨설팅 실습 (단일 Zammad)
가이드: JY-Group-Privacy-Audit-Execution-Guide / 작성 기준일 2026-09-09 / 실행 중심 개정판
상태 갱신일: 2026-10-06
수행자: 김준영 (고객 역할과 컨설턴트 역할을 겸함. 실제 고객 인터뷰가 아님)
현재 브랜치: feat/linux-evidence-collector
GitHub: https://github.com/jxxnk/JY-Group-Privacy-Audit.git
마지막 커밋: (로컬에서 `git log -1 --oneline` 값으로 교체)
Zammad 런타임: C:\JY-Lab\zammad-runtime
Zammad compose 커밋: (C:\JY-Lab\zammad-runtime에서 `git rev-parse HEAD` 값으로 교체)
접속: http://127.0.0.1:8080 (한국어 UI)
원본 증적: C:\JY-Lab\private-evidence\ (Git 제외)
참고 PDF: C:\JY-Lab\reference\ (가이드 원문)

## 완료한 단계

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

## 실제 생성 수 (관측)

- 직원 6, 고객 삭제 전 10(C01 삭제 후 고객 9 예상)
- 티켓: 원본 15 + 재생성분. C01 소유 T01·T11은 자료 보안으로 삭제됨.
- 핵심 ID: T02 id=3 #52003; T11 시험 id=29 #52028; T12 id=14 #52014; T15 id=17 #52017
- 복제(참고): T01 18/52018, T11 13/52013, T12 30/52029, T15 33/52032

## Checks 요약 (덮어쓰지 말 것)

적합: A01 A02 A03 A04 B01 C01 E02 F01
미흡: B02 B03 C02 C03 C04 D01 D02 D04 E01 E03 F02 F04
미확인: B04 D03 E04
적용 제외: F03 (외부 AI 미연결, 공격시험 안 함)

## 최근 증적ID

E-F01-B01, E-F01-A01, JSON-F01-B, JSON-F01-A
E-F02-B01~B03, E-F02-A01, E-F02-A01b, E-F02-A02, E-F02-A03
E-F03-B01~B03, E-F03-A01, E-F03-A02
SHA256은 Workbook Evidence 시트에 기입함. ENV-01/02 해시는 미기입.

## 열려 있는 발견사항

- F-01: 조치 완료, 재점검 적합. 기존 세션 회수·외부 토큰 미확인.
- F-02a/b: 조치 완료, 재점검 적합. 다운로드 사본은 권한 회수로 안 지워짐.
- F-03: 계정·본인티켓 삭제 적합(E02). T12 참조·사본 잔존 미흡(E03). A-03 예정.

## 미완료 단계 (가이드 순서)

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

## 차단 오류

없음. Zammad는 자료 보안 작업 completed. 검색(Elasticsearch)은 비어 있을 수 있어 URL zoom으로만 확인.

## 다음 세 가지 행동

1. 이 파일을 저장하고 feat/linux-evidence-collector에 커밋·푸시한다.
2. 10.4 diff를 실행해 users-diff.json을 private-evidence/after에만 둔다 (Git 금지).
3. 14장 위험점수와 변경요청서 초안을 작성한다.

## 금지사항

- docker compose down -v
- 원본 증적·토큰·.env를 GitHub에 올리기
- T12를 Scheduler 미리보기 1건 없이 삭제
- T15·조직 JY-Lab-Customers 삭제
- Checks 초기 미흡을 재점검 성공만으로 적합으로 덮기
- 확인하지 않은 백업 복구·물리보안·웹 취약점 전체를 완료로 표시
- 실제 사고 신고, 실제 메일 발송, 외부 AI에 상담문 전송
- 가이드 PDF를 결과보고서인 것처럼 제출
