# 비밀 검사

작성일: 2026-10-13
브랜치: docs/closeout-handover
오늘 로컬 Gitleaks를 실행하지 않았다. 아래는 현재 추적 파일을 대상으로 한 검색이다. Checks 판정은 바꾸지 않는다.

## 결과

- `git ls-files -- .env private-evidence`는 파일을 출력하지 않았다. 종료 코드는 0이다. `.env`와 `private-evidence`는 Git 추적 목록에 없다.
- `git grep`으로 `ZAMMAD_TOKEN=`, `BEGIN PRIVATE KEY`, `BEGIN OPENSSH PRIVATE KEY`, `ghp_`, `github_pat_`를 찾았다. 일치 파일이 없고 종료 코드는 1이다.
- 이 검색은 현재 추적 파일만 본다. Git 전체 이력을 다시 읽지 않았다.
- 환경 변수 이름 `ZAMMAD_TOKEN` 자체는 이번 패턴에 넣지 않았다. 수집기 코드는 그 이름을 읽기만 하고, 값은 문서에 넣지 않는다.
- 풀 리퀘스트 #6의 GitHub `secret-scan`은 통과했다. 그 검사는 Gitleaks다. 오늘 그 명령을 로컬에서 다시 실행하지 않았다.

Checks 판정은 바꾸지 않는다.

## 2026-10-22 로컬 실행

위 2026-10-13 절은 그날 추적 파일만 검색하고 로컬 Gitleaks는 실행하지 않은 기록이다. 2026-10-22 11:36 KST에 이 PC에서 같은 저장소를 Gitleaks로 읽었다. Checks 판정은 바꾸지 않는다.

- 실행 파일은 `C:\JY-Lab\bin\gitleaks\gitleaks.exe`, 버전 8.28.0이다. ZIP SHA256은 `da6458e8864af553807de1c46a7a8eac0880bd6b99ba56288e87e86a45af884f`이다.
- `gitleaks dir . --redact`는 작업 폴더 22.65MB를 5.16초 동안 읽었다. 결과는 no leaks found다.
- `gitleaks git . --redact`는 이 PC 저장소의 79개 커밋, 546.62KB를 10.2초 동안 읽었다. 결과는 no leaks found다. 이 명령이 2026-10-13에 하지 않은 이력 읽기다.
- `.gitignore`에 `private-evidence/`, `zammad-runtime/`, `backups/`를 넣었다. 같은 날 `git ls-files -- .env private-evidence zammad-runtime backups`는 파일을 출력하지 않았다.
- Office를 다시 연 결과는 이 절에 없다.