# -*- coding: utf-8 -*-
"""최종 보고서 DOCX와 PDF를 Word에서 직접 만든다.

실행: .\\.venv\\Scripts\\python.exe tools\\build_final_report.py
원고 docs/18-final-report.md를 읽고, evidence/sanitized의 공개 PNG만 넣는다.
"""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "docs" / "18-final-report.md"
SAN = ROOT / "evidence" / "sanitized"
OUT = ROOT / "reports"
DOCX = OUT / "JY-Final-Report.docx"
PDF = OUT / "JY-Final-Report.pdf"

ID_RE = re.compile(r"E-(?:F\d{2}|D\d{2})-[AB]\d{2}[a-z]?")

NOTES = {
    "E-F01-B01": "F-01 조치 전 화면. 입력 계정 특정과 기존 세션은 이 화면 밖이다.",
    "E-F01-A01": "F-01 조치 후 화면. 새 로그인 차단만 보여 주고 기존 세션 회수는 확인하지 않는다.",
    "E-F02-B01": "F-02 조치 전 화면. 후 T11의 대상과 순서는 이 화면 밖이다.",
    "E-F02-B03": "F-02b 조치 전 조직 공유 화면.",
    "E-F02-A01": "F-02 조치 후 화면. S06 차단 후 T11 시험은 이 화면으로 확인하지 않는다.",
    "E-F02-A02": "F-02 조치 후 화면. 직접 주소와 첨부 거부는 이 화면 밖이다.",
    "E-F02-A03": "F-02b 조치 후 목록 화면. 직접 주소와 첨부 거부는 미확인이다.",
    "E-F03-B01": "F-03 삭제 전 화면. 완료 화면은 다시 보지 않았다.",
    "E-F03-A01": "F-03 조치 후 화면. 백업 잔존과 복구는 이 화면 밖이다.",
    "E-F03-A02": "F-03 잔존 화면. 백업 잔존과 복구는 미확인이다.",
}


def clean(text: str) -> str:
    return text.replace("`", "").strip()


def require(md: str) -> None:
    for token in (
        "#52020",
        "6점·계획",
        "2026-11-06",
        "v2의 collect, diff, verify",
        "현재 FinalReview 24행",
    ):
        if token not in md:
            raise SystemExit("원고에 없다: " + token)
    if "F-02a, F-02b, F-03은 9점" in md:
        raise SystemExit("옛 점수 문장이 남아 있다")


def parse(md: str) -> list[tuple]:
    lines = md.splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("|"):
            raw = []
            while i < len(lines) and lines[i].startswith("|"):
                raw.append(lines[i])
                i += 1
            rows = []
            for item in raw:
                cells = [clean(cell) for cell in item.strip().strip("|").split("|")]
                if cells and all(
                    re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells
                ):
                    continue
                rows.append(cells)
            blocks.append(("table", rows))
            continue
        if line.startswith("### "):
            blocks.append(("h3", clean(line[4:])))
            i += 1
            continue
        if line.startswith("## "):
            blocks.append(("h2", clean(line[3:])))
            i += 1
            continue
        if line.startswith("# "):
            blocks.append(("h1", clean(line[2:])))
            i += 1
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(clean(lines[i][2:]))
                i += 1
            blocks.append(("ul", items))
            continue
        parts = [line.strip()]
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].startswith(("#", "|", "- "))
        ):
            parts.append(lines[i].strip())
            i += 1
        blocks.append(("p", clean(" ".join(parts))))
    return blocks


def active_rows() -> list[list[str]]:
    path = SAN / "users-active.csv"
    if not path.exists():
        return [["항목", "내용"], ["파일", "evidence/sanitized/users-active.csv 없음"]]
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [list(row) for row in csv.reader(handle)]


