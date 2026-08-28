# 새 채팅 시작 및 빠른 환경 설정

## 1. 이 파일을 먼저 읽는 이유

이 저장소는 이전 대화를 기억하지 못하는 새로운 GPT도 프로젝트를 바로 이어갈 수 있게 구성했습니다. 새 채팅에서는 긴 배경을 다시 설명하지 말고 이 저장소 ZIP 파일을 첨부한 다음 아래 프롬프트를 그대로 전달하면 됩니다.

## 2. 새 채팅에 전달할 파일

`JY-Group-Privacy-Audit-Starter.zip` 파일 하나를 첨부합니다. 압축본에는 기획, 서사, 작업규칙, 현재 상태, Git 운영방식과 코드 골격이 함께 들어 있습니다.

## 3. 새 채팅에 그대로 붙여 넣을 프롬프트

```text
첨부한 JY-Group-Privacy-Audit-Starter.zip은 앞으로 진행할 개인정보 보호 컨설팅 포트폴리오의 기준 저장소입니다.

작업을 시작하기 전에 압축을 풀고 다음 파일을 순서대로 전부 읽어주세요.
1. START_HERE_NEW_CHAT.md
2. PROJECT_STATE.md
3. README.md
4. AGENTS.md
5. docs/AI_WORK_INSTRUCTIONS.md
6. docs/PROJECT_MASTER_PLAN.md
7. docs/DECISION_LOG.md
8. docs/GIT_WORKFLOW.md
9. docs/CONTROL_BASELINE.md
10. docs/DELIVERABLES_AND_DOD.md

이 프로젝트는 HD현대그룹 계열사 개인정보 유출사고에서 확인된 계열사 간 불필요한 연결과 책임 공백에 주목해서 시작한 가상의 JY그룹 개인정보 보호 관리체계 진단 및 ISMS-P 사전심사 프로젝트입니다. 개인정보 보호법과 ISMS-P를 중심으로 하고, ISO/IEC 27701은 합법적으로 접근 가능한 공개정보 범위에서 참고하며, 주통기 가이드는 서버·DB·네트워크 기술점검에만 적용합니다. 자동화 기능은 증적수집을 돕지만 적합 여부를 최종판단하지 않습니다.

파일을 읽기 전에는 프로젝트 내용을 추정해서 작업하지 마세요. 모두 읽은 다음 현재 확정된 결정, 현재 진행상태, 다음 권장 작업, 이번에 사용할 브랜치를 먼저 요약해서 알려주세요. 아직 파일은 변경하지 말고 제 지시를 기다려주세요.
```

이 프롬프트를 사용하면 새로운 GPT가 먼저 자료를 읽고 현재 상태를 요약한 뒤 대기하게 됩니다. 따라서 대화가 바뀌어도 처음부터 기획을 다시 만들 가능성이 줄어듭니다.

## 4. 이후 업무 지시 형식

새 채팅에서 실제 업무를 요청할 때는 다음 형식을 사용합니다.

```text
이번 작업 목표:
관련 Issue:
사용할 브랜치:
수정 가능한 범위:
필수 산출물:
완료조건:
검증할 내용:
```

예시는 다음과 같습니다.

```text
이번 작업 목표: HD현대그룹 사고와 2026년 개인정보 정책 변화를 공식자료 중심으로 분석해 사건분석서를 작성해주세요.
관련 Issue: #1
사용할 브랜치: plan/incident-analysis
수정 가능한 범위: docs/research와 PROJECT_STATE.md
필수 산출물: 사건 타임라인, 사고 확산 원인, 법적 쟁점, JY그룹 반영사항, 출처대장
완료조건: 사실·해석·프로젝트 제안을 구분하고 모든 최신 주장에 공식 URL과 확인일을 기재
검증할 내용: 실제 기업의 미공개 사실을 추정하지 않았는지 확인
```

## 5. Windows에서 가장 빠른 로컬 설정

### 준비물

- Git
- Python 3.12 권장
- VS Code
- GitHub 계정

ZIP 압축을 푼 뒤 폴더를 VS Code에서 엽니다. VS Code에서 `터미널 → 새 터미널`을 누르고 PowerShell에서 다음 명령을 실행합니다.

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\bootstrap.ps1
```

스크립트는 다음 작업만 수행합니다.

- Git 저장소가 없으면 `main` 브랜치로 초기화
- `.env.example`을 복사해서 로컬 전용 `.env` 생성
- Python 가상환경 `.venv` 생성
- 개발 의존성 설치
- 최소 import 및 테스트 실행

비밀번호나 GitHub 토큰을 만들거나 저장하지 않으며 자동으로 원격 저장소에 push하지 않습니다.

## 6. GitHub 저장소 연결

GitHub에서 빈 Private 저장소 `JY-Group-Privacy-Audit`을 만듭니다. README, `.gitignore`, 라이선스 자동생성은 선택하지 않습니다. 로컬 PowerShell에서 다음 순서로 연결합니다.

```powershell
git status
git add .
git commit -m "chore: initialize JY Group privacy audit project"
git remote add origin https://github.com/사용자명/JY-Group-Privacy-Audit.git
git push -u origin main
git switch -c develop
git push -u origin develop
```

GitHub 저장소의 Settings에서 `main`과 `develop`에 branch protection을 적용합니다. 직접 push 대신 Pull Request를 사용하고 `quality` 검사를 요구하도록 설정합니다.

## 7. 첫 실제 작업

첫 Issue는 `HD현대그룹 사고 및 개인정보 정책동향 분석`으로 만듭니다. 첫 작업 브랜치는 `plan/incident-analysis`입니다.

```powershell
git switch develop
git pull --ff-only origin develop
git switch -c plan/incident-analysis
```

첫 단계에서는 랩이나 수집기 코드를 만들지 않습니다. 공식 사건자료, 법령 변화, 인증 방향을 조사하고 JY그룹 설계에 반영할 요구사항을 먼저 확정합니다.

## 8. 새 채팅으로 이동하기 전 마지막 작업

현재 채팅에서 변경한 내용을 Git에 반영하고 `PROJECT_STATE.md`를 갱신합니다. 그다음 새 채팅에 최신 저장소 ZIP 또는 GitHub 주소를 제공합니다. GitHub 주소만 제공할 때는 새 GPT가 저장소를 실제로 읽을 수 있는 환경인지 먼저 확인해야 합니다. 가장 확실한 방법은 최신 ZIP을 함께 첨부하는 것입니다.

## 9. 중요한 금지사항

- 새 GPT가 기존 문서를 읽지 않고 프로젝트를 재설계하게 두지 않습니다.
- 실제 개인정보와 기업 내부자료를 첨부하지 않습니다.
- `.env`, 비밀번호, 토큰과 SSH 개인키를 ZIP이나 Git에 넣지 않습니다.
- ISO 유료 원문을 저장소에 포함하지 않습니다.
- 자동수집 결과를 공식 인증판정으로 표현하지 않습니다.
- 현재 상태가 바뀌었는데 `PROJECT_STATE.md`를 갱신하지 않은 채 새 채팅으로 이동하지 않습니다.
