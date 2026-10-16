"""Offline selected-release checks. No network, credentials or live lab calls."""

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

LIST = "docs/delivery-files.txt"
EXTRA = {"BUILD_INFO.txt", "SHA256SUMS.csv"}
BLOCKED = {
    ".git",
    ".venv",
    "private-evidence",
    "zammad-runtime",
    "backups",
    "__pycache__",
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True
    ).stdout


def safe_path(value):
    p = PurePosixPath(value)
    if (
        not value
        or value != value.strip()
        or p.is_absolute()
        or p.as_posix() != value
        or any(x in {".", ".."} for x in value.split("/"))
        or re.search(r"[\\:*?\[\]\x00-\x1f]", value)
        or any(x.lower() in BLOCKED or x.lower().startswith(".env") for x in p.parts)
    ):
        raise ValueError("Excluded or invalid relative path")
    return value


def delivery_list(raw):
    rows = raw.decode("utf-8-sig").splitlines()
    if any(not x.strip() for x in rows):
        raise ValueError("Delivery list must contain only nonempty file paths")
    for row in rows:
        safe_path(row)
    if not rows or len(set(x.casefold() for x in rows)) != len(rows):
        raise ValueError("Empty or duplicate delivery list")
    if LIST not in rows or set(rows) & EXTRA:
        raise ValueError("List must include itself and exclude generated metadata")
    return rows


def check_links(files):
    """Check ordinary Markdown/HTML local links, not PDF/Office links or anchors."""
    for name, raw in files.items():
        if Path(name).suffix.lower() not in {".md", ".html", ".htm"}:
            continue
        text = raw.decode("utf-8-sig")
        text = re.sub(r"```[\s\S]*?```", "", text)
        text = re.sub(r"`[^`]*`", "", text)
        targets = re.findall(r"\]\(([^\s)]+)\)", text)
        targets += re.findall(r"(?:href|src)=[\"']([^\"']+)[\"']", text)
        for target in targets:
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = unquote(parsed.path)
            if path.startswith("/") or "\\" in path:
                raise ValueError("Local link must be package relative: " + name)
            parts = list(PurePosixPath(name).parent.parts)
            for part in path.split("/"):
                if part == "..":
                    if not parts:
                        raise ValueError("Link escapes package: " + name)
                    parts.pop()
                elif part not in {"", "."}:
                    parts.append(part)
            dest = "/".join(parts)
            if dest not in files and not any(x.startswith(dest + "/") for x in files):
                raise ValueError(
                    "Missing selected link target: " + name + " -> " + dest
                )


def selected_files(repo, ref):
    entries = {}
    for row in git(repo, "ls-tree", "-r", "-z", ref).split(b"\0"):
        if not row:
            continue
        head, path = row.split(b"\t", 1)
        mode, kind, oid = head.decode().split()
        entries[path.decode("utf-8")] = (mode, kind, oid)
    if LIST not in entries:
        raise ValueError("Delivery list is absent from selected commit")
    rows = delivery_list(git(repo, "cat-file", "blob", entries[LIST][2]))
    files = {}
    for name in rows:
        if name not in entries or entries[name][0] not in {"100644", "100755"}:
            raise ValueError(
                "Selected path is absent or not a regular Git blob: " + name
            )
        files[name] = git(repo, "cat-file", "blob", entries[name][2])
    check_links(files)
    return files


def check(repo, ref):
    files = selected_files(repo, ref)
    print("Selected files and ordinary local links checked:", len(files))
    print("Manual PDF/Office/image/legal/content review is still required")


