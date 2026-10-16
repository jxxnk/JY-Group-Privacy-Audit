# 검증 종료 기록

기록일: 2026-10-16
브랜치: `fix/evidence-validation-02`
기준 커밋: `192f185`

## 구분

가이드 작성자의 모의 검증은 Python 3.12, pytest 8.4.2, ruff 0.12.12다. 아래 표는 그 기록이 아니라 이 Windows PC에서 실행한 결과다.

## 이 PC의 실행

환경은 Python 3.13.14, pytest 8.4.2다. 처음 설치된 ruff는 0.17.0이었고, `requirements-dev.txt`를 `ruff==0.12.12`로 고정한 뒤 다시 설치했다. 종료 코드는 따로 출력하지 않았다. 아래 문장이 출력된 명령을 통과로 적는다.

| 명령 | 결과 |
| --- | --- |
| `py -3 -m unittest discover -s tools -p test_jy_evidence_v2.py -v` | Ran 20 tests, OK |
| `py -3 -m unittest discover -s tools -p test_jy_closeout.py -v` | Ran 10 tests, OK |
| `py -3 tools\jy_evidence_v2.py --help` | 사용법 출력 |
| `py -3 tools\jy_closeout.py --help` | 사용법 출력 |
| venv unittest v2 | Ran 20 tests in 0.490s, OK |
| venv unittest closeout | Ran 10 tests in 11.484s, OK |
| venv `pytest -q` 포맷 전 | 42 passed in 12.42s |
| venv `pytest -q` 포맷 후 | 42 passed in 12.60s |
| `ruff 0.12.12 check collector tools` | All checks passed |
| `ruff 0.12.12 format --check collector tools` | 12 files already formatted |

ruff 0.17.0은 collector와 tools에서 19건을 실패로 표시했다. 그중 `ValueError`를 `TypeError`로 바꾸라는 항목과, 자격증명이 출력되지 않게 막아 둔 `except Exception`을 빼라는 항목은 적용하지 않았다. v2 네 파일은 부록 E 바이트 그대로다. 0.12.12에서는 그 파일의 검사와 포맷이 통과한다. 예전 도구 4개는 줄 길이를 고쳤고, `list_zammad.py`의 한 줄 import를 나눴다. 커밋은 `192f185`다.

## 하지 않은 실행

Zammad 수집, API 토큰 입력, Docker 재시작, 이 브랜치의 GitHub Actions는 하지 않았다. `quality.yml` 수정 후의 PR 검사는 푸시 뒤에 확인한다.