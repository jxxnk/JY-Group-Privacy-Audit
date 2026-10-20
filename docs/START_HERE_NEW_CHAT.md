# 새 대화에서 시작

수행자: 김준영  
저장소: `C:\JY-Lab\JY-Group-Privacy-Audit`  
2026-10-07 작업 브랜치: `feat/linux-evidence-collector`  
2026-10-14 작업 브랜치: `docs/closeout-baseline-02`  
2026-10-19 작업 브랜치: `docs/closeout-deliverables-02`  
GitHub: `https://github.com/jxxnk/JY-Group-Privacy-Audit.git`

이 파일을 새 채팅에 붙이거나 열어 달라고 하면 됩니다. F-01~F-03 시험을 다시 하지 마세요.

## 지금 상태 (2026-10-19)

작업 브랜치는 `docs/closeout-deliverables-02`이다. 로컬 최신 커밋은 `ae67b9c`이고 아직 푸시 전이다. origin/main은 `56696f3`이며 2026-10-16 풀 리퀘스트 #10이다. 이 보완 브랜치는 아직 머지하지 않았다. `v1.0-final.1`은 만들지 않았다.

- 워크북은 기본 11시트와 Incident 시트다. 시트 탭에는 `FinalReview`도 있다.
- Checks A02 증적ID는 `S-L01~S-L07`이다. 판정 `적합`은 유지했다.
- E02 증적ID는 `E-F03-B01`이다. 판정 `적합`은 유지했다.
- B04는 `미확인`이다. `docs/15-rights-request-simulation.md`는 모의 기록이고 실제 이메일은 없다.
- `tools/list_zammad.py`는 `127.0.0.1:8080`과 `localhost:8080`만 허용한다.
- 아직 없는 것: Sessions 회수, E04 백업 실측, CR-04/A-03, 실제 교육·감독·권리 이메일, 이 브랜치의 PR과 머지.

## 지금 상태 (2026-10-07)

14~18장 문서와 워크북·tickets.csv id는 feat 브랜치에 있음. 마지막 복구 커밋 예: README `20a5e03`.  
남은 큰일: Word/PDF·PPT 로컬 변환, Gitleaks, (선택) Issue/PR, Controls 항·호(원문 후), CR-04 T12는 증적 고정 전 삭제 금지.

이 절은 2026-10-07 기록이다.

## Zammad가 필요하면

```powershell
Set-Location C:\JY-Lab\zammad-runtime
docker compose ps
docker compose start
docker compose ps
```

`http://127.0.0.1:8080` 주소창. AJ `admin@jy.example.test`. **down -v 금지.** T12 zoom/14, T15 zoom/17.

## Git (2026-10-19)

이 저장소에서 지금 쓰는 브랜치다. 다른 브랜치로 바꾸지 않는다.

```powershell
Set-Location C:\JY-Lab\JY-Group-Privacy-Audit
git status
git add -- <바꾼 파일만>
git commit -m "<한 조각>"
git push
```

add 금지: `private-evidence`, `.env`, PNG, `users-*.json`, `jy-doc02-copy.txt`, `*.bak`, `reports/JY-Audit-Workbook.before-final-remediation.xlsx`  
Cursor 쪽 원격을 `git pull` 하지 않음. README를 통째로 덮어쓰지 않음.

## Git (2026-10-07 방법)

아래 명령은 2026-10-07에 `feat/linux-evidence-collector`로 올리던 방법이다. 오늘 작업에 쓰지 않는다.

```powershell
Set-Location C:\JY-Lab\JY-Group-Privacy-Audit
git checkout feat/linux-evidence-collector
git status
git add <프로젝트 파일만>
git commit -m "<한 조각>"
git push origin feat/linux-evidence-collector
```

## 덮어쓰지 말 것

Checks: C02·C03·C04·D02·D03·E03·F04 `미흡`. E02만 삭제 범위 `적합`. B04·E04 `미확인`. F03 `적용 제외`.

## 핵심 ID

T02=3/#52003 · T11 시험=29/#52028(삭제) · T12=14/#52014 · T15=17/#52017