# -*- coding: utf-8 -*-
"""교육 1쪽 Word와 PDF를 만든다.

실행: py -3 tools/build_training_one_pager.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "training"
DOCX = OUT / "JY-Privacy-Training.docx"
PDF = OUT / "JY-Privacy-Training.pdf"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
CP = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC = "http://purl.org/dc/elements/1.1/"
DCTERMS = "http://purl.org/dc/terms/"
XSI = "http://www.w3.org/2001/XMLSchema-instance"

NAVY = "1B3A4B"
INK = "243038"
MUTED = "5C6B73"
LINE = "D5DEE3"
PAPER = "F4F7F8"
AMBER = "F8F1E7"
WHITE = "FFFFFF"


def esc(text: str) -> str:
    return escape(text)


def t_el(text: str) -> str:
    space = ' xml:space="preserve"' if text[:1].isspace() or text[-1:].isspace() else ""
    return f"<w:t{space}>{esc(text)}</w:t>"


def rpr(size: int, bold: bool = False, color: str = INK) -> str:
    b = "<w:b/>" if bold else ""
    return (
        "<w:rPr>"
        '<w:rFonts w:ascii="Malgun Gothic" w:hAnsi="Malgun Gothic" '
        'w:eastAsia="Malgun Gothic" w:cs="Malgun Gothic"/>'
        f"{b}<w:color w:val=\"{color}\"/>"
        f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        "</w:rPr>"
    )


def run(text: str, size: int = 16, bold: bool = False, color: str = INK) -> str:
    return f"<w:r>{rpr(size, bold, color)}{t_el(text)}</w:r>"


def p(
    text: str,
    size: int = 16,
    bold: bool = False,
    color: str = INK,
    before: int = 0,
    after: int = 40,
    align: str | None = None,
) -> str:
    jc = f'<w:jc w:val="{align}"/>' if align else ""
    return (
        "<w:p>"
        "<w:pPr>"
        f'<w:spacing w:before="{before}" w:after="{after}" w:line="240" w:lineRule="auto"/>'
        f"{jc}<w:ind w:left=\"0\" w:right=\"0\"/>"
        "</w:pPr>"
        f"{run(text, size, bold, color)}"
        "</w:p>"
    )


def cell(
    blocks: str,
    width: int,
    fill: str | None = None,
    span: int | None = None,
    align: str = "left",
) -> str:
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ""
    span_xml = f'<w:gridSpan w:val="{span}"/>' if span else ""
    mar = (
        '<w:tcMar><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
        '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar>'
    )
    return (
        "<w:tc>"
        "<w:tcPr>"
        f'<w:tcW w:w="{width}" w:type="dxa"/>'
        f"{span_xml}{shd}"
        f'<w:vAlign w:val="{align}"/>'
        f"{mar}"
        "</w:tcPr>"
        f"{blocks}"
        "</w:tc>"
    )


def borders() -> str:
    edge = f'<w:{{0}} w:val="single" w:sz="4" w:space="0" w:color="{LINE}"/>'
    return "".join(edge.format(side) for side in ("top", "left", "bottom", "right", "insideH", "insideV"))


def table(rows: list[str], widths: list[int]) -> str:
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    total = sum(widths)
    body = "".join(f"<w:tr>{row}</w:tr>" for row in rows)
    return (
        "<w:tbl>"
        "<w:tblPr>"
        '<w:tblW w:w="5000" w:type="pct"/>'
        f"<w:tblBorders>{borders()}</w:tblBorders>"
        '<w:tblLayout w:type="fixed"/>'
        f'<w:tblW w:w="{total}" w:type="dxa"/>'
        "</w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>"
        f"{body}"
        "</w:tbl>"
    )


def lines(items: list[str], size: int = 15) -> str:
    parts = []
    for item in items:
        parts.append(p(item, size=size, before=20, after=20))
    return "".join(parts)


DONT = [
    "제한상담 URL을 일반상담원과 외부 유지보수에 넘기지 않는다. F-02에서 S04와 S06이 T11을 열람했다.",
    "종료된 계정으로 로그인하지 않는다. S05는 종료일 2026-09-14 이후에도 활성인 채로 T02를 열람했다.",
    "다른 고객의 티켓을 내 조직에서 보지 않는다. 공유 조직은 아니오이다.",
    "첨부 jy-doc02.txt 등을 PC에 남기면 계정 삭제와 권한 회수로 지워지지 않는다.",
    "상담 본문을 외부 AI나 개인 메일에 붙여 넣지 않는다. 이 시스템은 AI에 연결되어 있지 않다.",
    "docker compose down -v 로 실습 데이터를 지우지 않는다.",
    "실제 개인정보위 신고 메일과 실제 고객 메일을 보내지 않는다.",
]

DO = [
    "티켓 주소는 http://127.0.0.1:8080 이다. T12 줌은 #ticket/zoom/14 이다. 52014를 주소에 넣으면 찾지 못한다.",
    "권한 요청은 S02가 받고 S01이 실행한다.",
    "삭제 요청은 접수, 본인확인, 실행, 회신 순이다. 버튼 한 번으로 참조 티켓, 사본, 백업까지 지워지지 않는다.",
    "증적 PNG, JSON, 토큰은 C:\\JY-Lab\\private-evidence\\ 에만 둔다. Git에 올리지 않는다.",
]

ROLES = [
    ("시스템 관리자", "S01  admin@jy.example.test", "계정 회수, 그룹, 공유 조직, 자료 보안"),
    ("보호 담당", "S02  privacy@jy.example.test", "요청 승인, 방침과 예외대장, 파기 범위"),
    ("상담 리더", "S03  lead@service.example.test", "Restricted full. 최소 인원만"),
    ("일반 상담", "S04  agent@service.example.test", "General만. Restricted 금지"),
    ("종료 계정", "S05  former@service.example.test", "Active=false. 로그인 시도 금지"),
    ("유지보수", "S06  maint@vendor.example.test", "그룹 없음. 한시 권한이 있을 때만"),
]


def role_rows() -> list[str]:
    widths = [1800, 4200, 4586]
    header = "".join(
        cell(p(text, size=14, bold=True, color=WHITE, before=0, after=0), width, NAVY, align="center")
        for text, width in zip(("역할", "계정", "기억할 일"), widths)
    )
    rows = [header]
    for i, (role, account, memory) in enumerate(ROLES):
        fill = PAPER if i % 2 == 0 else WHITE
        rows.append(
            "".join(
                [
                    cell(p(role, size=14, bold=True, before=0, after=0), widths[0], fill, align="center"),
                    cell(p(account, size=14, before=0, after=0), widths[1], fill, align="center"),
                    cell(p(memory, size=14, before=0, after=0), widths[2], fill, align="center"),
                ]
            )
        )
    return rows


def record_row() -> str:
    widths = [1800, 2200, 2800, 3786]
    labels = ("일자", "역할", "이름(가상)", "확인")
    head = "".join(
        cell(p(text, size=14, bold=True, color=WHITE, before=0, after=0), width, NAVY, align="center")
        for text, width in zip(labels, widths)
    )
    blank = "".join(
        cell(p(" ", size=14, before=0, after=0), width, WHITE, align="center")
        for width in widths
    )
    note = cell(
        p("서명 없음. 장기 증빙 없음. 이 칸을 채워도 D04는 미흡이다.", size=14, color=MUTED, before=0, after=0),
        sum(widths),
        AMBER,
        span=4,
    )
    return table([head, blank, note], widths)


def body() -> str:
    half = [5293, 5293]
    actions = table(
        [
            "".join(
                [
                    cell(p("하지 말 것", size=16, bold=True, color=WHITE, before=0, after=0), half[0], NAVY, align="center"),
                    cell(p("할 것", size=16, bold=True, color=WHITE, before=0, after=0), half[1], NAVY, align="center"),
                ]
            ),
            "".join(
                [
                    cell(lines(DONT), half[0], WHITE, align="top"),
                    cell(lines(DO), half[1], WHITE, align="top"),
                ]
            ),
        ],
        half,
    )
    return "".join(
        [
            p("개인정보 취급 교육 1장", size=28, bold=True, color=NAVY, before=0, after=40),
            p(
                "문서ID JY-Training-1P  ·  원문 2026-10-07  ·  형식 2026-10-19  ·  JY Service 상담원, JY Vendor 유지보수, JY Retail 관리자",
                size=14,
                color=MUTED,
                before=0,
                after=80,
            ),
            table(
                [
                    cell(
                        p(
                            "Checks D04는 미흡이다. 이 1장을 읽고 역할을 지키는 양식이다. 서명, 출석, 수료 증빙이 아니다. 실제 고객 교육과 법정 교육이 아니다. .example.test 계정만 쓴다.",
                            size=15,
                            before=0,
                            after=0,
                        ),
                        10586,
                        AMBER,
                    )
                ],
                [10586],
            ),
            p("", size=8, before=0, after=60),
            actions,
            p("역할", size=16, bold=True, color=NAVY, before=120, after=40),
            table(role_rows(), [1800, 4200, 4586]),
            p("이수 기록. 양식만 둔다.", size=16, bold=True, color=NAVY, before=120, after=40),
            record_row(),
        ]
    )


def document_xml() -> str:
    sect = (
        "<w:sectPr>"
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="620" w:right="640" w:bottom="620" w:left="640" w:header="280" w:footer="280" w:gutter="0"/>'
        '<w:cols w:space="0"/>'
        '<w:docGrid w:linePitch="360"/>'
        "</w:sectPr>"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{W}" xmlns:r="{R}">'
        f"<w:body>{body()}{sect}</w:body></w:document>"
    )


CONTENT_TYPES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="{CT}">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''

RELS = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL}">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W}">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Malgun Gothic" w:hAnsi="Malgun Gothic" w:eastAsia="Malgun Gothic" w:cs="Malgun Gothic"/>
      <w:sz w:val="16"/><w:szCs w:val="16"/>
    </w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
</w:styles>'''

CORE = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="{CP}" xmlns:dc="{DC}" xmlns:dcterms="{DCTERMS}" xmlns:xsi="{XSI}">
  <dc:title>JY 개인정보 취급 교육 1장</dc:title>
  <dc:creator>수행자</dc:creator>
  <cp:lastModifiedBy>수행자</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-10-19T00:40:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-10-19T00:40:00Z</dcterms:modified>
</cp:coreProperties>'''

APP = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>JY training one pager</Application>
  <Pages>1</Pages>
</Properties>'''


def write_docx(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", RELS)
        zf.writestr("word/document.xml", document_xml())
        zf.writestr("word/styles.xml", STYLES)
        zf.writestr("word/_rels/document.xml.rels", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{REL}"/>')
        zf.writestr("docProps/core.xml", CORE)
        zf.writestr("docProps/app.xml", APP)


def assert_text(path: Path) -> None:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8")
    required = [
        "D04",
        "미흡",
        "S04",
        "S06",
        "T11",
        "S05",
        "2026-09-14",
        "T02",
        "127.0.0.1:8080",
        "#ticket/zoom/14",
        "52014",
        "private-evidence",
        "down -v",
        "Active=false",
        "서명 없음",
        "JY-Training-1P",
    ]
    for token in required:
        if token not in xml:
            raise SystemExit(f"교육 1장에 {token} 이 없다.")
    for token in ("수료 완료", "출석 완료", "교육 실적 완료", "법정 교육 이수"):
        if token in xml:
            raise SystemExit(f"없는 실적을 넣었다: {token}")


def export_pdf(docx: Path, pdf: Path) -> int | None:
    if sys.platform == "win32":
        ps = r"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($env:TRAIN_DOCX, $false, $true)
$pages = $doc.ComputeStatistics(2)
$null = $doc.ExportAsFixedFormat($env:TRAIN_PDF, 17, $false, 0, 0, 1, 1, 0, $true, $true, 0, $true, $true, $false)
$doc.Close($false)
$word.Quit()
Write-Output $pages
"""
        env = dict(os.environ)
        env["TRAIN_DOCX"] = str(docx)
        env["TRAIN_PDF"] = str(pdf)
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            check=True,
            env=env,
            capture_output=True,
            text=True,
        )
        return int(result.stdout.strip().splitlines()[-1])
    soffice = shutil.which("soffice")
    if not soffice:
        return None
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(pdf.parent), str(docx)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return None


def main() -> None:
    write_docx(DOCX)
    assert_text(DOCX)
    pages = None
    try:
        pages = export_pdf(DOCX, PDF)
    except Exception as exc:
        print(f"PDF 내보내기 실패: {exc}")
        print("docx는 만들어졌다. Word를 모두 닫고 같은 명령을 다시 실행한다.")
    if pages is not None and pages != 1:
        raise SystemExit(f"1쪽이 아니다. Word 쪽수 {pages}")
    for path in (DOCX, PDF):
        if path.exists():
            print(f"{path.name}\t{path.stat().st_size}")
        else:
            print(f"{path.name}\tMISSING")
    if pages is not None:
        print(f"pages\t{pages}")


if __name__ == "__main__":
    main()