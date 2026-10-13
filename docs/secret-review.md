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