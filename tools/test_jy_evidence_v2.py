"""Offline regression tests. No real credentials or live Zammad requests."""

import copy
import tempfile
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib import request

import jy_evidence_v2 as jy


class EvidenceTests(unittest.TestCase):
    def roster(self):
        return [
            {"staff_id": f"S{i:02}", "email": f"s{i}@jy.example.test", "end_date": ""}
            for i in range(1, 7)
        ]

    def users(self):
        return [
            {"id": i, "email": row["email"], "active": True}
            for i, row in enumerate(self.roster(), 1)
        ]

    def snapshots(self):
        before = {
            "schema": jy.SCHEMA,
            "base": jy.BASE,
            "started_at": "2026-01-01T00:00:00+00:00",
            "finished_at": "2026-01-01T00:01:00+00:00",
            "roster_sha256": "a" * 64,
            "staff": jy.select_staff(self.users(), self.roster()),
        }
        after = copy.deepcopy(before)
        after["started_at"] = "2026-01-01T01:00:00+00:00"
        after["finished_at"] = "2026-01-01T01:01:00+00:00"
        return before, after

    def write_roster(self, path, rows):
        text = "staff_id,email,end_date\n" + "".join(
            f"{r['staff_id']},{r['email']},{r['end_date']}\n" for r in rows
        )
        path.write_text(text, encoding="utf-8")

    def test_valid_six_row_roster(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "staff.csv"
            self.write_roster(path, self.roster())
            rows, sha = jy.load_roster(path)
            self.assertEqual(len(rows), 6)
            self.assertEqual(sha, jy.digest(path.read_bytes()))

    def test_roster_missing_duplicate_bad_date_rejected(self):
        valid = self.roster()
        variants = [valid[:5]]
        for field, value in [
            ("staff_id", "S01"),
            ("email", valid[0]["email"]),
            ("end_date", "not-a-date"),
            ("email", "a@real.com"),
        ]:
            rows = copy.deepcopy(valid)
            rows[-1][field] = value
            variants.append(rows)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "staff.csv"
            for rows in variants:
                with self.subTest(rows=rows):
                    self.write_roster(path, rows)
                    with self.assertRaises(ValueError):
                        jy.load_roster(path)

    def test_loopback_boundary(self):
        self.assertEqual(jy.validate_base(jy.BASE), jy.BASE)
        for value in [
            "http://8.8.8.8:8080",
            "https://localhost:8080",
            "http://localhost:80",
            "http://localhost:8080/x",
            "http://a:b@localhost:8080",
            "http://localhost:8080?x=1",
        ]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                jy.validate_base(value)

    def test_redirect_is_blocked(self):
        result = jy.NoRedirect().redirect_request(
            None, None, 302, "", {}, "http://external"
        )
        self.assertIsNone(result)

    def test_proxy_disabled(self):
        with patch.object(request, "build_opener") as build:
            jy.make_opener()
        handlers = build.call_args.args
        self.assertEqual(handlers[0].proxies, {})
        self.assertIsInstance(handlers[1], jy.NoRedirect)

    def test_pagination_until_empty(self):
        calls = []

        def fetch(page):
            calls.append(page)
            return [{"id": page}] if page < 3 else []

        self.assertEqual(len(jy.collect_users(fetch)), 2)
        self.assertEqual(calls, [1, 2, 3])

    def test_duplicate_page_rejected(self):
        with self.assertRaises(ValueError):
            jy.collect_users(lambda _: [{"id": 1}])

    def test_bad_api_shape_rejected(self):
        for batch in [{"error": "x"}, [None], [{"id": True}]]:
            with self.subTest(batch=batch), self.assertRaises(ValueError):
                jy.collect_users(lambda _: batch)

    def test_missing_duplicate_email_rejected(self):
        for users in [self.users()[:-1], self.users() + [self.users()[0]]]:
            with self.assertRaises(ValueError):
                jy.select_staff(users, self.roster())

    def test_boolean_string_rejected(self):
        users = self.users()
        users[0]["active"] = "false"
        with self.assertRaises(ValueError):
            jy.select_staff(users, self.roster())

    def test_diff_identifies_s05(self):
        before, after = self.snapshots()
        after["staff"][4]["active"] = False
        changes = jy.compare(before, after)["changes"]
        self.assertEqual(
            changes,
            [{"staff_id": "S05", "field": "active", "before": True, "after": False}],
        )

    def test_changed_roster_target_recreated_account_rejected(self):
        before, after = self.snapshots()
        for field, value in [
            ("roster_sha256", "b" * 64),
            ("base", "http://localhost:8080"),
        ]:
            bad = copy.deepcopy(after)
            bad[field] = value
            with self.assertRaises(ValueError):
                jy.compare(before, bad)
        after["staff"][0]["id"] = 99
        with self.assertRaises(ValueError):
            jy.compare(before, after)

    def test_overlap_and_naive_timestamp_rejected(self):
        before, after = self.snapshots()
        for value in [before["finished_at"], "2026-01-01T01:00:00"]:
            bad = copy.deepcopy(after)
            bad["started_at"] = value
            with self.assertRaises(ValueError):
                jy.compare(before, bad)

    def test_hash_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "sample.json"
            jy.write_evidence(path, {"ok": True})
            self.assertEqual(jy.read_evidence(path), {"ok": True})
            with self.assertRaises(ValueError):
                jy.write_evidence(path, {"ok": False})
            path.write_text('{"ok": false}', encoding="utf-8")
            with self.assertRaises(ValueError):
                jy.read_evidence(path)

    def test_v1_snapshot_not_silently_converted(self):
        before, after = self.snapshots()
        before["schema"] = "v1"
        with self.assertRaises(ValueError):
            jy.compare(before, after)

    def test_non_hex_roster_digest_rejected(self):
        before, _ = self.snapshots()
        before["roster_sha256"] = "z" * 64
        with self.assertRaises(ValueError):
            jy.validate_snapshot(before)

    def test_bad_snapshot_shapes_rejected(self):
        before, _ = self.snapshots()
        for bad in [None, [], {**before, "staff": [None] * 6}]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                jy.validate_snapshot(bad)

    def test_unknown_schema_rejected(self):
        with self.assertRaises(ValueError):
            jy.validate_evidence({"schema": "unknown"})

    def test_diff_schema_and_values(self):
        before, after = self.snapshots()
        after["staff"][4]["active"] = False
        data = jy.compare(before, after)
        data.update(before_sha256="a" * 64, after_sha256="b" * 64)
        jy.validate_evidence(data)
        for changes in [
            data["changes"] * 2,
            [{"staff_id": "S05", "field": "active", "before": "true", "after": False}],
        ]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                jy.validate_diff({**data, "changes": changes})

    def test_cli_requires_explicit_hash_only(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "historical.json"
            jy.write_evidence(path, {"schema": "historical"})
            command = [
                sys.executable,
                str(Path(jy.__file__)),
                "verify",
                "--file",
                str(path),
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            result = subprocess.run(
                command + ["--hash-only"], capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("HASH ONLY", result.stdout)


if __name__ == "__main__":
    unittest.main()
