# -*- coding: utf-8 -*-
"""발표 7장과 원고를 만든다.

실행: py -3 tools/build_briefing.py
"""

from __future__ import annotations

import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
PPTX = ROOT / "reports" / "JY-Briefing.pptx"
MANUSCRIPT = ROOT / "docs" / "18-slides.md"

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
CP = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC = "http://purl.org/dc/elements/1.1/"
DCTERMS = "http://purl.org/dc/terms/"
XSI = "http://www.w3.org/2001/XMLSchema-instance"

NAVY = "1B3A4B"
INK = "243038"
MUTED = "5C6B73"
PAPER = "F4F7F8"
WHITE = "FFFFFF"
SLIDE_CX = 12192000
SLIDE_CY = 6858000

SLIDES = [
    {
        "title": "문제 선택의 배경",
        "kicker": "1 / 7 · 가상 실습 · 2026-10-07 · 김준영",
        "bullets": [
            "상담 티켓에 이름, 이메일, 문의, 첨부가 남는다.",
            "범위는 로컬 Zammad 한 대다. 서버를 여러 대로 두지 않았다.",
            "목적 결정은 Retail, 상담은 Service, 유지보수는 Vendor다.",
            "이 발표는 실제 기업 감사와 인증이 아니다.",
            "가이드 PDF는 결과 보고서가 아니다.",
        ],
        "note": (
            "이 실습은 상담 티켓에 남는 개인정보를 로컬 Zammad 한 대로 본 것입니다. "
            "서버를 여러 대 두지 않은 이유는 범위가 상담 흐름 하나이기 때문입니다. "
            "실제 감사나 인증이 아니고, 가이드 PDF를 결과로 내지 않습니다."
        ),
    },
    {
        "title": "고객, 흐름, 범위",
        "kicker": "2 / 7 · 포함과 제외",
        "bullets": [
            "포함: 상담 목적, 상담 수행, 유지보수 권한.",
            "제외: 결제, 배송, 마케팅, 백업 복구 실측.",
            "직원 6명. 과거 기록의 고객 수는 삭제 전 10명, C01 삭제 후 9명이다. 2026-10-22에 다시 실측하지 않았다.",
            "F-01의 T02는 #52020이고 내부ID는 미확인이다. #52003(id 3)은 S04 정상업무의 다른 티켓이다.",
            "T11 시험본은 29번 52028. T12는 14번 52014. T15는 17번 52017.",
            "재점검이 적합이어도 처음의 Checks 미흡은 유지한다.",
        ],
        "note": (
            "포함은 Retail의 목적 결정, Service의 상담, Vendor의 유지보수입니다. "
            "결제와 배송, 마케팅, 백업 실측은 빼었습니다. "
            "직원은 여섯 명입니다. 고객 수 10명과 9명은 과거 기록이고, 오늘 다시 세지 않았습니다. "
            "F-01에서 본 T02는 #52020입니다. #52003은 S04의 정상업무 티켓이라 대상에서 뺐습니다. "
            "재점검이 맞아도 처음의 미흡 판정은 지우지 않습니다."
        ),
    },
    {
        "title": "기준, 방법, 증적",
        "kicker": "3 / 7 · 워크북과 화면 시험",
        "bullets": [
            "판정은 적합, 미흡, 미확인, 적용 제외다.",
            "워크북 Checks는 24행이다. 화면 시험은 F-01, F-02a, F-02b, F-03이다.",
            "과거 v1 수집은 localhost GET과 수동 비교였다. 현재 도구는 v2의 collect, diff, verify다. 이메일은 .example.test다.",
            "v2가 보는 값은 직원 6명의 active뿐이다. 세션, 그룹, 권한, 법적 적합성은 판정하지 않는다.",
            "발표 화면에는 evidence/sanitized의 공개 PNG를 넣는다. 원본은 C:\\JY-Lab\\private-evidence에 둔다.",
            "법령은 법 제21조 제1항과 제2항, 제26조 제4항과 제5항, 제29조, 영 제30조 제1항 제2호다.",
            "고시 제4조는 비어 있다. 추측으로 채우지 않았다.",
        ],
        "note": (
            "판정은 네 가지입니다. 워크북 스물네 행을 화면 시험으로 확인했습니다. "
            "과거 v1은 수동 비교이고, 현재 v2는 collect, diff, verify입니다. "
            "v2 결과는 active 변경만 보여 줍니다. 공개 화면은 sanitized에 있고 원본은 비공개 폴더에 있습니다. "
            "파기, 위탁 감독, 안전조치와 접근권한은 조문을 적었고 고시 제4조는 비워 두었습니다."
        ),
    },
    {
        "title": "F-01 종료 계정",
        "kicker": "4 / 7 · 6점·계획 · R-01 적합 · C02 미흡",
        "bullets": [
            "대상은 T02 #52020이다. 내부ID는 미확인이다. #52003(id 3)은 이 시험의 대상이 아니다.",
            "S05는 종료일 2026-09-14 이후에도 Active였고 #52020을 열람했다.",
            "조치 A-01: Active=false. 새 로그인을 차단했다. 공개 요약에서 바뀐 값은 S05의 active뿐이다.",
            "현재 위험은 6점·계획이다. 기존 세션은 미확인이라 잔여 점수를 넣지 않는다.",
            "재점검 R-01은 적합이다.",
            "공개 증적: 전 E-F01-B01, 후 E-F01-A01. 관측 시각은 파일에 없다.",
            "남김: Checks C02는 미흡이다. 기존 Sessions와 외부 토큰 회수는 미확인이다. 근본 기한은 2026-11-06이다.",
        ],
        "note": (
            "종료된 S05가 #52020을 열었습니다. #52003을 빼 둔 이유는 그 티켓이 S04 정상업무의 다른 인스턴스이기 때문입니다. "
            "계정을 끄고 새 로그인은 막았습니다. active 표도 S05만 바뀌었습니다. "
            "이미 열려 있던 세션은 확인하지 못했으므로 잔여 점수는 넣지 않습니다. Checks C02는 미흡으로 남습니다."
        ),
    },
    {
        "title": "F-02a 제한상담과 F-02b 조직 공유",
        "kicker": "5 / 7 · 각 6점·계획 · R-02a, R-02b 적합",
        "bullets": [
            "F-02a: S04와 S06이 제한상담 T11, 29번 52028을 열람했다.",
            "F-02a 조치: S04는 JY-General만, S06은 그룹이 없다. S03 Restricted full과 Accounts의 S02 Restricted, S01 Admin은 유지한다.",
            "F-02a 한계: 후 T11의 대상과 순서는 미확인이다. S06 차단 후 시험과 S03 후 시험은 미확인이다. E-F02-B02는 조치 전 증적이고 공개 PNG는 없다.",
            "F-02b: C02가 공유 조직에서 C01의 T01을 열람했다. 조치 후 확인한 것은 목록 숨김이다. 직접 주소와 첨부 거부는 미확인이다.",
            "현재 위험은 F-02a와 F-02b가 각 6점·계획이다. 두 잔여에는 점수를 넣지 않는다.",
            "재점검 R-02a와 R-02b는 적합이다.",
            "공개 증적: 전 E-F02-B01, E-F02-B03. 후 E-F02-A01, E-F02-A02, E-F02-A03. 관측 시각은 파일에 없다.",
            "남김: C03, C04, D02는 미흡이다. 근본 기한은 2026-11-06이다.",
        ],
        "note": (
            "F-02a와 F-02b를 나눈 이유는 제한상담 권한과 조직 공유가 다른 사실이기 때문입니다. "
            "그룹을 걷고 공유를 껐습니다. 목록에서 숨긴 것과 주소로 직접 여는 것을 막은 것은 다릅니다. "
            "직접 주소와 첨부 거부는 확인하지 못했습니다. 공유 설정이 예였던 것이고, 제품 취약점으로 적지 않습니다. "
            "상담 리더와 S02, S01의 제한 권한은 계정 기록에 맞게 유지합니다. "
            "재점검은 적합이고, 처음의 권한과 위탁 점검 기록은 미흡으로 남습니다."
        ),
    },
    {
        "title": "F-03 파기 범위",
        "kicker": "6 / 7 · 9점·우선 · R-03 미흡",
        "bullets": [
            "C01 자료 보안으로 T01과 T11은 삭제됐다. E02는 적합이다. 공개 전 화면은 E-F03-B01이다.",
            "T12 14번 52014 마커는 남았다. 공개 후 화면은 E-F03-A01, E-F03-A02이다.",
            "로컬 사본 jy-doc02-copy.txt는 관측했다. E-D03-A01의 공개 PNG는 없다.",
            "T15 17번 52017은 대조군으로 보존한다.",
            "완료 화면은 다시 보지 않았다. 백업 잔존과 복구는 미확인이라 그 범위에 점수를 넣지 않는다.",
            "현재 위험은 9점·우선이다. 재점검 R-03은 미흡이다.",
            "A-03은 2026-10-06 기한이 지났고 미완료다. 새 목표일과 다음 검토일은 2026-11-06이다. 담당은 S02, 실행은 S01이다.",
            "남김: E03, D03, F04는 미흡이다. T12는 미리보기 없이 삭제하지 않는다.",
        ],
        "note": (
            "자료 보안으로 본인 티켓은 지워졌습니다. 지운 범위는 그 티켓까지입니다. "
            "참조 티켓 T12와 PC에 받은 사본은 남았고, T15는 대조군으로 보존합니다. "
            "백업은 확인하지 않았습니다. 그래서 재점검은 미흡이고 현재 위험은 9점입니다. "
            "T12를 남겨 둔 이유는 잔존 증적을 유지하기 위해서이고, 위험수용으로 연 것은 아닙니다. "
            "다음 결정일은 2026-11-06입니다."
        ),
    },
    {
        "title": "결과, 잔여위험, 회고",
        "kicker": "7 / 7 · F-03 9점·우선 · 다음 보고 2026-11-06",
        "bullets": [
            "현재 위험: F-01, F-02a, F-02b는 각 6점·계획. F-03은 9점·우선.",
            "세션, 후 T11 순서, 직접 주소, 완료 화면, 백업처럼 발생이 미확인인 잔여에는 점수를 넣지 않는다.",
            "A-03은 미완료다. 담당 S02, 실행 S01, 새 목표일과 다음 보고일은 2026-11-06이다.",
            "추가 작업시간과 자원 견적은 근거가 없어 적지 않는다. 보완통제는 T12와 로컬 사본을 증적으로 유지하는 것이다.",
            "미확인: B04 권리 메일, E04 백업. 모의 기록은 실제 발송이 아니다.",
            "적용 제외: F03. 외부 AI에 연결하지 않았다.",
            "D01 수탁 계약 문서 미확인, D04 교육 서명 없음은 미흡이다. 양식과 교육 1쪽은 있다.",
            "main 35b7b85에는 태그 v1.0-final이 있다. 보완 브랜치 docs/closeout-deliverables-02는 아직 머지하지 않았다.",
            "다음: T12는 Scheduler 미리보기 1건 뒤에만 결정한다. down -v 는 하지 않는다.",
        ],
        "note": (
            "현재 위험은 세 건이 6점이고 F-03만 9점입니다. 확인하지 못한 잔여에는 점수를 넣지 않았습니다. "
            "A-03의 다음 보고일은 2026-11-06이고 담당은 S02입니다. "
            "권리 메일과 백업은 미확인입니다. 교육 서명과 수탁 계약 확인도 미흡입니다. "
            "main에는 풀 리퀘스트 #3부터 #7의 병합과 태그 v1.0-final이 있다. "
            "보완 브랜치 docs/closeout-deliverables-02는 아직 머지하지 않았다. "
            "다음은 T12를 미리보기 한 건 뒤에만 결정하는 것입니다. "
            "예상 질문. 왜 Zammad 한 대인가. 상담 흐름 하나만 범위로 잡았기 때문이다. "
            "재점검이 적합인데 Checks가 미흡인 이유. 재점검은 조치 후이고 Checks는 처음 발견을 유지한다. "
            "고객을 지운 뒤에도 F-03이 미흡인 이유. T12와 로컬 사본이 남았기 때문이다. "
            "수집기를 어떻게 신뢰했는가. v2는 active만 보고, 화면 증적과 대조했다. "
            "백업과 Sessions를 미확인으로 남긴 이유. 범위 밖이거나 화면에서 확인하지 못했다. "
            "실제 기업 감사와 다른 점. 가상 계정이고 실제 신고와 메일이 없으며 인증 결과가 아니다."
        ),
    },
]

