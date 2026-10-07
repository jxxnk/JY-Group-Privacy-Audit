"""Server-less tests for tools/jy_evidence.py."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import jy_evidence as jy


def _roster(path: Path, extra: str = "") -> Path:
    path.write_text(
        "staff_id,email,end_date\n"
        "S01,admin@jy.example.test,\n"
        "S05,former@service.example.test,2026-09-14\n" + extra,
        encoding="utf-8",
    )
    return path


class UrlAndRosterTests(unittest.TestCase):
    def test_accepts_loopback_http_8080(self) -> None:
        self.assertEqual(jy.validate_base_url("http://127.0.0.1:8080"), "http://127.0.0.1:8080")
        self.assertEqual(jy.validate_base_url("http://localhost:8080/"), "http://localhost:8080")

    def test_rejects_remote_or_https(self) -> None:
        with self.assertRaises(jy.EvidenceError):
            jy.validate_base_url("https://zammad.example.com")
        with self.assertRaises(jy.EvidenceError):
            jy.validate_base_url("http://8.8.8.8:8080")
        with self.assertRaises(jy.EvidenceError):
            jy.validate_base_url("http://127.0.0.1:3000")

    def test_rejects_non_example_test_email(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "staff.csv"
            _roster(csv_path, "S99,admin@naver.com,\n")
            with self.assertRaises(jy.EvidenceError):
                jy.load_roster(csv_path)

    def test_loads_lab_roster(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rows = jy.load_roster(_roster(Path(tmp) / "staff.csv"))
        self.assertEqual(rows[1]["staff_id"], "S05")
        self.assertEqual(rows[1]["end_date"], "2026-09-14")


class SnapshotAndHashTests(unittest.TestCase):
    def test_snapshot_marks_active_and_omits_token(self) -> None:
        roster = [
            {"staff_id": "S05", "email": "former@service.example.test", "end_date": "2026-09-14"},
            {"staff_id": "S06", "email": "maint@vendor.example.test", "end_date": ""},
        ]
        users = [
            {
                "id": 42,
                "email": "former@service.example.test",
                "login": "former@service.example.test",
                "active": True,
                "firstname": "Former",
                "lastname": "Agent",
            }
        ]
        payload = jy.snapshot(roster, users, "http://127.0.0.1:8080")
        blob = jy.canonical_json(payload).decode("utf-8")
        self.assertNotIn("Authorization", blob)
        self.assertNotIn("Token token=", blob)
        self.assertIs(payload["users"][0]["active"], True)
        self.assertTrue(payload["users"][1]["found"] is False)
        self.assertEqual(payload["http_method"], "GET")

    def test_hash_is_stable(self) -> None:
        payload = {"b": 1, "a": True}
        self.assertEqual(jy.sha256_bytes(jy.canonical_json(payload)), jy.sha256_bytes(jy.canonical_json({"a": True, "b": 1})))

    def test_write_json_and_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "users-before.json"
            digest = jy.write_json_and_hash(out, {"ok": True})
            self.assertTrue(out.is_file())
            sidecar = Path(str(out) + ".sha256")
            self.assertEqual(sidecar.read_text(encoding="utf-8").split()[0], digest)
            self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["ok"], True)

    def test_fetch_users_is_get_only(self) -> None:
        calls: list[str] = []

        def fake_get(base_url: str, path: str, token: str):
            self.assertEqual(base_url, "http://127.0.0.1:8080")
            self.assertTrue(path.startswith("/api/v1/users"))
            self.assertEqual(token, "secret")
            calls.append(path)
            return [{"id": 1, "email": "admin@jy.example.test", "active": True}]

        users = jy.fetch_users("http://127.0.0.1:8080", "secret", getter=fake_get)
        self.assertEqual(len(users), 1)
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
