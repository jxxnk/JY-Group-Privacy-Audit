from __future__ import annotations
import json, os, sys, urllib.request
BASE = os.environ.get("ZAMMAD_URL", "http://127.0.0.1:8080").rstrip("/")
TOKEN = (os.environ.get("ZAMMAD_TOKEN") or "").strip()

def get(path: str):
    req = urllib.request.Request(BASE + path, headers={"Authorization": "Token token=" + TOKEN, "Accept": "application/json"}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main() -> int:
    if not TOKEN:
        print("환경 변수 ZAMMAD_TOKEN 이 없습니다.", file=sys.stderr)
        return 2
    tickets = get("/api/v1/tickets?per_page=100")
    print("tickets", len(tickets))
    for t in tickets:
        print(t.get("id"), t.get("number"), t.get("title"), "state", t.get("state_id"), "group", t.get("group_id"))
    print("---groups---")
    for g in get("/api/v1/groups"):
        print(g.get("id"), g.get("name"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
