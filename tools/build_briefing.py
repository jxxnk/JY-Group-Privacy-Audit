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
        "kicker": "1 / 7  ·  가상 실습  ·  2026-10-07  ·  김준영",
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
        "kicker": "2 / 7  ·  포함과 제외",
        "bullets": [
            "포함: 상담 목적, 상담 수행, 유지보수 권한.",
            "제외: 결제, 배송, 마케팅, 백업 복구 실측.",
            "직원 6명. 고객은 삭제 전 10명, C01 삭제 후 9명.",
            "T02는 3번 52003. T11 시험본은 29번 52028.",
            "T12는 14번 52014. T15는 17번 52017.",
            "재점검이 적합이어도 처음의 Checks 미흡은 유지한다.",
        ],
        "note": (
            "포함은 Retail의 목적 결정, Service의 상담, Vendor의 유지보수입니다. "
            "결제와 배송, 마케팅, 백업 실측은 빼었습니다. "
            "직원은 여섯 명이고, 고객은 C01을 지우기 전 열 명입니다. "
            "재점검이 맞아도 처음의 미흡 판정은 지우지 않습니다."
        ),
    },
    {
        "title": "기준, 방법, 증적",
        "kicker": "3 / 7  ·  워크북과 화면 시험",
        "bullets": [
            "판정은 적합, 미흡, 미확인, 적용 제외다.",
            "워크북 Checks는 24행이다. 화면 시험은 F-01, F-02, F-03이다.",
            "수집기는 localhost GET만 한다. 이메일은 .example.test다.",
            "원본 증적은 C:\\JY-Lab\\private-evidence 에 둔다. 발표에는 증적 ID만 말한다.",
            "법령은 법 제21조 제1항과 제2항, 제26조 제4항과 제5항, 제29조, 영 제30조 제1항 제2호다.",
            "고시 제4조는 비어 있다. 추측으로 채우지 않았다.",
        ],
        "note": (
            "판정은 네 가지입니다. 워크북 스물네 행을 화면 시험 세 건으로 확인했습니다. "
            "수집기는 이 컴퓨터의 localhost만 호출하고, 토큰은 출력하지 않습니다. "
            "화면 원본은 비공개 폴더에 있고 여기에는 증적 번호만 말합니다. "
            "파기, 위탁 감독, 안전조치와 접근권한은 조문을 적었고 고시 제4조는 비워 두었습니다."
        ),
    },
    {
        "title": "F-01  종료 계정",
        "kicker": "4 / 7  ·  재점검 R-01 적합  ·  Checks C02 미흡",
        "bullets": [
            "S05는 종료일 2026-09-14 이후에도 Active였고 T02를 열람했다.",
            "조치 A-01: Active=false. 새 로그인을 차단했다.",
            "재점검 R-01은 적합이다.",
            "증적: E-F01-B01, E-F01-A01, JSON-F01-DIFF.",
            "남김: Checks C02는 미흡이다. 기존 Sessions 회수는 미확인이다.",
        ],
        "note": (
            "종료된 S05가 활성 상태로 T02를 열었습니다. 계정을 끄고 새 로그인은 막았습니다. "
            "재점검은 적합입니다. 다만 이미 열려 있던 세션을 걷어냈는지는 화면에서 확인하지 못했습니다. "
            "그래서 Checks C02는 미흡으로 남습니다."
        ),
    },
    {
        "title": "F-02  최소권한",
        "kicker": "5 / 7  ·  R-02a, R-02b 적합  ·  C03, C04, D02 미흡",
        "bullets": [
            "S04와 S06이 제한상담 T11, 29번 52028을 열람했다.",
            "C02는 공유 조직에서 C01의 T01을 열람했다.",
            "조치: S04는 General만, S06은 그룹이 없고, 공유는 아니오. S03 Restricted는 유지.",
            "재점검 R-02a와 R-02b는 적합이다.",
            "증적: E-F02-A01, E-F02-A02, E-F02-A03.",
            "남김: C03, C04, D02는 미흡이다.",
        ],
        "note": (
            "일반 상담과 유지보수가 제한 티켓을 봤고, 다른 고객이 공유 조직에서 티켓을 봤습니다. "
            "그룹을 걷고 공유를 껐습니다. 상담 리더의 제한 권한은 설계상 유지합니다. "
            "재점검은 적합이고, 처음의 권한과 위탁 점검 기록은 미흡으로 남습니다."
        ),
    },
    {
        "title": "F-03  파기 범위",
        "kicker": "6 / 7  ·  E02 적합  ·  R-03 미흡",
        "bullets": [
            "C01 자료 보안으로 T01과 T11은 삭제됐다. E02는 적합이다.",
            "T12 마커와 jy-doc02 로컬 사본은 남았다. T15는 보존한다.",
            "재점검 R-03은 미흡이다. T12는 증적이라 삭제하지 않았다. A-03은 예정이다.",
            "증적: E-F03-A01, E-F03-A02, E-D03-A01.",
            "남김: E03, D03, F04는 미흡이다.",
        ],
        "note": (
            "자료 보안으로 본인 티켓 둘은 지워졌습니다. 참조 티켓 T12와 PC에 받은 사본은 남았고, T15는 보존합니다. "
            "그래서 재점검은 미흡입니다. T12는 증적이라 미리보기 한 건 전에는 지우지 않습니다."
        ),
    },
    {
        "title": "결과, 잔여위험, 회고",
        "kicker": "7 / 7  ·  PR과 태그는 아직 없다",
        "bullets": [
            "미확인: B04 권리 메일, E04 백업. 모의 기록은 실제 발송이 아니다.",
            "적용 제외: F03. 외부 AI에 연결하지 않았다.",
            "D01 수탁 연간 실적과 D04 교육 서명은 미흡이다. 양식만 있다.",
            "브랜치 docs/closeout-deliverables-02 는 푸시했다. PR, 태그, Release는 없다.",
            "다음: T12는 Scheduler 미리보기 1건 뒤에만 결정한다. down -v 는 하지 않는다.",
        ],
        "note": (
            "권리 메일과 백업은 미확인입니다. 교육 서명과 수탁 연간 실적도 미흡입니다. "
            "브랜치는 올렸고 PR과 태그는 없습니다. 다음은 T12를 미리보기 한 건 뒤에만 결정하는 것입니다. "
            "예상 질문. 왜 Zammad 한 대인가. 상담 흐름 하나만 범위로 잡았기 때문이다. "
            "재점검이 적합인데 Checks가 미흡인 이유. 재점검은 조치 후이고 Checks는 처음 발견을 유지한다. "
            "고객을 지운 뒤에도 F-03이 미흡인 이유. T12와 로컬 사본이 남았기 때문이다. "
            "수집기를 어떻게 신뢰했는가. localhost GET과 화면 증적을 대조했고 토큰은 출력하지 않는다. "
            "백업과 Sessions를 미확인으로 남긴 이유. 범위 밖이거나 화면에서 확인하지 못했다. "
            "실제 기업 감사와 다른 점. 가상 계정이고 실제 신고와 메일이 없으며 인증 결과가 아니다."
        ),
    },
]