def word_blocks(
    blocks: list[tuple], images: dict[str, Path]
) -> tuple[list[dict], list[str], list[str]]:
    out: list[dict] = []
    used: list[str] = []
    missing: list[str] = []
    toc_done = False
    active_done = False
    for kind, value in blocks:
        if kind == "h2" and not toc_done:
            out.append({"type": "toc"})
            toc_done = True
        if kind == "ul":
            for item in value:
                out.append({"type": "p", "text": "• " + item})
            continue
        if kind == "table":
            out.append({"type": "table", "rows": value})
            continue
        out.append({"type": kind, "text": value})
        if kind != "p":
            continue
        if (not active_done) and ("JSON-F01-DIFF" in value or "users-active" in value):
            out.append(
                {
                    "type": "p",
                    "text": "공개 요약 evidence/sanitized/users-active.csv. 바뀐 값은 S05의 active뿐이다. 세션과 권한은 이 표에 없다.",
                }
            )
            out.append({"type": "table", "rows": active_rows()})
            active_done = True
        for eid in ID_RE.findall(value):
            if eid in used or eid in missing:
                continue
            if eid not in images:
                missing.append(eid)
                continue
            used.append(eid)
            note = NOTES.get(
                eid,
                "공개 화면이다. 세션, 직접 주소 차단, 완료 화면, 백업은 이 파일로 확인하지 않는다.",
            )
            out.append(
                {
                    "type": "image",
                    "path": str(images[eid]),
                    "text": "%s. 공개 경로 evidence/sanitized/%s.png. 관측 시각은 파일에 없다. %s"
                    % (eid, eid, note),
                }
            )
    if not active_done:
        out.append({"type": "h2", "text": "공개 active 요약"})
        out.append(
            {
                "type": "p",
                "text": "공개 요약 evidence/sanitized/users-active.csv. 바뀐 값은 S05의 active뿐이다. 세션과 권한은 이 표에 없다.",
            }
        )
        out.append({"type": "table", "rows": active_rows()})
    if missing:
        out.append(
            {
                "type": "p",
                "text": "공개 PNG가 없는 증적ID: "
                + ", ".join(missing)
                + ". 원본은 C:\\JY-Lab\\private-evidence\\ 에만 둔다.",
            }
        )
    return out, used, missing


def build(blocks: list[dict]) -> str:
    if sys.platform != "win32":
        raise SystemExit("PDF는 Windows Word에서만 만든다")
    handle = tempfile.NamedTemporaryFile(
        prefix="jy-report-", suffix=".json", delete=False
    )
    json_path = Path(handle.name)
    handle.close()
    json_path.write_text(json.dumps(blocks, ensure_ascii=False), encoding="utf-8-sig")
    ps = r"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $true
$word.DisplayAlerts = 0
$doc = $word.Documents.Add()
try { $doc.PageSetup.PaperSize = 7 } catch {}
try {
    $doc.PageSetup.TopMargin = $word.CentimetersToPoints(1.5)
    $doc.PageSetup.BottomMargin = $word.CentimetersToPoints(1.5)
    $doc.PageSetup.LeftMargin = $word.CentimetersToPoints(1.5)
    $doc.PageSetup.RightMargin = $word.CentimetersToPoints(1.5)
} catch {}
try {
    $normal = $doc.Styles.Item(-1)
    $normal.Font.NameFarEast = 'Malgun Gothic'
    $normal.Font.Name = 'Malgun Gothic'
    $normal.Font.Size = 10.5
} catch {}

function Add-Paragraph($doc, $text, $style) {
    if ([string]::IsNullOrWhiteSpace($text)) { return }
    $range = $doc.Range($doc.Content.End - 1, $doc.Content.End - 1)
    $start = $range.Start
    $range.InsertAfter([string]$text)
    $null = $range.InsertParagraphAfter()
    $styled = $doc.Range($start, $start + ([string]$text).Length)
    $styled.Style = $doc.Styles.Item([int]$style)
}

