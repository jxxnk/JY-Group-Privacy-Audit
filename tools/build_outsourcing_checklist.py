# -*- coding: utf-8 -*-
"""수탁 점검표 엑셀을 만든다.

실행: py -3 tools/build_outsourcing_checklist.py
"""

from __future__ import annotations

import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "outsourcing" / "JY-Outsourcing-Checklist.xlsx"

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

INFO = [
    ("문서ID", "JY-Outsourcing-Checklist"),
    ("원문", "docs/15-outsourcing-checklist.md"),
    ("원문 작성일", "2026-10-07"),
    ("형식 파일 작성일", "2026-10-19"),
    ("판정", "Checks D01은 미흡이다. 이 파일이 그 칸을 바꾸지 않는다."),
    ("범위", "양식과 이번 실습 기입이다. 계약 체결과 연간 감독 실적이 아니다."),
    ("근거", "법 제26조. 항과 호는 이 표에서 새로 단정하지 않는다."),
    ("종료 시", "계정 비활성, 그룹 회수, 내려받은 사본과 백업 검색. 화면 삭제만으로 수탁자 PC 사본은 지워지지 않는다."),
]

VENDORS = [
    ["수탁ID", "수탁자", "연락(가상)", "업무", "목적", "재위탁", "계약서", "개인정보 항목"],
    ["V-01", "JY Service", "lead@service.example.test (S03)", "상담 수행", "상품 문의 상담. 목적 결정은 JY Retail", "없음", "없음", "이름, 이메일, 문의, 첨부"],
    ["V-02", "JY Vendor", "maint@vendor.example.test (S06)", "시스템 유지보수", "필요할 때만 권한. 상담문 상시 열람 아님", "없음", "없음", "시스템 접속. 상담문 상시 열람 아님"],
]

CHECKS = [
    ["수탁ID", "업무", "목적", "계약 검토항목", "요청자료", "확인방법", "결과", "미흡", "담당", "기한", "이행증적"],
    [
        "V-01", "상담 수행", "상품 문의 상담. 목적 결정은 JY Retail",
        "계약서 유무", "계약서", "문서 대조",
        "계약서 없음", "계약 미체결. 연간 실적 아님", "S02", "미정", "없음",
    ],
    [
        "V-01", "상담 수행", "상품 문의 상담. 목적 결정은 JY Retail",
        "제한상담 접근", "S03 권한 화면", "2026-10-06 화면",
        "Restricted full 유지", "없음. 설계상 필요", "S01", "2026-10-06", "Accounts S03",
    ],
    [
        "V-01", "상담 수행", "상품 문의 상담. 목적 결정은 JY Retail",
        "일반상담원 S04의 제한상담", "T11 열람 화면", "2026-10-06 시험과 재확인",
        "초기 T11 id 29, #52028 열람. 조치 후 JY-General만. T11 권한 없음. T02 유지",
        "초기 과다권한은 회수. 연간 감독은 아님", "S01", "2026-10-06", "E-F02-A01, E-F02-A02",
    ],
    [
        "V-01", "상담 수행", "상품 문의 상담. 목적 결정은 JY Retail",
        "권한 재확인", "F-02 기록", "2026-10-06 시험",
        "권한 재확인만 수행", "연간 실적은 아님", "S01", "2026-10-06", "F-02",
    ],
    [
        "V-01", "상담 수행", "상품 문의 상담. 목적 결정은 JY Retail",
        "파기와 반납", "반납 기록", "문서 대조",
        "미실시", "미흡", "S02", "미정", "없음",
    ],
    [
        "V-01", "상담 수행", "상품 문의 상담. 목적 결정은 JY Retail",
        "교육", "교육 기록", "문서 대조",
        "1장 배포 예정. 실적일 공란", "미실시", "S02", "미정", "없음",
    ],
    [
        "V-02", "시스템 유지보수", "필요할 때만 권한. 상담문 상시 열람 아님",
        "계약서 유무", "계약서", "문서 대조",
        "계약서 없음", "계약 미체결. 연간 실적 아님", "S02", "미정", "없음",
    ],
    [
        "V-02", "시스템 유지보수", "필요할 때만 권한. 상담문 상시 열람 아님",
        "유지보수 S06의 제한상담", "그룹 맵", "2026-10-06 시험과 재확인",
        "초기 T11 상시 열람. 조치 후 그룹 맵 없음",
        "초기 과다권한은 회수. 연간 감독은 아님", "S01", "2026-10-06", "E-F02-B02, A-02a",
    ],
    [
        "V-02", "시스템 유지보수", "필요할 때만 권한. 상담문 상시 열람 아님",
        "한시 권한 절차", "절차 문서", "문서 대조",
        "문서 없음. 이번 실습에서 한시 부여를 실행하지 않음",
        "미흡. 절차는 요청 S02, 승인 가상 Retail, 실행 S01", "S02", "미정", "없음",
    ],
    [
        "V-02", "시스템 유지보수", "필요할 때만 권한. 상담문 상시 열람 아님",
        "파기와 반납", "반납 기록", "문서 대조",
        "미실시. 화면 삭제만으로 수탁자 PC 사본은 지워지지 않음",
        "미흡", "S02", "미정", "D03",
    ],
    [
        "V-02", "시스템 유지보수", "필요할 때만 권한. 상담문 상시 열람 아님",
        "교육", "교육 기록", "문서 대조",
        "1장 배포 예정. 실적일 공란", "미실시", "S02", "미정", "없음",
    ],
]