def esc(text: str) -> str:
    return escape(text)


def paragraph(text: str, size: int, bold: bool, color: str, align: str = "l", before: int = 0, after: int = 0) -> str:
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


def shape(shape_id: int, name: str, x: int, y: int, cx: int, cy: int, fill: str | None, paragraphs: str, anchor: str = "t") -> str:
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
    bullets = "".join(
        paragraph("·  " + line, 2000, False, INK, before=80, after=80)
        for line in item["bullets"]
    )
    title = paragraph(item["title"], 3200, True, WHITE)
    kicker = paragraph(item["kicker"], 1400, False, MUTED, before=0, after=0)
    tree = "".join(
        [
            shape(2, "TitleBar", 0, 0, SLIDE_CX, 980000, NAVY, title, "ctr"),
            shape(3, "Kicker", 420000, 1080000, 11300000, 360000, None, kicker, "ctr"),
            shape(4, "Body", 420000, 1500000, 11300000, 4700000, None, bullets, "t"),
            shape(
                5,
                "Footer",
                0,
                6400000,
                SLIDE_CX,
                458000,
                PAPER,
                paragraph("가상 실습  ·  인증 발표 아님  ·  스크린샷 없음  ·  증적 ID만 표시", 1200, False, MUTED, "r"),
                "ctr",
            ),
        ]
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<p:sld xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}">'
        "<p:cSld><p:spTree>"
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        "<p:grpSpPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"0\" cy=\"0\"/>"
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        f"{tree}"
        "</p:spTree></p:cSld>"
        "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>"
        "</p:sld>"
    )


