# -*- coding: utf-8 -*-
"""처리방침 Before, After, Tracked docx와 PDF를 만든다.

실행: py -3 tools/build_policy_docs.py
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "policy"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CP = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC = "http://purl.org/dc/elements/1.1/"
DCTERMS = "http://purl.org/dc/terms/"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
EP = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"

NAVY = "1B3A4B"
MUTED = "5C6B73"
LINE = "D5DEE3"
PAPER = "F4F7F8"
WHITE = "FFFFFF"
WHEN = "2026-10-19T00:20:00Z"
AUTHOR = "수행자"

ORIGINAL_TITLE = "가상 고객 제공자료 / 초기 상태 / 실제 회사 문서 아님"
ORIGINAL_BODY = (
    "고객 상담을 위해 이름·이메일·문의내용을 처리한다. "
    "상담정보는 업무가 끝날 때까지 보관한다. "
    "고객은 담당자에게 삭제를 요청할 수 있다."
)


def esc(text: str) -> str:
    return escape(text, {"\"": "&quot;"})


def t_el(text: str, tag: str = "t") -> str:
    space = ' xml:space="preserve"' if text[:1].isspace() or text[-1:].isspace() else ""
    return f'<w:{tag}{space}>{esc(text)}</w:{tag}>'


def rpr(size: int, bold: bool = False, color: str = NAVY, italic: bool = False, strike: bool = False) -> str:
    b = "<w:b/>" if bold else ""
    i = "<w:i/>" if italic else ""
    s = "<w:strike/>" if strike else ""
    return (
        "<w:rPr>"
        '<w:rFonts w:ascii="Malgun Gothic" w:hAnsi="Malgun Gothic" '
        'w:eastAsia="Malgun Gothic" w:cs="Malgun Gothic"/>'
        f"{b}{i}{s}"
        f'<w:color w:val="{color}"/>'
        f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        "</w:rPr>"
    )


def run(text: str, size: int = 22, bold: bool = False, color: str = "243038") -> str:
    return f"<w:r>{rpr(size, bold, color)}{t_el(text)}</w:r>"


def ppr(style: str | None, before: int = 0, after: int = 120, outline: int | None = None, border: bool = False) -> str:
    style_xml = f'<w:pStyle w:val="{style}"/>' if style else ""
    outline_xml = f'<w:outlineLvl w:val="{outline}"/>' if outline is not None else ""
    border_xml = (
        "<w:pBdr><w:bottom w:val=\"single\" w:sz=\"12\" w:space=\"1\" w:color=\"1B3A4B\"/></w:pBdr>"
        if border
        else ""
    )
    return (
        "<w:pPr>"
        f"{style_xml}{outline_xml}"
        f'<w:spacing w:before="{before}" w:after="{after}" w:line="276" w:lineRule="auto"/>'
        f"{border_xml}"
        '<w:rPr><w:rFonts w:ascii="Malgun Gothic" w:hAnsi="Malgun Gothic" '
        'w:eastAsia="Malgun Gothic" w:cs="Malgun Gothic"/></w:rPr>'
        "</w:pPr>"
    )


def paragraph(text: str, style: str | None = None, size: int = 22, bold: bool = False, color: str = "243038", before: int = 0, after: int = 120, outline: int | None = None, border: bool = False) -> str:
    return f"<w:p>{ppr(style, before, after, outline, border)}{run(text, size, bold, color)}</w:p>"


def shade(color: str) -> str:
    return f'<w:shd w:val="clear" w:color="auto" w:fill="{color}"/>'


def cell(text: str, width: int, fill: str | None, bold: bool, color: str, size: int = 20, span: int | None = None) -> str:
    span_xml = f'<w:gridSpan w:val="{span}"/>' if span else ""
    fill_xml = shade(fill) if fill else ""
    return (
        "<w:tc>"
        "<w:tcPr>"
        f'<w:tcW w:w="{width}" w:type="dxa"/>'
        f"{span_xml}{fill_xml}"
        '<w:vAlign w:val="center"/>'
        "</w:tcPr>"
        f"<w:p>{ppr(None, 40, 40)}{run(text, size, bold, color)}</w:p>"
        "</w:tc>"
    )


def table(rows: list[list[str]], widths: list[int], header: bool = True) -> str:
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    body = []
    for index, row in enumerate(rows):
        is_header = header and index == 0
        fill = NAVY if is_header else (PAPER if index % 2 == 0 else WHITE)
        color = WHITE if is_header else "243038"
        cells = "".join(
            cell(value, widths[col], fill, is_header, color)
            for col, value in enumerate(row)
        )
        header_mark = "<w:tblHeader/>" if is_header else ""
        body.append(f"<w:tr><w:trPr>{header_mark}</w:trPr>{cells}</w:tr>")
    borders = "".join(
        f'<w:{edge} w:val="single" w:sz="4" w:space="0" w:color="{LINE}"/>'
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    return (
        "<w:tbl>"
        "<w:tblPr>"
        '<w:tblW w:w="5000" w:type="pct"/>'
        f"<w:tblBorders>{borders}</w:tblBorders>"
        '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
        '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar>'
        '<w:tblLook w:firstRow="1" w:noHBand="0" w:noVBand="1"/>'
        "</w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>"
        f"{''.join(body)}"
        "</w:tbl>"
    )


def callout(text: str) -> str:
    width = 9866
    return (
        "<w:tbl><w:tblPr>"
        '<w:tblW w:w="5000" w:type="pct"/>'
        f'<w:tblBorders><w:top w:val="nil"/><w:left w:val="single" w:sz="16" w:space="0" w:color="{NAVY}"/>'
        '<w:bottom w:val="nil"/><w:right w:val="nil"/>'
        '<w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>'
        '<w:tblCellMar><w:top w:w="80" w:type="dxa"/><w:left w:w="140" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar>'
        "</w:tblPr>"
        f'<w:tblGrid><w:gridCol w:w="{width}"/></w:tblGrid>'
        "<w:tr><w:tc><w:tcPr>"
        f'<w:tcW w:w="{width}" w:type="dxa"/>{shade(PAPER)}'
        "</w:tcPr>"
        f"<w:p>{ppr(None, 40, 40)}{run(text, 20, False, NAVY)}</w:p>"
        "</w:tc></w:tr></w:tbl>"
    )


def styles_xml() -> str:
    def style(style_id: str, name: str, size: int, bold: bool, color: str, outline: int | None = None) -> str:
        outline_xml = f"<w:outlineLvl w:val=\"{outline}\"/>" if outline is not None else ""
        b = "<w:b/>" if bold else ""
        return (
            f'<w:style w:type="paragraph" w:styleId="{style_id}">'
            f'<w:name w:val="{name}"/>'
            f"<w:pPr>{outline_xml}"
            '<w:spacing w:before="0" w:after="120" w:line="276" w:lineRule="auto"/>'
            "</w:pPr>"
            "<w:rPr>"
            '<w:rFonts w:ascii="Malgun Gothic" w:hAnsi="Malgun Gothic" w:eastAsia="Malgun Gothic" w:cs="Malgun Gothic"/>'
            f"{b}<w:color w:val=\"{color}\"/>"
            f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
            "</w:rPr></w:style>"
        )

    return (
        f'<w:styles xmlns:w="{W}">'
        "<w:docDefaults><w:rPrDefault><w:rPr>"
        '<w:rFonts w:ascii="Malgun Gothic" w:hAnsi="Malgun Gothic" w:eastAsia="Malgun Gothic" w:cs="Malgun Gothic"/>'
        '<w:sz w:val="22"/><w:szCs w:val="22"/>'
        "</w:rPr></w:rPrDefault></w:docDefaults>"
        + style("Normal", "Normal", 22, False, "243038")
        + style("Heading1", "heading 1", 32, True, NAVY, 0)
        + style("Heading2", "heading 2", 26, True, NAVY, 1)
        + "</w:styles>"
    )


def settings_xml(track: bool) -> str:
    track_xml = '<w:trackRevisions/><w:revisionView w:markup="1" w:comments="1" w:insDel="1"/>' if track else ""
    return (
        f'<w:settings xmlns:w="{W}">'
        f"{track_xml}"
        '<w:defaultTabStop w:val="720"/>'
        "<w:compat>"
        '<w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
        "</w:compat></w:settings>"
    )


def header_xml(left: str, right: str) -> str:
    return (
        f'<w:hdr xmlns:w="{W}">'
        "<w:tbl><w:tblPr>"
        '<w:tblW w:w="5000" w:type="pct"/>'
        '<w:tblBorders><w:bottom w:val="single" w:sz="8" w:space="0" w:color="1B3A4B"/>'
        '<w:top w:val="nil"/><w:left w:val="nil"/><w:right w:val="nil"/>'
        '<w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>'
        "</w:tblPr>"
        '<w:tblGrid><w:gridCol w:w="6400"/><w:gridCol w:w="3466"/></w:tblGrid>'
        "<w:tr>"
        f'<w:tc><w:tcPr><w:tcW w:w="6400" w:type="dxa"/></w:tcPr><w:p>{ppr(None, 0, 60)}{run(left, 16, True, NAVY)}</w:p></w:tc>'
        f'<w:tc><w:tcPr><w:tcW w:w="3466" w:type="dxa"/></w:tcPr><w:p>{ppr(None, 0, 60)}{run(right, 16, False, MUTED)}</w:p></w:tc>'
        "</w:tr></w:tbl></w:hdr>"
    )


def footer_xml(label: str) -> str:
    return (
        f'<w:ftr xmlns:w="{W}">'
        "<w:tbl><w:tblPr>"
        '<w:tblW w:w="5000" w:type="pct"/>'
        '<w:tblBorders><w:top w:val="single" w:sz="6" w:space="1" w:color="D5DEE3"/>'
        '<w:bottom w:val="nil"/><w:left w:val="nil"/><w:right w:val="nil"/>'
        '<w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>'
        "</w:tblPr>"
        '<w:tblGrid><w:gridCol w:w="7600"/><w:gridCol w:w="2266"/></w:tblGrid>'
        "<w:tr>"
        f'<w:tc><w:tcPr><w:tcW w:w="7600" w:type="dxa"/></w:tcPr><w:p>{ppr(None, 60, 0)}{run(label, 16, False, MUTED)}</w:p></w:tc>'
        "<w:tc><w:tcPr><w:tcW w:w=\"2266\" w:type=\"dxa\"/></w:tcPr>"
        f"<w:p>{ppr(None, 60, 0)}"
        f"{run('페이지 ', 16, False, MUTED)}"
        '<w:r><w:rPr><w:rFonts w:ascii="Malgun Gothic" w:hAnsi="Malgun Gothic" w:eastAsia="Malgun Gothic"/>'
        '<w:sz w:val="16"/><w:szCs w:val="16"/><w:color w:val="5C6B73"/></w:rPr>'
        '<w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        "</w:p></w:tc></w:tr></w:tbl></w:ftr>"
    )


def sect_pr() -> str:
    return (
        "<w:sectPr>"
        '<w:headerReference w:type="default" r:id="rHeader"/>'
        '<w:footerReference w:type="default" r:id="rFooter"/>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1020" w:bottom="1020" w:left="1020" w:header="454" w:footer="454" w:gutter="0"/>'
        "</w:sectPr>"
    )


def document_xml(body: str) -> str:
    return (
        f'<w:document xmlns:w="{W}" xmlns:r="{R}">'
        f"<w:body>{body}{sect_pr()}</w:body></w:document>"
    )


def core_xml(title: str) -> str:
    return (
        f'<cp:coreProperties xmlns:cp="{CP}" xmlns:dc="{DC}" xmlns:dcterms="{DCTERMS}" xmlns:xsi="{XSI}">'
        f"<dc:title>{esc(title)}</dc:title>"
        "<dc:creator>김준영</dc:creator>"
        "<cp:lastModifiedBy>김준영</cp:lastModifiedBy>"
        "<dc:description>가상 실습. 대외 공시 문서가 아니다.</dc:description>"
        "</cp:coreProperties>"
    )


def app_xml() -> str:
    return (
        f'<Properties xmlns="{EP}">'
        "<Application>JY Group privacy lab</Application></Properties>"
    )


def content_types(comments: bool) -> str:
    extra = (
        '<Override PartName="/word/comments.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>'
        if comments
        else ""
    )
    return (
        f'<Types xmlns="{CT}">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
        '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
        '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        f"{extra}</Types>"
    )


def package_rels() -> str:
    return (
        f'<Relationships xmlns="{REL}">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )


def document_rels(comments: bool) -> str:
    extra = (
        '<Relationship Id="rComments" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/>'
        if comments
        else ""
    )
    return (
        f'<Relationships xmlns="{REL}">'
        '<Relationship Id="rStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '<Relationship Id="rSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
        '<Relationship Id="rHeader" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
        '<Relationship Id="rFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
        f"{extra}</Relationships>"
    )


def write_docx(path: Path, title: str, header_left: str, header_right: str, footer: str, body: str, track: bool = False, comments: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types(comments is not None))
        zf.writestr("_rels/.rels", package_rels())
        zf.writestr("docProps/core.xml", core_xml(title))
        zf.writestr("docProps/app.xml", app_xml())
        zf.writestr("word/document.xml", document_xml(body))
        zf.writestr("word/styles.xml", styles_xml())
        zf.writestr("word/settings.xml", settings_xml(track))
        zf.writestr("word/header1.xml", header_xml(header_left, header_right))
        zf.writestr("word/footer1.xml", footer_xml(footer))
        zf.writestr("word/_rels/document.xml.rels", document_rels(comments is not None))
        if comments is not None:
            zf.writestr("word/comments.xml", comments)


def before_body() -> str:
    meta = table(
        [
            ["항목", "내용"],
            ["원문 파일", "docs/client-before/02-privacy-policy.md.txt"],
            ["원문 시점", "미기재. 파일에 날짜가 없다."],
            ["Word 변환일", "2026-10-19"],
        ],
        [2400, 7466],
    )
    return (
        paragraph("변환 기록", "Heading1", 32, True, NAVY, 0, 80, 0, True)
        + callout("이 상자와 위 제목은 초기 원문에 없다. 아래 두 문단만 원문이다.")
        + meta
        + paragraph(ORIGINAL_TITLE, "Heading1", 32, True, NAVY, 280, 80, 0, True)
        + paragraph(ORIGINAL_BODY, "Normal", 22, False, "243038", 80, 120)
    )


def after_sections() -> list[tuple[str, list[str], list[list[str]] | None, list[int] | None]]:
    return [
        (
            "1. 처리 목적과 항목",
            [
                "상담은 상품 문의 목적에 한정한다. 처리 항목은 이름, 이메일, 문의 본문, 첨부다. 합성 자료에 주민등록번호와 민감정보는 없다. 수집 항목을 동의 하나로 묶지 않는다.",
                "제한상담의 항목도 같다. 일반상담원과 외부 유지보수가 상시로 보는 대상이 아니다.",
            ],
            None,
            None,
        ),
        (
            "2. 보유와 파기",
            [
                "상담이 끝나면 지체 없이 파기한다.",
                "법령에 보관 의무가 있는 경우에만 그 기간 동안 보관한다. 기간 숫자는 해당 조문을 확인한 뒤 적는다. 현재 이 칸은 비어 있다.",
                "화면의 삭제만으로 파기가 끝났다고 보지 않는다. 다른 기록, 첨부, 내려받은 사본, 백업을 따로 확인한다.",
            ],
            None,
            None,
        ),
        (
            "3. 위탁과 제3자 제공",
            ["계약서와 정기 감독 실적은 이 초안에 없다."],
            [
                ["구분", "상대", "업무", "범위"],
                ["위탁", "JY Service", "상담 수행", "목적 결정은 JY Retail"],
                ["위탁", "JY Vendor", "시스템 유지보수", "필요할 때만 권한을 준다. 제한상담을 상시로 보지 않는다"],
                ["제3자 제공", "해당 없음", "", "그룹사 이름만으로 제공 근거가 되지 않는다"],
            ],
            [1600, 2000, 2400, 3866],
        ),
        (
            "4. 정보주체의 권리",
            [
                "열람, 정정, 삭제, 처리정지를 받는다.",
                "접수 창구는 가상 주소 privacy@jy.example.test 이고, 역할은 보호 담당이다. 실행 역할은 시스템 관리자다.",
                "순서는 접수, 본인확인, 승인, 실행, 회신이다.",
                "이 실습에서 메일을 보내거나 받지 않았다. 서명은 없다.",
                "삭제를 실행할 때는 다른 기록, 사본, 백업을 범위에 넣는다. 시험용으로 남겨 둔 기록은 따로 관리한다.",
            ],
            None,
            None,
        ),
        (
            "5. 안전조치",
            [
                "종료일이 된 계정은 비활성으로 두고, 그 계정으로 새로 로그인하지 못하게 한다. 이미 열려 있던 세션은 확인하지 않았다.",
                "일반상담과 제한상담의 접근 범위를 나눈다.",
                "고객 조직의 공유는 꺼져 있다.",
                "상담 본문을 외부 AI에 보내지 않는다. 이 시스템은 AI에 연결되어 있지 않다.",
            ],
            None,
            None,
        ),
        (
            "6. 책임자",
            [
                "보호 담당은 privacy@jy.example.test 이다. 시스템 관리자는 admin@jy.example.test 이다.",
                "한 사람이 두 역할을 겸한 실습이다. 실제 조직의 서명이 아니다.",
            ],
            None,
            None,
        ),
        (
            "7. 사고 통지",
            [
                "통지와 신고는 사실을 확인한 뒤 판단한다. 모든 사고의 기한을 72시간으로 적지 않는다.",
                "이 실습에서 대외 통지와 신고는 하지 않았다.",
            ],
            None,
            None,
        ),
    ]


def after_body() -> str:
    meta = table(
        [
            ["항목", "내용"],
            ["문서ID", "JY-Privacy-Policy-After"],
            ["문안 작성일", "2026-10-07"],
            ["Word 정리일", "2026-10-19"],
            ["상태", "가상 실습 초안. 대외 공시와 동의가 아니다."],
            ["대상", "로컬 상담 시스템 1식"],
            ["적용", "JY Retail은 처리 목적을 정한다. JY Service는 상담을 수행한다. JY Vendor는 유지보수를 한다."],
        ],
        [2200, 7666],
    )
    parts = [
        paragraph("JY Group 개인정보 처리방침", "Heading1", 32, True, NAVY, 0, 160, 0, True),
        meta,
        paragraph("", "Normal", 22, False, "243038", 60, 40),
        callout("이 초안을 만들었다는 이유로 초기 점검 판정을 바꾸지 않는다."),
    ]
    for title, paras, grid, widths in after_sections():
        parts.append(paragraph(title, "Heading2", 26, True, NAVY, 280, 80, 1))
        if grid and widths:
            parts.append(table(grid, widths))
        for text in paras:
            parts.append(paragraph(text, "Normal", 22, False, "243038", 60, 80))
    parts.append(paragraph("8. 변경", "Heading2", 26, True, NAVY, 280, 80, 1))
    parts.append(
        table(
            [
                ["일자", "내용"],
                ["초기 문안", "보유, 위탁, 권리 설명이 부족했다"],
                ["2026-10-07", "이 초안을 작성했다"],
                ["2026-10-19", "대외 문안에서 내부 번호와 로컬 경로를 뺐다"],
            ],
            [2200, 7666],
        )
    )
    return "".join(parts)


def rev_run(text: str, kind: str, rev_id: int, size: int = 22, bold: bool = False, color: str = "243038") -> tuple[str, int]:
    tag = "ins" if kind == "ins" else "del"
    text_tag = "t" if kind == "ins" else "delText"
    strike = kind == "del"
    xml = (
        f'<w:{tag} w:id="{rev_id}" w:author="{AUTHOR}" w:date="{WHEN}">'
        f"<w:r>{rpr(size, bold, color, strike=strike)}{t_el(text, text_tag)}</w:r>"
        f"</w:{tag}>"
    )
    return xml, rev_id + 1


def comment_ref(comment_id: int) -> str:
    return (
        f'<w:commentRangeStart w:id="{comment_id}"/>'
        "{MARK}"
        f'<w:commentRangeEnd w:id="{comment_id}"/>'
        f'<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>'
        f'<w:commentReference w:id="{comment_id}"/></w:r>'
    )


def tracked_body() -> tuple[str, str]:
    rev = 1
    comments = [
        (0, "2. 보유와 파기", "B02. 초기 문장의 보관 문구를 바꿨다. 기간 숫자는 비웠다. CT-F03. 법 제21조 제1항과 제2항."),
        (1, "3. 위탁과 제3자 제공", "D01. 계약서와 연간 감독 실적은 없다. 수탁은 JY Service와 JY Vendor다."),
        (2, "4. 정보주체의 권리", "B04는 미확인이다. 실제 메일은 없다. 모의 기록은 JY-RR-2026-01이다."),
        (3, "5. 안전조치", "F-01과 F-02. 조치는 2026-10-06이다. 세션과 백업은 확인하지 않았다."),
        (4, "7. 사고 통지", "F02는 미흡이다. 법 제34조. 통지와 신고는 하지 않았다."),
    ]
    by_title = {title: (cid, text) for cid, title, text in comments}
    parts = [
        paragraph(
            "비교 기준은 초기 TXT다. 원문 시점은 미기재이고, Word 변환일과 정리일은 2026-10-19이다.",
            "Normal",
            20,
            False,
            MUTED,
            0,
            120,
        )
    ]
    deleted_title, rev = rev_run(ORIGINAL_TITLE, "del", rev, 32, True, "9B2C2C")
    parts.append(f"<w:p>{ppr('Heading1', 200, 80, 0, True)}{deleted_title}</w:p>")
    deleted_body, rev = rev_run(ORIGINAL_BODY, "del", rev, 22, False, "9B2C2C")
    parts.append(f"<w:p>{ppr('Normal', 80, 160)}{deleted_body}</w:p>")

    title_ins, rev = rev_run("JY Group 개인정보 처리방침", "ins", rev, 32, True, NAVY)
    parts.append(f"<w:p>{ppr('Heading1', 200, 160, 0, True)}{title_ins}</w:p>")

    for title, paras, grid, widths in after_sections():
        inserted, rev = rev_run(title, "ins", rev, 26, True, NAVY)
        mark = ""
        if title in by_title:
            cid, _note = by_title[title]
            wrapped = comment_ref(cid).replace("{MARK}", inserted)
            parts.append(f"<w:p>{ppr('Heading2', 280, 80, 1)}{wrapped}</w:p>")
            memo, rev = rev_run(f"메모. {_note}", "ins", rev, 18, False, MUTED)
            parts.append(f"<w:p>{ppr('Normal', 0, 60)}{memo}</w:p>")
        else:
            parts.append(f"<w:p>{ppr('Heading2', 280, 80, 1)}{inserted}{mark}</w:p>")
        if grid and widths:
            # 표 안의 글도 삽입으로 표시하면 비교본이 읽힌다.
            shown = []
            for row in grid:
                new_row = []
                for value in row:
                    if not value:
                        new_row.append(value)
                        continue
                    piece, rev = rev_run(value, "ins", rev, 20, False, "243038")
                    new_row.append(piece)
                shown.append(new_row)
            parts.append(revision_table(shown, widths))
        for text in paras:
            inserted, rev = rev_run(text, "ins", rev, 22, False, "243038")
            parts.append(f"<w:p>{ppr('Normal', 60, 80)}{inserted}</w:p>")

    change_title, rev = rev_run("8. 변경", "ins", rev, 26, True, NAVY)
    parts.append(f"<w:p>{ppr('Heading2', 280, 80, 1)}{change_title}</w:p>")
    change_rows = [
        ["일자", "내용"],
        ["초기 문안", "보유, 위탁, 권리 설명이 부족했다"],
        ["2026-10-07", "이 초안을 작성했다"],
        ["2026-10-19", "대외 문안에서 내부 번호와 로컬 경로를 뺐다"],
    ]
    shown_rows = []
    for row in change_rows:
        piece_row = []
        for value in row:
            piece, rev = rev_run(value, "ins", rev, 20, False, "243038")
            piece_row.append(piece)
        shown_rows.append(piece_row)
    parts.append(revision_table(shown_rows, [2200, 7666], header=True))

    comment_xml = [f'<w:comments xmlns:w="{W}">']
    for cid, _title, note in comments:
        comment_xml.append(
            f'<w:comment w:id="{cid}" w:author="{AUTHOR}" w:date="{WHEN}" w:initials="S02">'
            f"<w:p>{ppr(None, 0, 0)}{run(note, 20, False, '243038')}</w:p>"
            "</w:comment>"
        )
    comment_xml.append("</w:comments>")
    return "".join(parts), "".join(comment_xml)


def revision_table(rows: list[list[str]], widths: list[int], header: bool = True) -> str:
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    body = []
    for index, row in enumerate(rows):
        is_header = header and index == 0
        fill = NAVY if is_header else (PAPER if index % 2 == 0 else WHITE)
        color = WHITE if is_header else "243038"
        cells = []
        for col, value in enumerate(row):
            fill_xml = shade(fill)
            # value is already revision XML, or empty.
            inner = value if value else run("", 20, False, color)
            if is_header and value and "<w:color" in value:
                inner = value.replace('w:color w:val="243038"', f'w:color w:val="{WHITE}"').replace("<w:rPr>", "<w:rPr><w:b/>", 1)
            cells.append(
                "<w:tc><w:tcPr>"
                f'<w:tcW w:w="{widths[col]}" w:type="dxa"/>{fill_xml}'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f"<w:p>{ppr(None, 40, 40)}{inner}</w:p></w:tc>"
            )
        mark = "<w:tblHeader/>" if is_header else ""
        body.append(f"<w:tr><w:trPr>{mark}</w:trPr>{''.join(cells)}</w:tr>")
    borders = "".join(
        f'<w:{edge} w:val="single" w:sz="4" w:space="0" w:color="{LINE}"/>'
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    return (
        "<w:tbl><w:tblPr>"
        '<w:tblW w:w="5000" w:type="pct"/>'
        f"<w:tblBorders>{borders}</w:tblBorders>"
        '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
        '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar>'
        "</w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>{''.join(body)}</w:tbl>"
    )


def export_with_word(after_docx: Path, tracked_docx: Path, after_pdf: Path, tracked_pdf: Path) -> None:
    ps = r"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$word.Options.PrintRevisions = $true
function Export-One([string]$docx, [string]$pdf, [int]$item) {
  $doc = $word.Documents.Open($docx, $false, $true)
  $null = $doc.ExportAsFixedFormat($pdf, 17, $false, 0, 0, 1, 1, $item, $true, $true, 0, $true, $true, $false)
  $doc.Close($false)
}
Export-One $env:POLICY_AFTER_DOCX $env:POLICY_AFTER_PDF 0
Export-One $env:POLICY_TRACKED_DOCX $env:POLICY_TRACKED_PDF 7
$word.Quit()
"""
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    env["POLICY_AFTER_DOCX"] = str(after_docx)
    env["POLICY_TRACKED_DOCX"] = str(tracked_docx)
    env["POLICY_AFTER_PDF"] = str(after_pdf)
    env["POLICY_TRACKED_PDF"] = str(tracked_pdf)
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True, env=env)


