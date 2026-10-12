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
    hashes = re.findall(r"[0-9a-f]{64}", text)
    assert len(hashes) == 21
    assert len(set(hashes)) == 21


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
