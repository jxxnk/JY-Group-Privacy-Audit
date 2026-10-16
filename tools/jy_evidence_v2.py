"""Version 2: local GET evidence; never a legal compliance verdict."""

import argparse
import csv
import getpass
import hashlib
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib import request
from urllib.parse import urlsplit

SCHEMA = "jy-evidence-v2"
BASE = "http://127.0.0.1:8080"
STAFF_IDS = {f"S{i:02}" for i in range(1, 7)}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def validate_base(value):
    parsed = urlsplit(value)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"localhost", "127.0.0.1"}
        or parsed.port != 8080
        or parsed.path not in {"", "/"}
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Only loopback HTTP port 8080 is allowed")
    return f"http://{parsed.hostname}:8080"


def load_roster(path):
    raw = Path(path).read_bytes()
    rows = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    if len(rows) != 6:
        raise ValueError("Expected exactly six staff rows")
    seen_ids, seen_emails = set(), set()
    cleaned = []
    for row in rows:
        sid = (row.get("staff_id") or "").strip()
        email = (row.get("email") or "").strip().lower()
        end = (row.get("end_date") or "").strip()
        if (
            sid not in STAFF_IDS
            or sid in seen_ids
            or email in seen_emails
            or email.count("@") != 1
            or not email.endswith(".example.test")
        ):
            raise ValueError("Invalid, duplicate or missing staff identity")
        if end:
            date.fromisoformat(end)
        seen_ids.add(sid)
        seen_emails.add(email)
        cleaned.append({"staff_id": sid, "email": email, "end_date": end})
    if seen_ids != STAFF_IDS:
        raise ValueError("Staff set differs from S01-S06")
    return cleaned, digest(raw)


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def make_opener():
    return request.build_opener(request.ProxyHandler({}), NoRedirect())


def get_page(base, token, page):
    base = validate_base(base)
    req = request.Request(
        f"{base}/api/v1/users?page={page}&per_page=100&expand=false",
        method="GET",
        headers={"Authorization": "Token token=" + token, "Accept": "application/json"},
    )
    with make_opener().open(req, timeout=20) as resp:
        return json.load(resp)


def collect_users(fetch):
    records, seen = [], set()
    for page in range(1, 101):
        batch = fetch(page)
        if not isinstance(batch, list):
            raise ValueError("API response must be a list")
        if not batch:
            return records
        for user in batch:
            if not isinstance(user, dict):
                raise ValueError("API record must be an object")
            uid = user.get("id")
            if type(uid) is not int or uid <= 0 or uid in seen:
                raise ValueError("Invalid ID, duplicate record or repeated page")
            seen.add(uid)
            records.append(user)
    raise ValueError("Pagination limit reached; completeness unknown")


def select_staff(users, roster):
    selected = []
    for row in roster:
        matches = [
            u
            for u in users
            if str(u.get("email") or "").strip().lower() == row["email"]
        ]
        if len(matches) != 1:
            raise ValueError("Missing or duplicate staff match: " + row["staff_id"])
        user = matches[0]
        if type(user.get("active")) is not bool:
            raise ValueError("Active must be a JSON boolean")
        selected.append(
            {
                "staff_id": row["staff_id"],
                "id": user["id"],
                "active": user["active"],
                "end_date": row["end_date"],
            }
        )
    return selected


def write_evidence(path, payload):
    path = Path(path)
    sidecar = Path(str(path) + ".sha256")
    if path.exists() or sidecar.exists():
        raise ValueError("Refusing to overwrite evidence or sidecar")
    raw = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    with sidecar.open("x", encoding="ascii") as stream:
        stream.write(digest(raw) + "\n")
    return digest(raw)


def read_evidence(path):
    path = Path(path)
    raw = path.read_bytes()
    expected = Path(str(path) + ".sha256").read_text(encoding="ascii").strip()
    if len(expected) != 64 or digest(raw).lower() != expected.lower():
        raise ValueError("Evidence hash mismatch")
    return json.loads(raw)


def timestamp(value):
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError("Timestamp must include timezone")
    return result


def validate_digest(value):
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-fA-F]{64}", value) is None:
        raise ValueError("Digest must be 64 hexadecimal characters")


def validate_diff(data):
    if not isinstance(data, dict) or data.get("schema") != "jy-evidence-v2-diff":
        raise ValueError("Not a v2 diff")
    timestamp(data["created_at"])
    for key in ("before_sha256", "after_sha256"):
        validate_digest(data[key])
    if not isinstance(data["changes"], list):
        raise ValueError("Changes must be a list")
    seen = set()
    for row in data["changes"]:
        if not isinstance(row, dict):
            raise ValueError("Change must be an object")
        sid = row.get("staff_id")
        if sid not in STAFF_IDS or sid in seen or row.get("field") != "active":
            raise ValueError("Invalid or duplicate change")
        seen.add(sid)
        if type(row.get("before")) is not bool or type(row.get("after")) is not bool:
            raise ValueError("Change values must be booleans")
        if row["before"] == row["after"]:
            raise ValueError("Unchanged value recorded as a change")