def export_with_libreoffice(folder: Path) -> None:
    soffice = "soffice"
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(folder), str(folder / "JY-Privacy-Policy-After.docx"), str(folder / "JY-Privacy-Policy-Tracked.docx")],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def plain_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8")
        comments = zf.read("word/comments.xml").decode("utf-8") if "word/comments.xml" in zf.namelist() else ""
    return xml + comments


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    before = OUT / "JY-Privacy-Policy-Before.docx"
    after = OUT / "JY-Privacy-Policy-After.docx"
    tracked = OUT / "JY-Privacy-Policy-Tracked.docx"
    after_pdf = OUT / "JY-Privacy-Policy-After.pdf"
    tracked_pdf = OUT / "JY-Privacy-Policy-Tracked.pdf"

    write_docx(
        before,
        "JY Group 개인정보 처리방침 초기 문안",
        "JY Group 개인정보 실습",
        "Before",
        "초기 문안. 가상 실습. 대외 공시 아님",
        before_body(),
    )
    write_docx(
        after,
        "JY Group 개인정보 처리방침",
        "JY Group 개인정보 실습",
        "After",
        "대외 문안 초안. 가상 실습. 대외 공시 아님",
        after_body(),
    )
    body, comments = tracked_body()
    write_docx(
        tracked,
        "JY Group 개인정보 처리방침 비교",
        "JY Group 개인정보 실습",
        "Tracked",
        "변경 표시. 가상 실습. 대외 공시 아님",
        body,
        track=True,
        comments=comments,
    )

    before_text = plain_text(before)
    after_text = plain_text(after)
    tracked_text = plain_text(tracked)
    if ORIGINAL_BODY not in before_text or "업무가 끝날 때까지" not in before_text:
        raise SystemExit("Before에 원문이 없다.")
    if "T12" in after_text or "EX-0" in after_text or "private-evidence" in after_text:
        raise SystemExit("After 대외 문안에 내부 번호가 있다.")
    if "지체 없이 파기한다" not in after_text:
        raise SystemExit("After 파기 문장이 없다.")
    for token in ("B04", "JY-RR-2026-01", "CT-F03", "F02", ORIGINAL_BODY, "지체 없이 파기한다"):
        if token not in tracked_text:
            raise SystemExit(f"Tracked에 {token} 이 없다.")

    if sys.platform == "win32":
        try:
            export_with_word(after, tracked, after_pdf, tracked_pdf)
        except Exception as exc:
            print(f"PDF 내보내기 실패: {exc}")
            print("docx 3개는 만들어졌다. Word를 모두 닫고 같은 명령을 다시 실행한다.")
    elif __import__("shutil").which("soffice"):
        export_with_libreoffice(OUT)

    for path in (before, after, tracked, after_pdf, tracked_pdf):
        if path.exists():
            print(f"{path.name}\t{path.stat().st_size}")
        else:
            print(f"{path.name}\tMISSING")


if __name__ == "__main__":
    main()