function Add-Table($doc, $rows) {
    $rowList = @($rows)
    if ($rowList.Count -lt 1) { return }
    $nCols = 1
    foreach ($row in $rowList) {
        $count = @($row).Count
        if ($count -gt $nCols) { $nCols = $count }
    }
    $range = $doc.Range($doc.Content.End - 1, $doc.Content.End - 1)
    $table = $doc.Tables.Add($range, $rowList.Count, $nCols)
    try { $table.PreferredWidthType = 2; $table.PreferredWidth = 100 } catch {}
    for ($r = 0; $r -lt $rowList.Count; $r++) {
        $cells = @($rowList[$r])
        for ($c = 0; $c -lt $nCols; $c++) {
            $val = ''
            if ($c -lt $cells.Count -and $null -ne $cells[$c]) { $val = [string]$cells[$c] }
            $table.Cell($r + 1, $c + 1).Range.Text = $val
        }
    }
    try { $table.Rows.Item(1).Range.Bold = $true } catch {}
    $end = $doc.Range($doc.Content.End - 1, $doc.Content.End - 1)
    $null = $end.InsertParagraphAfter()
}

function Add-Image($doc, $path, $caption) {
    $range = $doc.Range($doc.Content.End - 1, $doc.Content.End - 1)
    if (Test-Path -LiteralPath $path) {
        $shape = $doc.InlineShapes.AddPicture([string]$path, $false, $true, $range)
        $shape.LockAspectRatio = $true
        if ($shape.Width -gt 460) { $shape.Width = 460 }
    } else {
        Add-Paragraph $doc ('missing png ' + $path) -1
    }
    Add-Paragraph $doc $caption -1
}

$blocks = Get-Content -Raw -Encoding UTF8 $env:REPORT_JSON | ConvertFrom-Json
foreach ($block in @($blocks)) {
    switch ([string]$block.type) {
        'h1' { Add-Paragraph $doc $block.text -2 }
        'h2' { Add-Paragraph $doc $block.text -3 }
        'h3' { Add-Paragraph $doc $block.text -4 }
        'p' { Add-Paragraph $doc $block.text -1 }
        'toc' {
            $range = $doc.Range($doc.Content.End - 1, $doc.Content.End - 1)
            $null = $doc.TablesOfContents.Add($range, $true, 1, 2)
            $end = $doc.Range($doc.Content.End - 1, $doc.Content.End - 1)
            $null = $end.InsertParagraphAfter()
        }
        'table' { Add-Table $doc $block.rows }
        'image' { Add-Image $doc $block.path $block.text }
    }
}
if ($doc.TablesOfContents.Count -ge 1) { $doc.TablesOfContents.Item(1).Update() }
try { $doc.ActiveWindow.View.Type = 3 } catch {}
$doc.Repaginate()
$chars = $doc.Content.Text.Length
if ($chars -lt 2000) { throw ('TOO-SHORT ' + $chars) }
if (Test-Path -LiteralPath $env:REPORT_DOCX) { Remove-Item -LiteralPath $env:REPORT_DOCX -Force }
if (Test-Path -LiteralPath $env:REPORT_PDF) { Remove-Item -LiteralPath $env:REPORT_PDF -Force }
$doc.SaveAs2($env:REPORT_DOCX, 16)
$null = $doc.ExportAsFixedFormat($env:REPORT_PDF, 17)
$pages = $doc.ComputeStatistics(2)
$doc.Saved = $true
$doc.Close($false)
$word.Quit()
Write-Output ('chars ' + $chars)
Write-Output ('pages ' + $pages)
"""
    env = dict(os.environ)
    env["REPORT_JSON"] = str(json_path)
    env["REPORT_DOCX"] = str(DOCX)
    env["REPORT_PDF"] = str(PDF)
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            check=False,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
        )
    finally:
        json_path.unlink(missing_ok=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit("Word 생성 실패")
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines[-1] if lines else "쪽수 없음"


def main() -> None:
    md = MD.read_text(encoding="utf-8")
    require(md)
    images = {path.stem: path for path in SAN.glob("*.png")} if SAN.exists() else {}
    blocks, used, missing = word_blocks(parse(md), images)
    OUT.mkdir(parents=True, exist_ok=True)
    pages = build(blocks)
    print("embedded\t" + (", ".join(used) if used else "없음"))
    print("missing-png\t" + (", ".join(missing) if missing else "없음"))
    for path in (DOCX, PDF):
        if path.exists():
            print("%s\t%s" % (path.name, path.stat().st_size))
        else:
            print("%s\tMISSING" % path.name)
    print(pages)


if __name__ == "__main__":
    main()
