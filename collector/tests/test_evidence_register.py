"""Public evidence hash register stays complete and free of raw evidence."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "docs" / "evidence-hashes.md"

REQUIRED_PATHS = (
    r"before\users-before.json",
    r"after\users-after-f01.json",
    r"after\users-diff.json",
    r"after\jy-doc02-copy.txt",
)


def test_register_has_twenty_one_unique_hashes() -> None:
    text = REGISTER.read_text(encoding="utf-8")
    head, marker, tail = text.partition("## 2026-10-14 재계산")
    assert marker
    first = re.findall(r"[0-9a-f]{64}", head)
    later = re.findall(r"[0-9a-f]{64}", tail)
    assert len(first) == 21
    assert len(set(first)) == 21
    assert set(later) - set(first) == {
        "d94f7cb9cf1191f79a34df5c13061239aa5fdb0f884ada71483c7743c69f023f",
        "d94e86cd325051ff98b8f4dcd9de31e4440fba6d1c48321e416e498998c51347",
        "5680e5263c36d398ead884fb6810be17781ce622346fcc62d40126c0ec72c783",
    }


def test_register_names_the_lab_json_outputs() -> None:
    text = REGISTER.read_text(encoding="utf-8")
    for path in REQUIRED_PATHS:
        assert path in text
    assert "diff 명령이 없어" in text


def test_register_does_not_embed_secrets_or_raw_files() -> None:
    text = REGISTER.read_text(encoding="utf-8")
    assert "ZAMMAD_TOKEN" not in text
    assert "Authorization" not in text
    assert "```" not in text
