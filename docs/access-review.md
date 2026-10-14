# 원본 보존과 접근 검토

기록일: 2026-10-14
검토: 김준영
기준: ADR-015
상태: 작업중. 제출은 차단

## 보존

편집하는 폴더는 `C:\JY-Lab\JY-Group-Privacy-Audit`이다. `private-evidence`와 `zammad-runtime`은 그 형제 폴더로 둔다.

`C:\JY-Backup\2026-10-14`에 사본을 두었다. 아래 5개 파일은 원본과 SHA256이 같았다.

- `reports\JY-Audit-Workbook.xlsx`
- `private-evidence\before\users-before.json`
- `private-evidence\after\users-after-f01.json`
- `private-evidence\after\users-diff.json`
- `private-evidence\after\jy-doc02-copy.txt`

사본의 전체 파일 수와, 사본을 열어 보았는지는 이 기록에 없다. 이 복사는 Docker 볼륨 백업이 아니다. 런타임과 DB는 옮기거나 초기화하지 않았다.

## 공유

Drive의 원본 폴더 접근은 2026-10-14에 제한하지 않았다. 2차 점검 가이드가 관찰한 “링크를 가진 사람 편집 가능”은 오늘 공유 화면으로 다시 확인하지 않았다. 비밀값은 적지 않는다. `.env`의 비밀번호도 열거나 바꾸지 않았다.

원본 폴더의 일반 액세스를 제한하고, 별도 제출 폴더에는 검수가 끝난 ZIP만 두기 전에는 제출하지 않는다. 이미 전달된 링크의 사본까지 회수됐다고 적지 않는다. 실제 침해가 있었다는 결론도 적지 않는다.

## 아직 하지 않은 일

- Drive 공유를 제한됨으로 바꾸기
- 비로그인 창에서 원본 링크가 열리지 않는지 확인하기
- 자격증명 교체와 DB 접속 검증
- 제출용 폴더 만들기