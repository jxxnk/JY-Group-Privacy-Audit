# JY Group 개인정보 진단 실습 산출물

가상 JY Retail / Service / Vendor 상담 환경(로컬 Zammad 1식)용 9장 진단 워크북입니다. 실제 기업 감사·인증이 아닙니다.

## 워크북

`reports/JY-Audit-Workbook.xlsx`

| 시트 | 내용 |
| --- | --- |
| Scope | SC-01~05 범위 (결제·배송·마케팅·백업 실측 제외) |
| Assets | A-01~04 상담시스템·첨부·사본·백업 |
| Processing | P-01~03 상담·제한상담·유지보수 |
| Accounts | S01~S06. S05 종료일 2026-09-14, **Active = FALSE** (F-01 개선 후) |
| Sources | S-L01~L04 법령·고시·작성지침 |
| Controls | CT-F01~F03 |
| Checks | 24행. 시험·문서 대조 반영. E04=`미확인`, B04=`미확인`, D03=`미흡`, F03=`적용 제외` |
| Findings / Actions / Retest | F-01·F-02a·F-02b·F-03. R-01·R-02a·R-02b=`적합`, R-03=`미흡`. A-03 상태 예정. 담당=가상 역할명(S01/S02) |
| Evidence | ENV + F-01/F-02/F-03 화면·JSON + JSON-F01-DIFF + E-D03-A01. SHA256은 로컬 해시 후 기입 |

Checks 판정 목록: `적합`, `미흡`, `미확인`, `적용 제외`, `미실시`.

## 내 PC에 저장

1. 이 저장소에서 `reports/JY-Audit-Workbook.xlsx`를 받습니다.
2. 아래 경로로 받아 기존 9장 양식 위에 덮어씁니다. 증적 PNG는 `private-evidence`에 그대로 둡니다.

```
C:\JY-Lab\JY-Group-Privacy-Audit\reports\JY-Audit-Workbook.xlsx
```

`reports` 폴더가 없으면 만듭니다.

```powershell
New-Item -ItemType Directory -Force -Path C:\JY-Lab\JY-Group-Privacy-Audit\reports
Copy-Item -Path .\reports\JY-Audit-Workbook.xlsx -Destination C:\JY-Lab\JY-Group-Privacy-Audit\reports\JY-Audit-Workbook.xlsx
```

3. Excel에서 Accounts S05 종료일 `2026-09-14`, Active=`FALSE`를 확인합니다.
4. Evidence 원본경로가 `C:\JY-Lab\private-evidence\`의 실제 파일명과 다르면 그 시트만 고칩니다.
5. `docs\sources.csv`, `docs\control-notes.md`, `docs\14-*.md`도 프로젝트 `docs\`에 복사합니다.

## 14장 문서

| 파일 | 내용 |
| --- | --- |
| `docs/14-risk-assessment.md` | 발생 1–3 × 영향 1–3, 잔여, 이행 역할 |
| `docs/14-change-requests.md` | CR-01~03 완료, CR-04(T12 파기) 예정 |
| `docs/14-exception-register.md` | 백업·Sessions·T12 증적 유지·AI 적용 제외 |

## 15장 문서

| 파일 | 내용 |
| --- | --- |
| `docs/15-privacy-policy-after.md` | 처리방침 개선본. B02는 초기 미흡 유지 |
| `docs/15-outsourcing-checklist.md` | 수탁 점검표. D01 연간실적 없음 |
| `docs/15-training-one-pager.md` | 교육 1장. D04 서명 없음 |
| `docs/15-30-90-plan.md` | 30일·90일 과제. T12 강제 삭제 아님 |

## 16장 문서

| 파일 | 내용 |
| --- | --- |
| `docs/16-incident-tabletop.md` | S05 도상훈련 Incident 기록. F02 미흡 유지 |
| `docs/16-mock-notification.md` | 모의 통지문. 발송 없음 |
| `docs/16-ai-review.md` | AI 미연결. F03 적용 제외 유지 |

## 17장 문서

| 파일 | 내용 |
| --- | --- |
| `docs/17-self-review.md` | 모의심사 6항목. 판정 값을 바꾸지 않음 |
| `docs/17-remediation-log.md` | CR-01~03 완료, CR-04 예정 |
| `docs/17-unconfirmed.md` | B04·E04 및 해시·Sessions 등 |

## 18장 문서

| 파일 | 내용 |
| --- | --- |
| `docs/18-final-report.md` | 최종보고서 초안. Word에 붙여 PDF로 내보내면 됨 |
| `docs/18-slides.md` | 발표 7장 원고. PNG는 비공개 폴더만 |

### 18.2 제출 묶음 (Git에 넣는 것)

- `reports/JY-Audit-Workbook.xlsx`
- `docs/` (14~18장, sources, control-notes)
- `tools/jy_evidence.py` (GET localhost만)
- `samples/synthetic-data/jy/` (합성 명부·tickets.csv)

Git에 넣지 않음: `C:\JY-Lab\private-evidence\`, `.env`, 토큰, PNG, `users-*.json`, `jy-doc02-copy.txt`.

Gitleaks·GitHub Issue/PR·태그는 이 초안 다음 조각입니다. 지금 `main`으로 머지하지 않습니다. 브랜치는 `feat/linux-evidence-collector`만 사용합니다.

## 다시 만들기

9장 초기 양식만 다시 만들면 Findings가 비워집니다.

```powershell
py -3 -m pip install openpyxl
py -3 tools\generate_audit_workbook.py
py -3 tools\apply_f01_f02_workbook.py
```

## 하지 말 것

- Checks C02·C03·C04·D02·E03를 재점검/삭제 성공만으로 `적합`으로 바꾸기. C01 본인 티켓 삭제는 E02만 `적합`. F-03 잔존은 Retest R-03=`미흡`.
- 증적 원본·토큰·`.env`를 Git에 올리기.

## 10장 수집기

`tools/jy_evidence.py` — `127.0.0.1:8080` GET만. 명부 이메일은 `.example.test`.

```powershell
py -3 -m unittest discover -s tools -p "test_jy_evidence.py" -v
$env:ZAMMAD_URL = "http://127.0.0.1:8080"
$env:ZAMMAD_TOKEN = "화면에서-한-번만-보이는-값"
py -3 tools\jy_evidence.py collect --roster samples\synthetic-data\jy\staff.csv --out C:\JY-Lab\private-evidence\before\users-before.json
```

JSON은 `C:\JY-Lab\private-evidence`에만 둡니다. 커밋하지 않습니다.