SAN = ROOT / "evidence" / "sanitized"
SLIDE_IMAGES = {
    4: [
        ("E-F01-B01.png", "전 #52020. 세션은 이 화면 밖"),
        ("E-F01-A01.png", "후 새 로그인 차단. 세션 미확인"),
    ],
    5: [
        ("E-F02-B01.png", "전 제한상담 열람"),
        ("E-F02-A03.png", "후 목록 숨김. 직접 주소는 미확인"),
    ],
    6: [
        ("E-F03-B01.png", "삭제 전 미리보기. 완료 화면 아님"),
        ("E-F03-A01.png", "T12 잔존. 백업은 미확인"),
    ],
}


def png_px(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    return 16, 9


def fit(width: int, height: int, box_w: int, box_h: int) -> tuple[int, int]:
    scale = min(box_w / width, box_h / height)
    return max(1, int(width * scale)), max(1, int(height * scale))


def picture(
    shape_id: int, name: str, rel_id: str, x: int, y: int, cx: int, cy: int
) -> str:
    return (
        "<p:pic>"
        "<p:nvPicPr>"
        f'<p:cNvPr id="{shape_id}" name="{esc(name)}"/>'
        '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
        "<p:nvPr/>"
        "</p:nvPicPr>"
        "<p:blipFill>"
        f'<a:blip r:embed="{rel_id}"/>'
        "<a:stretch><a:fillRect/></a:stretch>"
        "</p:blipFill>"
        "<p:spPr>"
        "<a:xfrm>"
        f'<a:off x="{x}" y="{y}"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/>'
        "</a:xfrm>"
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        "</p:spPr>"
        "</p:pic>"
    )


def image_column(images: list[tuple[str, str]]) -> str:
    top = 1560000
    height = 4600000
    gap = 140000
    slot = (height - gap * (len(images) - 1)) // len(images)
    caption_h = 360000
    box_w = 4700000
    left = 7050000
    chunks = []
    shape_id = 10
    for index, (filename, caption) in enumerate(images):
        width, height_px = png_px(SAN / filename)
        cx, cy = fit(width, height_px, box_w, slot - caption_h)
        y = top + index * (slot + gap)
        x = left + (box_w - cx) // 2
        chunks.append(picture(shape_id, filename, f"rId{index + 3}", x, y, cx, cy))
        shape_id += 1
        chunks.append(
            shape(
                shape_id,
                f"Cap{index}",
                left,
                y + cy,
                box_w,
                caption_h,
                None,
                paragraph(caption, 1100, False, MUTED, "ctr"),
                "ctr",
            )
        )
        shape_id += 1
    return "".join(chunks)


def esc(text: str) -> str:
    return escape(text)


def paragraph(
    text: str,
    size: int,
    bold: bool,
    color: str,
    align: str = "l",
    before: int = 0,
    after: int = 0,
) -> str:
    b = ' b="1"' if bold else ""
    return (
        "<a:p>"
        f'<a:pPr algn="{align}" marL="0">'
        f'<a:spcBef><a:spcPts val="{before}"/></a:spcBef>'
        f'<a:spcAft><a:spcPts val="{after}"/></a:spcAft>'
        "</a:pPr>"
        "<a:r>"
        f'<a:rPr lang="ko-KR" sz="{size}"{b} dirty="0">'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        '<a:latin typeface="Malgun Gothic"/>'
        '<a:ea typeface="Malgun Gothic"/>'
        '<a:cs typeface="Malgun Gothic"/>'
        "</a:rPr>"
        f"<a:t>{esc(text)}</a:t>"
        "</a:r>"
        "</a:p>"
    )


def shape(
    shape_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    fill: str | None,
    paragraphs: str,
    anchor: str = "t",
) -> str:
    if fill:
        fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln>'
    else:
        fill_xml = "<a:noFill/><a:ln><a:noFill/></a:ln>"
    return (
        "<p:sp>"
        "<p:nvSpPr>"
        f'<p:cNvPr id="{shape_id}" name="{esc(name)}"/>'
        "<p:cNvSpPr/>"
        "<p:nvPr/>"
        "</p:nvSpPr>"
        "<p:spPr>"
        "<a:xfrm>"
        f'<a:off x="{x}" y="{y}"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/>'
        "</a:xfrm>"
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f"{fill_xml}"
        "</p:spPr>"
        "<p:txBody>"
        f'<a:bodyPr wrap="square" lIns="274320" tIns="90000" rIns="274320" bIns="60000" anchor="{anchor}"/>'
        "<a:lstStyle/>"
        f"{paragraphs}"
        "</p:txBody>"
        "</p:sp>"
    )


def slide_xml(item: dict) -> str:
    images = item.get("images") or []
    bullet_size = 1500 if images else 2000
    bullet_gap = 40 if images else 80
    body_cx = 6400000 if images else 11300000
    bullets = "".join(
        paragraph(
            "·  " + line, bullet_size, False, INK, before=bullet_gap, after=bullet_gap
        )
        for line in item["bullets"]
    )
    title = paragraph(item["title"], 3200, True, WHITE)
    kicker = paragraph(item["kicker"], 1400, False, MUTED, before=0, after=0)
    tree = [
        shape(2, "TitleBar", 0, 0, SLIDE_CX, 980000, NAVY, title, "ctr"),
        shape(3, "Kicker", 420000, 1080000, 11300000, 360000, None, kicker, "ctr"),
        shape(4, "Body", 420000, 1500000, body_cx, 4700000, None, bullets, "t"),
    ]
    if images:
        tree.append(image_column(images))
    tree.append(
        shape(
            5,
            "Footer",
            0,
            6400000,
            SLIDE_CX,
            458000,
            PAPER,
            paragraph(
                "가상 실습 · 인증 발표 아님 · 공개 화면은 evidence/sanitized",
                1200,
                False,
                MUTED,
                "r",
            ),
            "ctr",
        )
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<p:sld xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}">'
        "<p:cSld><p:spTree>"
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        f"{''.join(tree)}"
        "</p:spTree></p:cSld>"
        "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>"
        "</p:sld>"
    )