def notes_xml(text: str) -> str:
    chunks = text.split("예상 질문. ")
    paragraphs = paragraph(chunks[0].strip(), 1400, False, INK, before=40, after=80)
    if len(chunks) == 2:
        paragraphs += paragraph("예상 질문", 1400, True, NAVY, before=80, after=40)
        paragraphs += paragraph(chunks[1].strip(), 1300, False, INK, before=20, after=20)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<p:notes xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}">'
        "<p:cSld><p:spTree>"
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        "<p:grpSpPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"0\" cy=\"0\"/>"
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        "<p:sp><p:nvSpPr><p:cNvPr id=\"2\" name=\"Notes\"/>"
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
        "형식 파일: 2026-10-19 `reports/JY-Briefing.pptx`",
        "스크린샷은 넣지 않는다. 원본은 `C:\\JY-Lab\\private-evidence\\` 에만 둔다.",
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
        f'<p:sldIdLst>{"".join(ids)}</p:sldIdLst>'
        f'<p:sldSz cx="{SLIDE_CX}" cy="{SLIDE_CY}" type="screen16x9"/>'
        '<p:notesSz cx="6858000" cy="9144000"/>'
        "</p:presentation>"
    )


def presentation_rels() -> str:
    rows = [
        f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
        f'<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>',
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


def slide_rels() -> str:
    return (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{REL}">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{n}.xml"/>'
        "</Relationships>"
    )


CORE = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="{CP}" xmlns:dc="{DC}" xmlns:dcterms="{DCTERMS}" xmlns:xsi="{XSI}">
  <dc:title>JY Group 상담 시스템 개인정보 진단</dc:title>
  <dc:creator>김준영</dc:creator>
  <cp:lastModifiedBy>수행자</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-10-19T02:10:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-10-19T02:10:00Z</dcterms:modified>
</cp:coreProperties>'''

APP = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>JY briefing</Application>
  <Slides>7</Slides>
  <PresentationFormat>Widescreen</PresentationFormat>
</Properties>'''


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
    banned = ["항·호는 원문 후", "원문 확인 전에", "수료 완료", "인증 취득", "PR 머지 완료"]
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
        zf.writestr("_rels/.rels", rels_one("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml").replace(
            "</Relationships>",
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
            "</Relationships>",
        ))
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
            rels_one("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml"),
        )
        zf.writestr("ppt/notesMasters/notesMaster1.xml", NOTES_MASTER)
        zf.writestr(
            "ppt/notesMasters/_rels/notesMaster1.xml.rels",
            rels_one("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
        )
        zf.writestr("ppt/theme/theme1.xml", THEME)
        zf.writestr("ppt/presProps.xml", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentationPr xmlns:p="{P}" xmlns:a="{A}"/>')
        zf.writestr("ppt/viewProps.xml", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:viewPr xmlns:a="{A}" xmlns:p="{P}"><p:normalViewPr><p:restoredLeft sz="15620"/><p:restoredTop sz="94660"/></p:normalViewPr><p:slideViewPr><p:cSldViewPr><p:cViewPr varScale="1"><p:scale><a:sx n="100" d="100"/><a:sy n="100" d="100"/></p:scale><p:origin x="0" y="0"/></p:cViewPr></p:cSldViewPr></p:slideViewPr><p:notesTextViewPr><p:cViewPr><p:scale><a:sx n="100" d="100"/><a:sy n="100" d="100"/></p:scale><p:origin x="0" y="0"/></p:cViewPr></p:notesTextViewPr></p:viewPr>')
        zf.writestr("ppt/tableStyles.xml", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:tblStyleLst xmlns:a="{A}" def="{{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}}"/>')
        zf.writestr("docProps/core.xml", CORE)
        zf.writestr("docProps/app.xml", APP)
        for i, item in enumerate(SLIDES, start=1):
            xml = slide_xml(item)
            note = notes_xml(item["note"])
            chunks.append(xml)
            chunks.append(note)
            zf.writestr(f"ppt/slides/slide{i}.xml", xml)
            zf.writestr(
                f"ppt/slides/_rels/slide{i}.xml.rels",
                slide_rels().replace("{n}", str(i)),
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