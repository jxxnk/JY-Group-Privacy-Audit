# tools

## 현재 경로

`tools/jy_evidence_v2.py`는 직원 6명의 active 상태만 다룬다. 명령은 `collect`, `diff`, `verify`다. 역할, 그룹, 세션, 권한, 법적 적합성은 판정하지 않는다. 명부 해시는 64자리 16진수다. `--hash-only`는 해시만 확인하고 구조 검증은 아니다.

`tools/jy_closeout.py`는 제출 목록, 일반 Markdown과 HTML의 상대 링크, 태그 바이트, ZIP과 개별 파일 해시를 검사한다. 명령은 `check`, `pack`, `verify`다. 네트워크와 자격증명은 쓰지 않는다. PDF와 Office 내부 링크, 표의 ID, 법률 판단, 스크린샷 안전은 검사하지 않는다.

## 이력으로 둔 경로

`tools/jy_evidence.py`는 예전 수집기다. 명령은 `collect`와 `hash`다. `diff` 명령은 없다. 새 수집과 대조는 v2를 쓴다.

`tools/list_zammad.py`는 예전 목록 조회다. 새 작업에서는 쓰지 않는다.

`tools/test_jy_evidence.py`는 v1 테스트다. v2 테스트는 `tools/test_jy_evidence_v2.py`다.