def notes_xml(text: str) -> str:
    chunks = text.split("예상 질문. ")
    paragraphs = paragraph(chunks[0].strip(), 1400, False, INK, before=40, after=80)
    if len(chunks) == 2:
        paragraphs += paragraph("예상 질문", 1400, True, NAVY, before=80, after=40)
        paragraphs += paragraph(
            chunks[1].strip(), 1300, False, INK, before=20, after=20
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<p:notes xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}">'
        "<p:cSld><p:spTree>"
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Notes"/>'
        '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        '<p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>'
        "<p:spPr/>"
        "<p:txBody><a:bodyPr/><a:lstStyle/>"
        f"{paragraphs}"
        "</p:txBody></p:sp>"
        "</p:spTree></p:cSld>"
        "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>"
        "</p:notes>"
    )


def manuscript() -> str:
    lines = [
        "# 18장 발표 슬라이드 7장 원고",
        "",
        "작성일: 2026-10-07",
        "재검토일: 2026-10-22",
        "형식 파일: `reports/JY-Briefing.pptx`",
        "발표 화면에는 `evidence/sanitized`의 공개 PNG만 넣는다. 원본은 `C:\\JY-Lab\\private-evidence\\`에만 둔다.",
        "가상 실습. 인증 발표가 아님. 가이드 PDF는 결과가 아니다.",
        "",
    ]
    for index, item in enumerate(SLIDES, start=1):
        lines.append(f"## {index}. {item['title']}")
        lines.append("")
        lines.extend(f"- {bullet}" for bullet in item["bullets"])
        lines.append("")
        lines.append(f"발표 메모: {item['note']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


THEME = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="{A}" name="JY"><a:themeElements>
<a:clrScheme name="JY"><a:dk1><a:srgbClr val="243038"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
<a:dk2><a:srgbClr val="1B3A4B"/></a:dk2><a:lt2><a:srgbClr val="F4F7F8"/></a:lt2>
<a:accent1><a:srgbClr val="1B3A4B"/></a:accent1><a:accent2><a:srgbClr val="5C6B73"/></a:accent2>
<a:accent3><a:srgbClr val="8A5A2A"/></a:accent3><a:accent4><a:srgbClr val="1B3A4B"/></a:accent4>
<a:accent5><a:srgbClr val="5C6B73"/></a:accent5><a:accent6><a:srgbClr val="243038"/></a:accent6>
<a:hlink><a:srgbClr val="1B3A4B"/></a:hlink><a:folHlink><a:srgbClr val="5C6B73"/></a:folHlink></a:clrScheme>
<a:fontScheme name="JY"><a:majorFont><a:latin typeface="Malgun Gothic"/><a:ea typeface="Malgun Gothic"/><a:cs typeface="Malgun Gothic"/></a:majorFont>
<a:minorFont><a:latin typeface="Malgun Gothic"/><a:ea typeface="Malgun Gothic"/><a:cs typeface="Malgun Gothic"/></a:minorFont></a:fontScheme>
<a:fmtScheme name="JY"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
</a:fmtScheme></a:themeElements></a:theme>'''

SLIDE_MASTER = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}">
<p:cSld><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
</p:spTree></p:cSld>
<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
</p:sldMaster>'''

SLIDE_LAYOUT = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}" type="blank" preserve="1">
<p:cSld name="Blank"><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
</p:spTree></p:cSld>
<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>'''

NOTES_MASTER = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notesMaster xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}">
<p:cSld><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
<p:sp><p:nvSpPr><p:cNvPr id="2" name="Notes"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>
<p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="ko-KR"/></a:p></p:txBody></p:sp>
</p:spTree></p:cSld>
<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
</p:notesMaster>'''


