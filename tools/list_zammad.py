"""List local Zammad tickets/groups using GET requests only."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from urllib.parse import urlsplit

ALLOWED_HOSTS = {"127.0.0.1", "localhost"}
ALLOWED_PORT = 8080
DEFAULT_URL = "http://127.0.0.1:8080"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_base_url(raw: str) -> str:
    value = raw.strip().rstrip("/")
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise ValueError(f"잘못된 ZAMMAD_URL: {exc}") from exc

    if (
        parsed.scheme != "http"
        or parsed.hostname not in ALLOWED_HOSTS
        or port != ALLOWED_PORT
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            "ZAMMAD_URL은 http://127.0.0.1:8080 또는 "
            "http://localhost:8080만 허용합니다."
        )
    return f"http://{parsed.hostname}:{port}"


def get_json(base_url: str, token: str, path: str):
    req = urllib.request.Request(
        base_url + path,
        headers={
            "Authorization": f"Token token={token}",
            "Accept": "application/json",
        },
        method="GET",
    )
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        NoRedirect(),
    )
    with opener.open(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    try:
        base_url = validate_base_url(os.environ.get("ZAMMAD_URL", DEFAULT_URL))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    token = (os.environ.get("ZAMMAD_TOKEN") or "").strip()
    if not token:
        print("환경 변수 ZAMMAD_TOKEN 이 없습니다.", file=sys.stderr)
        return 2

    try:
        tickets = get_json(base_url, token, "/api/v1/tickets?per_page=100")
        print("tickets", len(tickets))
        for ticket in tickets:
            print(
                ticket.get("id"),
                ticket.get("number"),
                ticket.get("title"),
                "state",
                ticket.get("state_id"),
                "group",
                ticket.get("group_id"),
            )

        print("---groups---")
        for group in get_json(base_url, token, "/api/v1/groups"):
            print(group.get("id"), group.get("name"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"조회 실패: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())