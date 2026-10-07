"""JY lab evidence collector — GET localhost Zammad users only."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ALLOWED_HOSTS = {"127.0.0.1", "localhost"}
ALLOWED_PORTS = {8080, None}
ROSTER_SUFFIX = ".example.test"
DEFAULT_URL = "http://127.0.0.1:8080"
USERS_PATH = "/api/v1/users"


class EvidenceError(Exception):
    def __init__(self, message: str, code: int = 2) -> None:
        super().__init__(message)
        self.code = code


def die(message: str, code: int = 2) -> None:
    raise EvidenceError(message, code)


def load_roster(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        die(f"명부가 없습니다: {path}")
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or "email" not in reader.fieldnames:
            die("staff.csv에 email 열이 있어야 합니다.")
        for i, row in enumerate(reader, 2):
            email = (row.get("email") or "").strip()
            staff_id = (row.get("staff_id") or "").strip()
            end_date = (row.get("end_date") or "").strip()
            if not email:
                die(f"{path}:{i} 이메일이 비어 있습니다.")
            if not email.lower().endswith(ROSTER_SUFFIX):
                die(f"{path}:{i} 이메일이 {ROSTER_SUFFIX}로 끝나야 합니다: {email}")
            rows.append({"staff_id": staff_id, "email": email, "end_date": end_date})
    if not rows:
        die("명부에 직원이 없습니다.")
    return rows


def validate_base_url(url: str) -> str:
    raw = (url or "").strip().rstrip("/")
    parsed = urlparse(raw)
    if parsed.scheme != "http":
        die(f"http만 허용합니다: {url}")
    if parsed.hostname not in ALLOWED_HOSTS:
        die(f"localhost/127.0.0.1만 허용합니다: {url}")
    if parsed.port not in ALLOWED_PORTS and parsed.port != 8080:
        die(f"포트 8080만 허용합니다: {url}")
    if parsed.path not in ("", "/"):
        die(f"경로가 있는 URL은 쓰지 않습니다: {url}")
    if parsed.query or parsed.fragment or parsed.username or parsed.password:
        die(f"질의·자격증명이 있는 URL은 쓰지 않습니다: {url}")
    return f"http://{parsed.hostname}:8080" if parsed.port in (None, 8080) else raw


def canonical_json(payload: Any) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json_and_hash(out: Path, payload: Any) -> str:
    out.parent.mkdir(parents=True, exist_ok=True)
    blob = canonical_json(payload)
    digest = sha256_bytes(blob)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_bytes(blob)
    tmp.replace(out)
    out.with_suffix(out.suffix + ".sha256").write_text(f"{digest}  {out.name}\n", encoding="utf-8")
    return digest


def token_from_env() -> str:
    token = (os.environ.get("ZAMMAD_TOKEN") or os.environ.get("JY_ZAMMAD_TOKEN") or "").strip()
    if not token:
        die("환경 변수 ZAMMAD_TOKEN 이 없습니다. 값은 채팅·커밋·캡처에 넣지 마세요.")
    return token


def get_json(base_url: str, path: str, token: str) -> Any:
    if not path.startswith("/"):
        die(f"절대 경로만 호출합니다: {path}")
    if path != USERS_PATH and not path.startswith(USERS_PATH + "?"):
        die(f"허용된 GET 경로는 {USERS_PATH} 뿐입니다: {path}")
    url = base_url + path
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Authorization": f"Token token={token}",
            "Accept": "application/json",
            "User-Agent": "jy-evidence-local/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                die(f"HTTP {resp.status}: {url}")
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        die(f"HTTP {exc.code} {exc.reason}: GET {USERS_PATH} 실패. 토큰 권한·API 토큰 접근을 확인하세요.")
    except urllib.error.URLError as exc:
        die(f"연결 실패: {exc.reason}. Docker Desktop과 Zammad(127.0.0.1:8080)를 확인하세요.")


def fetch_users(base_url: str, token: str, getter=get_json) -> list[dict[str, Any]]:
    page = 1
    found: list[dict[str, Any]] = []
    while True:
        chunk = getter(base_url, f"{USERS_PATH}?expand=false&per_page=100&page={page}", token)
        if not isinstance(chunk, list):
            die("사용자 API 응답이 목록이 아닙니다.")
        found.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1
        if page > 20:
            die("사용자 페이지가 비정상적으로 깁니다.")
    return found


def snapshot(roster: list[dict[str, str]], zammad_users: list[dict[str, Any]], base_url: str) -> dict[str, Any]:
    by_email = {}
    for user in zammad_users:
        email = str(user.get("email") or "").strip().lower()
        if email:
            by_email[email] = user
    records = []
    for row in roster:
        key = row["email"].lower()
        user = by_email.get(key)
        records.append(
            {
                "staff_id": row["staff_id"],
                "email": row["email"],
                "end_date": row["end_date"] or None,
                "found": bool(user),
                "zammad_id": user.get("id") if user else None,
                "login": user.get("login") if user else None,
                "active": user.get("active") if user else None,
                "firstname": user.get("firstname") if user else None,
                "lastname": user.get("lastname") if user else None,
            }
        )
    return {
        "lab": "JY-Group-Privacy-Audit",
        "collected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "base_url": base_url,
        "http_method": "GET",
        "path": USERS_PATH,
        "note": "token omitted; GET localhost only",
        "roster_count": len(roster),
        "zammad_user_count": len(zammad_users),
        "users": records,
    }


def cmd_collect(args: argparse.Namespace) -> int:
    roster = load_roster(Path(args.roster))
    base_url = validate_base_url(os.environ.get("ZAMMAD_URL", DEFAULT_URL) if not args.url else args.url)
    token = token_from_env()
    users = fetch_users(base_url, token)
    payload = snapshot(roster, users, base_url)
    digest = write_json_and_hash(Path(args.out), payload)
    missing = [u["email"] for u in payload["users"] if not u["found"]]
    s05 = next((u for u in payload["users"] if u["staff_id"] == "S05"), None)
    print(f"wrote {args.out}")
    print(f"sha256 {digest}")
    if missing:
        print("명부에는 있으나 Zammad에서 못 찾음: " + ", ".join(missing), file=sys.stderr)
    if s05:
        print(f"S05 active={s05['active']} end_date={s05['end_date']}")
    return 0


def cmd_hash(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        die(f"파일이 없습니다: {path}")
    digest = sha256_bytes(path.read_bytes())
    print(f"{digest}  {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="JY local Zammad GET-only evidence collector")
    sub = parser.add_subparsers(dest="command", required=True)
    collect = sub.add_parser("collect", help="명부와 사용자 Active 상태를 JSON+SHA256으로 저장")
    collect.add_argument("--roster", required=True)
    collect.add_argument("--out", required=True)
    collect.add_argument("--url", default=None)
    collect.set_defaults(func=cmd_collect)
    hashed = sub.add_parser("hash", help="이미 있는 파일 SHA256")
    hashed.add_argument("--file", required=True)
    hashed.set_defaults(func=cmd_hash)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EvidenceError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(exc.code)
