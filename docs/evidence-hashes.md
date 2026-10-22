# 증적 해시

확인일: 2026-10-12
원본 위치: `C:\JY-Lab\private-evidence\`
원본과 `sha256-manifest.txt`는 Git에 넣지 않는다. 이 문서는 경로와 SHA256만 담는다.

`before\users-before.json.sha256`와 `after\users-after-f01.json.sha256`는 아래 해시와 같다. `users-diff.json`은 수집기에 diff 명령이 없어 옆자리 해시 파일이 없고, 이 목록의 해시만 기록한다.

| 경로 | SHA256 |
| --- | --- |
| after\E-F01-A01-S05-login-blocked.png | e0e8f4b36b38f969ba39bd63e96d07343d0886f253c5982f5560c648b3860a68 |
| after\E-F02-A01-S04-T11-denied.png | 820e8d35e734b01665b54b1f9f22e9809b25c1f1f24907c3a204bce2a4f72b9c |
| after\E-F02-A01-S04-T11-denied-T02tab.png | 47f8f8473cdf75bea008f2a673430ac2601e154aada4f4988196ba1e8c2bb2c6 |
| after\E-F02-A02-S04-T02-ok.png | a1a72fac7d94227e05261979a13a2e1de81bf2b6800901b0492ad8ebadef8a79 |
| after\E-F02-A03-C02-no-T01.png | 56f7e61008c2ed480a37a9499f4b2f20125bbe7dbd53e81ecbf5569b653fdd1c |
| after\E-F03-A01-T12-residual.png | 0c878a3fbcdea9d5d7dd5ea3e1a3b3964e5040cfce49f4460f976eab10ecdd23 |
| after\E-F03-A02-T15-preserved.png | 5b576280c64b3e30b77034cbe4a37e40ddbb166fbff2beaf33fde7dc3708a553 |
| after\jy-doc02-copy.txt | 6f0ba336b53f81fbf7da509798b8219f726c4e4b421e22772cf92a7514053c2b |
| after\users-after-f01.json | 1ee5dd42af94a4a38eb62827df3b659aa84e88aeafa85334f5d618f8ffab0224 |
| after\users-diff.json | fb3a3d9489ea34b8592ba30c29235561ad6791b0c64211733a875dde32f67882 |
| before\E-F01-B01-S05-active-T02.png | 11eca98be3060702da44a8db353f0f54a57defda2c15db308e3e1d54cb04957d |
| before\E-F02-B01-S04-T11.png | bb5d1cb3c45c6bf486506fa5d6e539c02502bd080d5af54b8d7e3cd9509c932c |
| before\E-F02-B02-S06-T11.png | e59e461108afca1876d9391731187a1efba1f1073bf3789fb0d7168a6e801c54 |
| before\E-F02-B03-C02-sees-T01.png | 24aa3ebeae227353e9de1e545987a30f133f1b814de7aa09f34037563644ac50 |
| before\E-F03-B01-C01-preview.png | dfbd99cd39f5b3f0b3068eec58eea47e1473413ddd72ab44f0fa6379aad8da2e |
| before\E-F03-B02-T12-marker.png | e6b1424a80d6a20581d38278d80d12cbca3225db4b9ac67a61526582624b9b46 |
| before\E-F03-B03-T15-control.png | 3ba3ed20a657a2ac4cb8336f3474531f7f997301e7ddfc9765a01fc75ca14c3c |
| before\users-before.json | 733293c02e65f593dddab16b6ce7505bb7e843cd20a67042c7ce1b031f527338 |
| ENV-01-system-base.png | faa8108fed50c17353c0080469ed989642bfd90eb35fb4745e53f1de1481edcb |
| ENV-01-version.txt | 7274bb1e848d671e25c2ca7fccae4dd74922a7df73a6a883c3eebd4f006b8b0c |
| ENV-02-local-port.txt | 0c0b19d3ee6090021b8cb62a1129825c6d7f04747df185c9d922fbafc1ac7314 |

점검 판정은 바꾸지 않는다. 이 목록은 2026-10-12에 계산한 해시이며 재시험이 아니다.

## 2026-10-14 재계산

같은 파일을 다시 해시했다. 재시험은 아니다. 2026-10-12 목록과 같으면 그 값을 유지한다.

| 경로 | SHA256 | 2026-10-12 목록 |
| --- | --- | --- |
| before\users-before.json | 733293c02e65f593dddab16b6ce7505bb7e843cd20a67042c7ce1b031f527338 | 같음 |
| after\users-after-f01.json | 1ee5dd42af94a4a38eb62827df3b659aa84e88aeafa85334f5d618f8ffab0224 | 같음 |
| after\users-diff.json | fb3a3d9489ea34b8592ba30c29235561ad6791b0c64211733a875dde32f67882 | 같음 |
| after\jy-doc02-copy.txt | 6f0ba336b53f81fbf7da509798b8219f726c4e4b421e22772cf92a7514053c2b | 같음 |
| ENV-01-system-base.png | faa8108fed50c17353c0080469ed989642bfd90eb35fb4745e53f1de1481edcb | 같음 |
| ENV-01-version.txt | 7274bb1e848d671e25c2ca7fccae4dd74922a7df73a6a883c3eebd4f006b8b0c | 같음 |
| ENV-02-local-port.txt | 0c0b19d3ee6090021b8cb62a1129825c6d7f04747df185c9d922fbafc1ac7314 | 같음 |
| docs\data-flow.pdf | d94f7cb9cf1191f79a34df5c13061239aa5fdb0f884ada71483c7743c69f023f | 이전 목록에 없음. 워크북 DF-01 H4를 이날 채움 |

워크북 Evidence H2·H3·H5는 비어 있었고, 위 해시와 같다. H4는 이날의 첫 계산이다. 표시는 보완 시점 계산이다.

## 2026-10-15 공개 가공본

10개 PNG를 evidence/sanitized에 복사했다. 화면을 열어 토큰·암호·실명이 없는지 봤다. 가릴 글자가 없어 가공본 SHA256은 원본과 같다. 글자를 덧그리지 않았다.

| 파일 | SHA256 |
| --- | --- |
| evidence/sanitized/E-F01-B01.png | 11eca98be3060702da44a8db353f0f54a57defda2c15db308e3e1d54cb04957d |
| evidence/sanitized/E-F01-A01.png | e0e8f4b36b38f969ba39bd63e96d07343d0886f253c5982f5560c648b3860a68 |
| evidence/sanitized/E-F02-B01.png | bb5d1cb3c45c6bf486506fa5d6e539c02502bd080d5af54b8d7e3cd9509c932c |
| evidence/sanitized/E-F02-A01.png | 820e8d35e734b01665b54b1f9f22e9809b25c1f1f24907c3a204bce2a4f72b9c |
| evidence/sanitized/E-F02-A02.png | a1a72fac7d94227e05261979a13a2e1de81bf2b6800901b0492ad8ebadef8a79 |
| evidence/sanitized/E-F02-B03.png | 24aa3ebeae227353e9de1e545987a30f133f1b814de7aa09f34037563644ac50 |
| evidence/sanitized/E-F02-A03.png | 56f7e61008c2ed480a37a9499f4b2f20125bbe7dbd53e81ecbf5569b653fdd1c |
| evidence/sanitized/E-F03-B01.png | dfbd99cd39f5b3f0b3068eec58eea47e1473413ddd72ab44f0fa6379aad8da2e |
| evidence/sanitized/E-F03-A01.png | 0c878a3fbcdea9d5d7dd5ea3e1a3b3964e5040cfce49f4460f976eab10ecdd23 |
| evidence/sanitized/E-F03-A02.png | 5b576280c64b3e30b77034cbe4a37e40ddbb166fbff2beaf33fde7dc3708a553 |

식별 한계는 워크북 Evidence K열에 있다. 원본 PNG와 원본 JSON은 Git에 넣지 않는다.

## 2026-10-15 계정 active 요약

원본 users JSON은 공개하지 않는다. Accounts 시트의 이메일과 대조해 직원ID와 active만 evidence/sanitized/users-active.csv에 남겼다. S05만 true에서 false로 바뀌었다. SHA256은 5680e5263c36d398ead884fb6810be17781ce622346fcc62d40126c0ec72c783이다.

## 2026-10-22 흐름도 문장 정정

`docs/data-flow.pdf`의 사본 문장을 고친 뒤 다시 해시했다. 재시험은 아니다. 이전 해시는 이력으로 남긴다.

| 경로 | SHA256 | 이전 |
| --- | --- | --- |
| docs/data-flow.pdf | d94e86cd325051ff98b8f4dcd9de31e4440fba6d1c48321e416e498998c51347 | d94f7cb9cf1191f79a34df5c13061239aa5fdb0f884ada71483c7743c69f023f |