def validate_evidence(data):
    if not isinstance(data, dict):
        raise ValueError("Evidence must be an object")
    if data.get("schema") == SCHEMA:
        validate_snapshot(data)
    elif data.get("schema") == "jy-evidence-v2-diff":
        validate_diff(data)
    else:
        raise ValueError("Unknown schema; use --hash-only for historical evidence")


def validate_snapshot(data):
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ValueError("Not a v2 snapshot; do not rewrite historical evidence")
    validate_base(data["base"])
    validate_digest(data["roster_sha256"])
    start, end = timestamp(data["started_at"]), timestamp(data["finished_at"])
    if start > end:
        raise ValueError("Snapshot time is reversed")
    records = data["staff"]
    if not isinstance(records, list) or not all(isinstance(x, dict) for x in records):
        raise ValueError("Snapshot staff must be a list of objects")
    if len(records) != 6 or {x["staff_id"] for x in records} != STAFF_IDS:
        raise ValueError("Snapshot staff set must be S01-S06")
    ids = set()
    for record in records:
        uid = record["id"]
        if type(uid) is not int or uid <= 0 or uid in ids:
            raise ValueError("Invalid or duplicate account ID")
        ids.add(uid)
        if type(record["active"]) is not bool:
            raise ValueError("Invalid active value")
        if not isinstance(record["end_date"], str):
            raise ValueError("End date must be a string")
        if record["end_date"]:
            date.fromisoformat(record["end_date"])


def compare(before, after):
    validate_snapshot(before)
    validate_snapshot(after)
    if before["base"] != after["base"]:
        raise ValueError("Target URL changed")
    if before["roster_sha256"] != after["roster_sha256"]:
        raise ValueError("Roster changed")
    if timestamp(before["finished_at"]) >= timestamp(after["started_at"]):
        raise ValueError("Snapshots overlap or are reversed")
    old = {x["staff_id"]: x for x in before["staff"]}
    new = {x["staff_id"]: x for x in after["staff"]}
    changes = []
    for sid in sorted(STAFF_IDS):
        if old[sid]["id"] != new[sid]["id"]:
            raise ValueError("Account recreated: " + sid)
        if old[sid]["end_date"] != new[sid]["end_date"]:
            raise ValueError("Staff metadata changed")
        if old[sid]["active"] != new[sid]["active"]:
            changes.append(
                {
                    "staff_id": sid,
                    "field": "active",
                    "before": old[sid]["active"],
                    "after": new[sid]["active"],
                }
            )
    return {
        "schema": "jy-evidence-v2-diff",
        "created_at": utcnow(),
        "changes": changes,
        "limitation": "Active configuration only, not login/session/permission/legal verification",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    col = sub.add_parser("collect")
    col.add_argument("--roster", required=True, type=Path)
    col.add_argument("--out", required=True, type=Path)
    col.add_argument("--url", default=BASE)
    diff = sub.add_parser("diff")
    diff.add_argument("--before", required=True, type=Path)
    diff.add_argument("--after", required=True, type=Path)
    diff.add_argument("--out", required=True, type=Path)
    ver = sub.add_parser("verify")
    ver.add_argument("--file", required=True, type=Path)
    ver.add_argument("--hash-only", action="store_true")
    args = parser.parse_args()
    if args.command == "verify":
        data = read_evidence(args.file)
        if args.hash_only:
            print("HASH ONLY verified; schema and content were not validated")
        else:
            validate_evidence(data)
            print("HASH AND SCHEMA verified; no authenticity or compliance verdict")
        return
    if args.out.exists() or Path(str(args.out) + ".sha256").exists():
        raise ValueError("Output already exists; choose a new name")
    if args.command == "diff":
        before, after = read_evidence(args.before), read_evidence(args.after)
        result = compare(before, after)
        result["before_sha256"] = digest(args.before.read_bytes())
        result["after_sha256"] = digest(args.after.read_bytes())
        validate_diff(result)
    else:
        base = validate_base(args.url)
        roster, sha = load_roster(args.roster)
        token = getpass.getpass("Token: ").strip()
        if not token or "\r" in token or "\n" in token:
            raise ValueError("Invalid token")
        started = utcnow()
        users = collect_users(lambda page: get_page(base, token, page))
        staff = select_staff(users, roster)
        if digest(args.roster.read_bytes()) != sha:
            raise ValueError("Roster changed during collection")
        result = {
            "schema": SCHEMA,
            "tool_version": "2.1-closeout",
            "base": base,
            "started_at": started,
            "finished_at": utcnow(),
            "roster_sha256": sha,
            "staff": staff,
            "flags": [
                x["staff_id"]
                for x in staff
                if x["active"]
                and x["end_date"]
                and date.fromisoformat(x["end_date"]) < date.today()
            ],
            "limitation": "Local Active configuration only; user must confirm same instance",
        }
        validate_snapshot(result)
    sha = write_evidence(args.out, result)
    print("Saved new evidence and sidecar. SHA256:", sha)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Never echo credentials, URLs or HTTP response bodies.
        print("FAILED:", type(exc).__name__, file=sys.stderr)
        if isinstance(exc, ValueError):
            print(str(exc), file=sys.stderr)
        sys.exit(1)