def pack(repo, tag, out):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", tag):
        raise ValueError("Use a simple release tag name")
    if git(repo, "status", "--porcelain").strip():
        raise ValueError("Working tree must be clean")
    commit = git(repo, "rev-parse", tag + "^{commit}").decode().strip()
    if git(repo, "cat-file", "-t", tag).strip() != b"tag":
        raise ValueError("Release tag must be annotated")
    for ref in ("HEAD", "origin/main"):
        if git(repo, "rev-parse", ref).decode().strip() != commit:
            raise ValueError("HEAD, fetched origin/main and tag must match")
    if out.resolve().is_relative_to(repo.resolve()):
        raise ValueError("Build outside the repository")
    files = selected_files(repo, tag)
    out.mkdir(parents=True, exist_ok=False)
    stage = out / "files"
    stage.mkdir()
    info = {
        "tag": tag,
        "commit": commit,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "source": "exact Git blob bytes; no checkout EOL conversion",
        "delivery_list": LIST,
    }
    files["BUILD_INFO.txt"] = (
        json.dumps(info, ensure_ascii=False, indent=2) + "\n"
    ).encode()
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["Path", "SHA256"])
    writer.writerows((name, sha(raw)) for name, raw in sorted(files.items()))
    files["SHA256SUMS.csv"] = stream.getvalue().encode("utf-8")
    for name, raw in files.items():
        target = stage / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    archive = out / ("JY-Final-" + tag + ".zip")
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as z:
        for name, raw in sorted(files.items()):
            z.writestr(name, raw)
    hashfile = Path(str(archive) + ".sha256.txt")
    hashfile.write_text(
        sha(archive.read_bytes()) + "  " + archive.name + "\n", encoding="ascii"
    )
    verify(archive, hashfile, None)
    for name, raw in selected_files(repo, tag).items():
        if (stage / name).read_bytes() != raw:
            raise ValueError("Stage differs from Git blob")
    print("Built once; freeze these files. ZIP:", archive.name)


def verify(archive, hashfile, extract):
    expected = hashfile.read_text(encoding="utf-8-sig").split()[0]
    if not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
        raise ValueError("Invalid ZIP digest")
    if sha(archive.read_bytes()).lower() != expected.lower():
        raise ValueError("ZIP digest mismatch")
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        if len(set(x.casefold() for x in names)) != len(names):
            raise ValueError("Duplicate archive paths")
        for name in names:
            safe_path(name)
        files = {name: z.read(name) for name in names}
    rows = delivery_list(files[LIST])
    if set(files) != set(rows) | EXTRA:
        raise ValueError("Extra or missing archive file")
    hashes = list(
        csv.DictReader(io.StringIO(files["SHA256SUMS.csv"].decode("utf-8-sig")))
    )
    if not hashes or any(set(row) != {"Path", "SHA256"} for row in hashes):
        raise ValueError("Invalid manifest columns")
    paths = [row["Path"] for row in hashes]
    if len(set(paths)) != len(paths) or set(paths) != set(rows) | {"BUILD_INFO.txt"}:
        raise ValueError("Manifest file set differs")
    for row in hashes:
        if sha(files[row["Path"]]).lower() != row["SHA256"].lower():
            raise ValueError("File digest mismatch: " + row["Path"])
    info = json.loads(files["BUILD_INFO.txt"])
    if not re.fullmatch(r"[0-9a-f]{40,64}", info.get("commit", "")):
        raise ValueError("Build commit missing")
    check_links(files)
    if extract is not None:
        extract.mkdir(parents=True, exist_ok=False)
        for name, raw in files.items():
            target = extract / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
    print("ZIP hash, exact file set, per-file hashes and ordinary local links verified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    chk = sub.add_parser("check")
    chk.add_argument("--repo", type=Path, default=Path("."))
    chk.add_argument("--ref", default="HEAD")
    build = sub.add_parser("pack")
    build.add_argument("--repo", type=Path, default=Path("."))
    build.add_argument("--tag", required=True)
    build.add_argument("--out", type=Path, required=True)
    ver = sub.add_parser("verify")
    ver.add_argument("--zip", type=Path, required=True)
    ver.add_argument("--hash-file", type=Path, required=True)
    ver.add_argument("--extract", type=Path)
    args = parser.parse_args()
    if args.command == "check":
        check(args.repo, args.ref)
    elif args.command == "pack":
        pack(args.repo, args.tag, args.out)
    else:
        verify(args.zip, args.hash_file, args.extract)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAILED:", type(exc).__name__, file=sys.stderr)
        if isinstance(exc, ValueError):
            print(str(exc), file=sys.stderr)
        sys.exit(1)
