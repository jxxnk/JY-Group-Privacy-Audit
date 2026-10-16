"""Offline release regression tests; only isolated temporary repositories."""

import hashlib
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

import jy_closeout as jy


class CloseoutTests(unittest.TestCase):
    def repository(self, directory):
        root = Path(directory) / "repo"
        root.mkdir()
        self.git(root, "init")
        self.git(root, "config", "user.name", "Offline Check")
        self.git(root, "config", "user.email", "check@example.test")
        self.git(root, "config", "core.autocrlf", "false")
        (root / "docs").mkdir()
        (root / "README.md").write_bytes(b"[Guide](docs/guide.md)\n")
        (root / "docs/guide.md").write_bytes(b"Fictional fixture\n")
        (root / jy.LIST).write_bytes(
            b"README.md\ndocs/guide.md\ndocs/delivery-files.txt\n"
        )
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "fixture")
        self.git(root, "tag", "-a", "v-test", "-m", "fixture")
        self.git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
        return root

    def git(self, root, *args):
        return subprocess.run(
            ["git", "-C", str(root), *args], check=True, capture_output=True
        ).stdout

    def rewrite_zip(self, archive, files):
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for name, raw in files.items():
                z.writestr(name, raw)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        Path(str(archive) + ".sha256.txt").write_text(digest, encoding="ascii")

    def test_invalid_paths(self):
        for value in [
            "../a",
            "/a",
            "a\\b",
            ".env.example",
            "private-evidence/a",
            "a//b",
            "a/./b",
            "a:b",
            " a",
        ]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                jy.safe_path(value)

    def test_delivery_list_contract(self):
        jy.delivery_list(b"docs/delivery-files.txt\nREADME.md\n")
        for raw in [
            b"README.md\n",
            b"docs/delivery-files.txt\nREADME.md\nreadme.md\n",
            b"docs/delivery-files.txt\nBUILD_INFO.txt\n",
        ]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                jy.delivery_list(raw)

    def test_missing_local_link(self):
        with self.assertRaises(ValueError):
            jy.check_links({"README.md": b"[x](missing.md)"})

    def test_nested_link_and_external_link(self):
        jy.check_links(
            {
                "README.md": b"[x](docs/a.md) [web](https://example.test)",
                "docs/a.md": b"[home](../README.md#title)",
            }
        )

    def test_pack_uses_blob_bytes_with_crlf_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.repository(d)
            self.git(root, "config", "core.autocrlf", "true")
            checkout = Path(d) / "checkout"
            self.git(root, "worktree", "add", "--detach", str(checkout), "HEAD")
            self.assertIn(b"\r\n", (checkout / "README.md").read_bytes())
            out = Path(d) / "release"
            jy.pack(checkout, "v-test", out)
            self.assertEqual(
                (out / "files/README.md").read_bytes(), b"[Guide](docs/guide.md)\n"
            )
            jy.verify(
                out / "JY-Final-v-test.zip",
                out / "JY-Final-v-test.zip.sha256.txt",
                Path(d) / "download",
            )

    def test_annotated_tag_required(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.repository(d)
            self.git(root, "tag", "light")
            with self.assertRaises(ValueError):
                jy.pack(root, "light", Path(d) / "release")

    def test_existing_output_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.repository(d)
            out = Path(d) / "release"
            out.mkdir()
            with self.assertRaises(FileExistsError):
                jy.pack(root, "v-test", out)

    def test_zip_digest_rejects_changed_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.repository(d)
            out = Path(d) / "release"
            jy.pack(root, "v-test", out)
            archive = out / "JY-Final-v-test.zip"
            archive.write_bytes(archive.read_bytes() + b"changed")
            with self.assertRaises(ValueError):
                jy.verify(archive, Path(str(archive) + ".sha256.txt"), None)

    def test_extra_file_rejected_even_with_matching_zip_digest(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.repository(d)
            out = Path(d) / "release"
            jy.pack(root, "v-test", out)
            archive = out / "JY-Final-v-test.zip"
            with zipfile.ZipFile(archive) as z:
                files = {n: z.read(n) for n in z.namelist()}
            files["unexpected.txt"] = b"unexpected"
            self.rewrite_zip(archive, files)
            with self.assertRaises(ValueError):
                jy.verify(archive, Path(str(archive) + ".sha256.txt"), None)

    def test_file_digest_rejects_modified_payload(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.repository(d)
            out = Path(d) / "release"
            jy.pack(root, "v-test", out)
            archive = out / "JY-Final-v-test.zip"
            with zipfile.ZipFile(archive) as z:
                files = {n: z.read(n) for n in z.namelist()}
            files["docs/guide.md"] = b"modified"
            self.rewrite_zip(archive, files)
            with self.assertRaises(ValueError):
                jy.verify(archive, Path(str(archive) + ".sha256.txt"), None)


if __name__ == "__main__":
    unittest.main()
