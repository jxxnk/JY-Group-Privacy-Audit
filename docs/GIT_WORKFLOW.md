# Git 브랜치 및 작업 흐름

## 1. 목적

이 프로젝트에서 Git은 단순 백업이 아니라 컨설팅 과정을 입증하는 증적이다. 모든 중요한 판단과 결과는 `Issue → Branch → Commit → Pull Request → Review → Merge → Tag/Release`로 이어져야 한다.

## 2. 저장소 정책

- 작업 중에는 GitHub 비공개 저장소를 사용한다.
- 최종 공개 전 실제 개인정보, 비밀, 내부 IP·계정, 원본 패킷과 라이선스 문서를 제거한다.
- `main`과 `develop` 직접 push를 금지하고 Pull Request로만 병합한다.
- PR에는 최소 하나의 관련 Issue를 연결한다.
- 개인 프로젝트이므로 리뷰어는 본인이지만 체크리스트와 CI를 통과한 뒤 병합한다.
- force push, history rewrite와 대규모 squash는 이미 공유된 브랜치에서 사용하지 않는다.

## 3. 고정 브랜치

| 브랜치 | 역할 | 병합 대상 |
|---|---|---|
| `main` | 검증된 공개 가능 결과와 릴리스 | 최종 단계에서만 |
| `develop` | 완료된 작업의 통합 기준선 | 모든 작업 브랜치 |

초기 생성 명령 예시는 다음과 같다.

```bash
git init -b main
git add .
git commit -m "chore: initialize privacy audit project"
git switch -c develop
git push -u origin main
git push -u origin develop
```

GitHub에서 두 브랜치에 branch protection을 설정하고 `quality` 상태검사를 요구한다.

## 4. 규정된 작업 브랜치

| 순서 | 브랜치 | 목적 | 대표 산출물 |
|---:|---|---|---|
| 1 | `plan/incident-analysis` | 사건·법·정책 방향 조사 | 사건분석, 출처대장 |
| 2 | `docs/scope-and-inventory` | 범위, 조직, 자산과 흐름 설계 | 범위서, 자산대장, 흐름도 |
| 3 | `docs/control-mapping` | 법·인증·기술기준 통합 | 통제 매트릭스, 체크리스트 |
| 4 | `lab/group-network` | 개선 전 가상환경 구성 | 구성도, Docker/VM 설정 |
| 5 | `feat/linux-evidence-collector` | 계정·서버·로그 증적수집 | Python/Bash 모듈과 테스트 |
| 6 | `feat/network-evidence` | 연결·포트·방화벽 증적수집 | 도달성 결과와 정규화 |
| 7 | `feat/report-generator` | 결과를 표·보고서로 변환 | CSV/XLSX/Markdown 생성기 |
| 8 | `fix/access-control-remediation` | 발견사항 개선 및 재점검 | 개선 설정과 전후 증적 |
| 9 | `docs/final-report` | 최종 기술·경영진 보고 | 보고서, 회고, 발표자료 |

브랜치를 미리 모두 만들지 않는다. 관련 Issue가 준비된 시점에 최신 `develop`에서 생성한다.

```bash
git switch develop
git pull --ff-only origin develop
git switch -c feat/linux-evidence-collector
```

## 5. Issue 흐름

Issue에는 다음을 작성한다.

- 배경과 해결할 문제
- 범위와 제외 범위
- 예상 산출물
- 적용 기준 또는 출처
- 완료조건
- 예상시간/실제시간
- 위험과 보안 주의사항
- 연결할 브랜치와 후속 Issue

작업이 커지면 2~6시간 단위로 나눈다. 조사·문서·코드·랩 변경을 한 Issue에 무리하게 섞지 않는다.

## 6. VS Code 작업 흐름

1. GitHub에서 Issue를 만든다.
2. VS Code Source Control에서 `develop`을 최신화한다.
3. 규정된 이름으로 브랜치를 만든다.
4. 작업 전에 Issue의 완료조건을 체크리스트로 옮긴다.
5. 변경 중에는 `git diff`와 VS Code diff로 비밀·개인정보·불필요한 생성물을 확인한다.
6. 작은 단위로 테스트하고 커밋한다.
7. push 후 `develop` 대상 Draft PR을 일찍 연다.
8. 구현·문서·테스트·보안 체크를 완료하고 Ready for review로 전환한다.
9. 본인이 PR을 처음 보는 사람처럼 검토하고 CI 통과 후 병합한다.
10. 로컬 `develop`을 갱신하고 병합된 작업 브랜치를 삭제한다.

## 7. 커밋 규칙

Conventional Commits의 다음 유형을 사용한다.

