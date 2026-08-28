# Contributing

이 프로젝트는 개인 포트폴리오지만 실제 컨설팅 프로젝트처럼 변경을 관리한다. 기여 전 `README.md`, `docs/AI_WORK_INSTRUCTIONS.md`, `docs/GIT_WORKFLOW.md`를 읽는다.

## 기본 흐름

1. Issue에 문제, 범위, 산출물과 완료조건을 작성한다.
2. 최신 `develop`에서 규정된 작업 브랜치를 만든다.
3. 작은 커밋으로 코드·문서·테스트를 함께 갱신한다.
4. Draft PR을 열고 Issue를 연결한다.
5. 로컬 품질검사와 민감정보 검사를 수행한다.
6. PR 체크리스트와 CI 통과 후 `develop`에 병합한다.
7. 마일스톤 검증 후 `main`과 태그에 반영한다.

## 로컬 검증

```bash
python -m pip install -r requirements-dev.txt
ruff check collector
ruff format --check collector
pytest
gitleaks detect --no-git --redact
```

## 보안

실제 개인정보, 비밀번호, 토큰, SSH 키, 원본 패킷, VM 이미지, 내부자료와 ISO 유료 원문을 커밋하지 않는다. 보안 문제를 발견하면 공개 Issue에 비밀값을 쓰지 말고 먼저 해당 인증정보를 폐기한다.

## 문서와 근거

변경 가능한 사실에는 공식 출처와 확인일을 남긴다. 법률·인증기준을 바꾸는 PR은 적용 버전과 시행일을 명시한다. 자동수집과 사람의 최종판단은 언제나 구분한다.
