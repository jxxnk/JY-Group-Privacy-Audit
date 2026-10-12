# 수집기 부록

작성일: 2026-10-12
기준 코드: `tools/jy_evidence.py`
오늘 수집기를 다시 실행하지 않았다. Checks 판정은 바꾸지 않는다.

## 현재 도구가 하는 일

- 명령은 `collect`와 `hash`다.
- `collect`는 명부 CSV와 Zammad 사용자 목록을 맞춰 JSON을 쓰고, 같은 이름의 `.sha256` 파일을 옆에 둔다.
- 호출은 GET뿐이다. 호스트는 `127.0.0.1` 또는 `localhost`, 포트는 8080, 스킴은 http만 허용한다.
- 경로는 `/api/v1/users`만 허용한다.
- 명부 이메일은 `.example.test`로 끝나야 한다.
- 토큰은 환경 변수 `ZAMMAD_TOKEN` 또는 `JY_ZAMMAD_TOKEN`에서 읽는다. JSON에는 토큰을 넣지 않으며, 출력 메모는 `token omitted; GET localhost only`다.
- 사용자 레코드에 남기는 값은 `staff_id`, `email`, `end_date`, `found`, `zammad_id`, `login`, `active`, `firstname`, `lastname`다.
- User-Agent는 `jy-evidence-local/1.0`이다.
- 이 도구는 개인정보 보호법이나 인증 적합을 판정하지 않는다.

## 이미 있는 산출

- `before\users-before.json`과 `after\users-after-f01.json`은 `collect` 결과다. 옆자리 `.sha256`과 `docs/evidence-hashes.md`의 해시가 같다.
- `after\users-diff.json`의 해시도 `docs/evidence-hashes.md`에 있다. 수집기에 `diff` 명령이 없어 옆자리 `.sha256` 파일은 없다.
- 오늘 이 파일들을 다시 만들지 않았다.

## 하지 않는 일

- `diff` 하위 명령이 없다. 전후 비교 JSON을 수집기가 만든 공식 출력이라고 쓰지 않는다.
- 티켓, 첨부, 그룹, 조직, 세션, 백업은 수집하지 않는다.
- 원격 호스트, https, 8080이 아닌 포트, 경로가 붙은 URL은 거부한다.
- `collector/` 패키지는 버전 `0.0.0` 골격이다. 실습 JSON을 만든 코드는 `tools/jy_evidence.py`다.
- `collector/tests/test_scaffold.py`는 버전 문자열만 확인한다.
- `tools/test_jy_evidence.py`는 서버 없이 URL, 명부, 스냅샷, 해시, GET 제한을 확인하는 단위 테스트다. 오늘 이 테스트를 다시 실행하지 않았다.

Checks 판정은 바꾸지 않는다.