- `docs`: 계획, 조사, 체크리스트, 보고서
- `feat`: 새로운 수집·변환 기능
- `fix`: 오류 또는 통제 미흡 개선
- `test`: 테스트 추가·수정
- `refactor`: 동작 변화 없는 구조 개선
- `chore`: 설정, 의존성, CI와 저장소 관리
- `security`: 비밀 제거, 보안 강화와 안전장치

예시:

```text
docs: map processor oversight controls to evidence
feat: collect linux privileged account evidence
test: add redaction test for collector output
fix: restrict inter-company database connectivity
security: prevent raw evidence from being committed
```

한 커밋은 한 가지 이유로 설명 가능해야 한다. `update`, `final`, `수정`처럼 의미 없는 메시지를 쓰지 않는다. 자동 생성물과 소스 변경은 필요하면 별도 커밋으로 나눈다.

## 8. Pull Request 규칙

- 제목은 커밋 규칙과 같은 형식을 사용한다.
- 본문에 `Closes #번호`를 쓴다.
- 변경 이유, 적용 기준, 검증방법, 민감정보 점검, 스크린샷/샘플과 한계를 기록한다.
- 보고서 결과를 바꾸는 코드라면 이전과 이후 샘플을 비교한다.
- 법률 또는 기준 해석이 바뀌면 출처와 확인일을 반드시 적는다.
- 큰 PR은 병합 전에 논리 단위로 분리한다.

권장 병합은 `Squash and merge`다. 개별 커밋에 중요한 판단 이력이 있으면 `Create a merge commit`을 선택하고 PR에 이유를 기록한다. 프로젝트 전체에서 선택을 일관되게 유지한다.

## 9. 태그와 릴리스

| 태그 | 의미 | 필수 포함내용 |
|---|---|---|
| `v0.1-scope` | 사건·범위 확정 | 사건분석, 범위, 가정·한계 |
| `v0.2-current-state` | 현황진단 완료 | 자산·흐름·연결·초기 발견 |
| `v0.3-evidence-collector` | 수집기 구현 | 코드, 테스트, 샘플 증적 |
| `v0.4-remediation` | 개선안 및 적용 | 이행계획, 변경 설정 |
| `v0.5-retest` | 재점검 완료 | 전후 비교, 잔여위험 |
| `v1.0-final` | 최종 포트폴리오 | 공개용 결과, 보고서, 회고 |

태그는 검증된 `main` 커밋에 annotated tag로 생성한다.

```bash
git switch main
git pull --ff-only origin main
git tag -a v1.0-final -m "Complete JY Group privacy audit portfolio"
git push origin v1.0-final
```

각 GitHub Release에는 범위, 주요 변화, 검증결과, 알려진 한계와 다음 버전을 작성한다.

## 10. 브랜치 병합 흐름

모든 작업 브랜치는 `develop`으로 들어간다. 각 마일스톤에서 통합 테스트와 공개 가능성 검토를 거친 뒤 `develop → main` PR을 만든다. 긴급 수정도 실제 서비스 운영 저장소가 아니므로 별도 hotfix 모델을 두지 않고 `fix/* → develop → main` 순서를 유지한다.

## 11. 비밀 및 대용량 파일

절대 커밋하지 않는 항목:

- `.env`, API 키, PAT, SSH 개인키, 비밀번호
- 실제 개인정보와 원본 고객자료
- VM 이미지, 메모리 덤프와 대형 패킷 원본
- 내부망을 식별할 수 있는 공개 부적절 정보
- 구매한 ISO PDF 또는 무단 복제 문서

커밋 전 `gitleaks detect --no-git`를 실행하고, PR CI에서도 검사한다. 이미 커밋된 비밀은 파일 삭제만으로 해결되지 않으므로 즉시 키를 폐기하고 별도 대응 Issue를 만든다.

## 12. GitHub 공개 전 점검

- 모든 샘플이 합성 데이터인가?
- 사람 이름·이메일·전화번호·사번이 실제 값이 아닌가?
- 내부 IP와 호스트명이 문서용 범위로 치환됐는가?
- raw evidence가 `evidence/sanitized` 결과로 대체됐는가?
- ISO 원문이나 재배포 제한 자료가 없는가?
- 링크, 테스트, 보고서 재생성이 정상인가?
- README가 현재 결과와 일치하는가?
- 한계와 미완료 항목이 숨겨지지 않았는가?

## 13. 충돌과 예외

기존 변경을 임의로 덮어쓰거나 `git reset --hard`를 사용하지 않는다. 충돌 시 양쪽 변경 의도를 확인하고 해결 내용을 PR에 기록한다. 규정된 흐름을 벗어날 필요가 있으면 먼저 `docs/DECISION_LOG.md`에 이유·대안·영향을 기록한다.