def col_name(index: int) -> str:
    name = ""
    n = index
    while n:
        n, rem = divmod(n - 1, 26)
        name = chr(65 + rem) + name
    return name


def cell(ref: str, text: str, style: int) -> str:
    return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t>{escape(text)}</t></is></c>'


def sheet(rows: list[list[str]], widths: list[int]) -> str:
    body = []
    for r, row in enumerate(rows, start=1):
        cells = []
        for c, value in enumerate(row, start=1):
            style = 1 if r == 1 else 2
            cells.append(cell(f"{col_name(c)}{r}", value, style))
        body.append(f'<row r="{r}">{"".join(cells)}</row>')
    last_col = col_name(len(rows[0]))
    last_row = len(rows)
    cols = "".join(
        f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>'
        for i, width in enumerate(widths, start=1)
    )
    return (
        f'<worksheet xmlns="{NS}">'
        "<sheetViews><sheetView workbookViewId=\"0\">"
        '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        "</sheetView></sheetViews>"
        f"<cols>{cols}</cols>"
        f"<sheetData>{''.join(body)}</sheetData>"
        f'<autoFilter ref="A1:{last_col}{last_row}"/>'
        "<pageMargins left=\"0.5\" right=\"0.5\" top=\"0.6\" bottom=\"0.6\" header=\"0.3\" footer=\"0.3\"/>"
        '<pageSetup paperSize="9" orientation="landscape" fitToWidth="1" fitToHeight="1"/>'
        "</worksheet>"
    )


def info_sheet() -> str:
    rows = [["항목", "내용"], *INFO]
    return sheet(rows, [24, 90])


STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="{NS}">
  <fonts count="2">
    <font><sz val="11"/><name val="Malgun Gothic"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Malgun Gothic"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1B3A4B"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left style="thin"><color rgb="FFD5DEE3"/></left>
      <right style="thin"><color rgb="FFD5DEE3"/></right>
      <top style="thin"><color rgb="FFD5DEE3"/></top>
      <bottom style="thin"><color rgb="FFD5DEE3"/></bottom>
      <diagonal/>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment horizontal="center" vertical="center" wrapText="1"/>
    </xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1">
      <alignment vertical="center" wrapText="1"/>
    </xf>
  </cellXfs>
</styleSheet>'''


def workbook() -> None:
    vendors = sheet(VENDORS, [12, 16, 36, 18, 42, 12, 12, 36])
    checks = sheet(CHECKS, [12, 18, 36, 24, 16, 22, 42, 36, 10, 14, 28])
    info = info_sheet()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>''')
        zf.writestr("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>''')
        zf.writestr("xl/workbook.xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="{NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="문서정보" sheetId="1" r:id="rId1"/>
    <sheet name="수탁목록" sheetId="2" r:id="rId2"/>
    <sheet name="표본점검" sheetId="3" r:id="rId3"/>
  </sheets>
</workbook>''')
        zf.writestr("xl/_rels/workbook.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>''')
        zf.writestr("xl/styles.xml", STYLES)
        zf.writestr("xl/worksheets/sheet1.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + info)
        zf.writestr("xl/worksheets/sheet2.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + vendors)
        zf.writestr("xl/worksheets/sheet3.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + checks)
    text = "\n".join("\t".join(row) for row in CHECKS)
    if "연간 감독 실적 완료" in text or "계약 체결 완료" in text:
        raise SystemExit("실적을 꾸몄다.")
    if "D01" not in info or "미흡" not in "".join(cell for row in CHECKS for cell in row):
        raise SystemExit("판정 문구가 빠졌다.")
    print(f"{OUT.name}\t{OUT.stat().st_size}")


if __name__ == "__main__":
    workbook()