# 새 대화에서 시작

수행자: 김준영  
저장소: `C:\JY-Lab\JY-Group-Privacy-Audit`  
브랜치: `feat/linux-evidence-collector`  
GitHub: `https://github.com/jxxnk/JY-Group-Privacy-Audit.git`

이 파일을 새 채팅에 붙이거나 열어 달라고 하면 됩니다. F-01~F-03 시험을 다시 하지 마세요.

## 지금 상태 (2026-10-07)

14~18장 문서와 워크북·tickets.csv id는 feat 브랜치에 있음. 마지막 복구 커밋 예: README `20a5e03`.  
남은 큰일: Word/PDF·PPT 로컬 변환, Gitleaks, (선택) Issue/PR, Controls 항·호(원문 후), CR-04 T12는 증적 고정 전 삭제 금지.

## Zammad가 필요하면

```powershell
Set-Location C:\JY-Lab\zammad-runtime
docker compose ps
docker compose start
docker compose ps
```

`http://127.0.0.1:8080` 주소창. AJ `admin@jy.example.test`. **down -v 금지.** T12 zoom/14, T15 zoom/17.

## Git (이 저장소만)

```powershell
Set-Location C:\JY-Lab\JY-Group-Privacy-Audit
git checkout feat/linux-evidence-collector
git status
git add <프로젝트 파일만>
git commit -m "<한 조각>"
git push origin feat/linux-evidence-collector
```

add 금지: `private-evidence`, `.env`, PNG, `users-*.json`, `jy-doc02-copy.txt`, `*.bak`  
Cursor 쪽 원격을 `git pull` 하지 않음. README를 통째로 덮어쓰지 않음.

## 덮어쓰지 말 것

Checks: C02·C03·C04·D02·D03·E03·F04 `미흡`. E02만 삭제 범위 `적합`. B04·E04 `미확인`. F03 `적용 제외`.

## 핵심 ID

T02=3/#52003 · T11 시험=29/#52028(삭제) · T12=14/#52014 · T15=17/#52017