def content_types() -> str:
    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>',
        '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>',
        '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(1, 8):
        overrides.append(
            f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        )
        overrides.append(
            f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
        )
    body = "\n  ".join(overrides)
    return (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'<Types xmlns="{CT}">\n'
        '  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
        '  <Default Extension="xml" ContentType="application/xml"/>\n'
        '  <Default Extension="png" ContentType="image/png"/>\n'
        f"  {body}\n</Types>"
    )


def presentation_xml() -> str:
    ids = []
    for i in range(7):
        ids.append(f'<p:sldId id="{256 + i}" r:id="rId{i + 3}"/>')
    return (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<p:presentation xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}" saveSubsetFonts="1">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        '<p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst>'
        f"<p:sldIdLst>{''.join(ids)}</p:sldIdLst>"
        f'<p:sldSz cx="{SLIDE_CX}" cy="{SLIDE_CY}" type="screen16x9"/>'
        '<p:notesSz cx="6858000" cy="9144000"/>'
        "</p:presentation>"
    )


def presentation_rels() -> str:
    rows = [
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>',
    ]
    for i in range(1, 8):
        rows.append(
            f'<Relationship Id="rId{i + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        )
    rows.append(
        '<Relationship Id="rId10" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>'
    )
    rows.append(
        '<Relationship Id="rId11" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps" Target="viewProps.xml"/>'
    )
    rows.append(
        '<Relationship Id="rId12" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles" Target="tableStyles.xml"/>'
    )
    body = "\n  ".join(rows)
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="{REL}">\n  {body}\n</Relationships>'


def rels_one(rel_id: str, rel_type: str, target: str) -> str:
    return (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{REL}">'
        f'<Relationship Id="{rel_id}" Type="{rel_type}" Target="{target}"/>'
        f"</Relationships>"
    )


def slide_rels(note_number: int, image_names: list[str]) -> str:
    rows = [
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>',
        f'<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{note_number}.xml"/>',
    ]
    for index, name in enumerate(image_names, start=3):
        rows.append(
            f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{name}"/>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{REL}">{"".join(rows)}</Relationships>'
    )


CORE = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="{CP}" xmlns:dc="{DC}" xmlns:dcterms="{DCTERMS}" xmlns:xsi="{XSI}">
  <dc:title>JY Group 상담 시스템 개인정보 진단</dc:title>
  <dc:creator>김준영</dc:creator>
  <cp:lastModifiedBy>수행자</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-10-19T02:10:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-10-19T02:10:00Z</dcterms:modified>
</cp:coreProperties>'''

APP = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>JY briefing</Application>
  <Slides>7</Slides>
  <PresentationFormat>Widescreen</PresentationFormat>
</Properties>"""


def assert_package(path: Path, text: str) -> None:
    required = [
        "문제 선택의 배경",
        "F-01",
        "F-02",
        "F-03",
        "R-03",
        "C02",
        "D01",
        "D04",
        "B04",
        "E04",
        "52014",
        "52028",
        "52020",
        "6점·계획",
        "고시 제4조",
        "docs/closeout-deliverables-02",
        "왜 Zammad 한 대인가",
        "재점검이 적합인데 Checks가 미흡인 이유",
        "수집기를 어떻게 신뢰했는가",
        "백업과 Sessions를 미확인으로 남긴 이유",
        "실제 기업 감사와 다른 점",
    ]
    for token in required:
        if token not in text:
            raise SystemExit(f"발표 자료에 {token} 이 없다.")
    banned = [
        "항·호는 원문 후",
        "원문 확인 전에",
        "수료 완료",
        "인증 취득",
        "PR 머지 완료",
    ]
    for token in banned:
        if token in text:
            raise SystemExit(f"빼야 할 문장이 있다: {token}")
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
    for i in range(1, 8):
        for part in (f"ppt/slides/slide{i}.xml", f"ppt/notesSlides/notesSlide{i}.xml"):
            if part not in names:
                raise SystemExit(f"{part} 이 없다.")


def write_pptx(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    chunks = []
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types())
        zf.writestr(
            "_rels/.rels",
            rels_one(
                "rId1",
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument",
                "ppt/presentation.xml",
            ).replace(
                "</Relationships>",
                '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                "</Relationships>",
            ),
        )
        zf.writestr("ppt/presentation.xml", presentation_xml())
        zf.writestr("ppt/_rels/presentation.xml.rels", presentation_rels())
        zf.writestr("ppt/slideMasters/slideMaster1.xml", SLIDE_MASTER)
        zf.writestr(
            "ppt/slideMasters/_rels/slideMaster1.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="{REL}">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
            "</Relationships>",
        )
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", SLIDE_LAYOUT)
        zf.writestr(
            "ppt/slideLayouts/_rels/slideLayout1.xml.rels",
            rels_one(
                "rId1",
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster",
                "../slideMasters/slideMaster1.xml",
            ),
        )
        zf.writestr("ppt/notesMasters/notesMaster1.xml", NOTES_MASTER)
        zf.writestr(
            "ppt/notesMasters/_rels/notesMaster1.xml.rels",
            rels_one(
                "rId1",
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme",
                "../theme/theme1.xml",
            ),
        )
        zf.writestr("ppt/theme/theme1.xml", THEME)
        zf.writestr(
            "ppt/presProps.xml",
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentationPr xmlns:p="{P}" xmlns:a="{A}"/>',
        )
        zf.writestr(
            "ppt/viewProps.xml",
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:viewPr xmlns:a="{A}" xmlns:p="{P}"><p:normalViewPr><p:restoredLeft sz="15620"/><p:restoredTop sz="94660"/></p:normalViewPr><p:slideViewPr><p:cSldViewPr><p:cViewPr varScale="1"><p:scale><a:sx n="100" d="100"/><a:sy n="100" d="100"/></p:scale><p:origin x="0" y="0"/></p:cViewPr></p:cSldViewPr></p:slideViewPr><p:notesTextViewPr><p:cViewPr><p:scale><a:sx n="100" d="100"/><a:sy n="100" d="100"/></p:scale><p:origin x="0" y="0"/></p:cViewPr></p:notesTextViewPr></p:viewPr>',
        )
        zf.writestr(
            "ppt/tableStyles.xml",
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:tblStyleLst xmlns:a="{A}" def="{{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}}"/>',
        )
        zf.writestr("docProps/core.xml", CORE)
        zf.writestr("docProps/app.xml", APP)
        for i, item in enumerate(SLIDES, start=1):
            shown = dict(item)
            shown["images"] = SLIDE_IMAGES.get(i, [])
            xml = slide_xml(shown)
            note = notes_xml(item["note"])
            chunks.append(xml)
            chunks.append(note)
            zf.writestr(f"ppt/slides/slide{i}.xml", xml)
            image_names = []
            for filename, _caption in shown["images"]:
                source = SAN / filename
                if not source.exists():
                    raise SystemExit(f"공개 화면이 없다: {source}")
                zf.write(source, f"ppt/media/{filename}")
                image_names.append(filename)
            zf.writestr(
                f"ppt/slides/_rels/slide{i}.xml.rels",
                slide_rels(i, image_names),
            )
            zf.writestr(f"ppt/notesSlides/notesSlide{i}.xml", note)
            zf.writestr(
                f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<Relationships xmlns="{REL}">'
                f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="../notesMasters/notesMaster1.xml"/>'
                f'<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide{i}.xml"/>'
                "</Relationships>",
            )
    return "".join(chunks)


def main() -> None:
    text = write_pptx(PPTX)
    script = manuscript()
    MANUSCRIPT.write_text(script, encoding="utf-8")
    assert_package(PPTX, text + script)
    print(f"{PPTX.name}\t{PPTX.stat().st_size}")
    print(f"{MANUSCRIPT.name}\t{MANUSCRIPT.stat().st_size}")
    print("slides\t7")


if __name__ == "__main__":
    main()
