#!/usr/bin/env python3
"""Deterministic tests for the OpenCode Studio search CLI."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ARTIFACT_DIR = Path(__file__).resolve().parent
SEARCH_SOURCE = ARTIFACT_DIR / "search.py"


class SearchCliTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="opencode-studio-test-"))
        self.artifact_dir = self.temp_dir / "artifact"
        self.artifact_dir.mkdir()
        self.script = self.artifact_dir / "search.py"
        shutil.copyfile(SEARCH_SOURCE, self.script)
        self.knowledge_base = self.artifact_dir / "knowledge_base"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def make_knowledge_base(self):
        self.knowledge_base.mkdir()

    def write_text(self, relative_path, content):
        path = self.knowledge_base / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def write_bytes(self, relative_path, content):
        path = self.knowledge_base / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def run_cli(self, *arguments, cwd=None):
        return subprocess.run(
            [sys.executable, str(self.script), *arguments],
            capture_output=True,
            encoding="utf-8",
            cwd=str(cwd) if cwd is not None else str(self.temp_dir),
        )

    def parse_stdout(self, completed):
        return json.loads(completed.stdout)

    def test_happy_path_is_deterministic(self):
        self.make_knowledge_base()
        self.write_text("notes.txt", "installation installation guide")
        self.write_text("other.txt", "installation")
        self.write_text("empty.txt", "nothing relevant")

        first = self.run_cli("installation")
        second = self.run_cli("installation")

        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.returncode, second.returncode)
        self.assertEqual(first.stderr, "")
        self.assertTrue(first.stdout.endswith("\n"))
        self.assertEqual(first.stdout.count("\n"), 1)
        self.assertEqual(
            self.parse_stdout(first),
            [
                {"title": "notes", "score": 1.0, "source": "notes.txt"},
                {"title": "other", "score": 0.5, "source": "other.txt"},
            ],
        )

    def test_case_insensitive_queries_match(self):
        self.make_knowledge_base()
        self.write_text("a.txt", "Alpha BETA alpha beta ALPHA")

        lower = self.run_cli("alpha")
        upper = self.run_cli("ALPHA")

        self.assertEqual(lower.returncode, 0)
        self.assertEqual(lower.stdout, upper.stdout)
        self.assertEqual(
            self.parse_stdout(lower),
            [{"title": "a", "score": 1.0, "source": "a.txt"}],
        )

    def test_non_overlapping_count_and_rounding(self):
        self.make_knowledge_base()
        self.write_text("many.txt", "aa aa aa")
        self.write_text("one.txt", "aa")

        completed = self.run_cli("aa")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(
            self.parse_stdout(completed),
            [
                {"title": "many", "score": 1.0, "source": "many.txt"},
                {"title": "one", "score": 0.3333, "source": "one.txt"},
            ],
        )

    def test_ties_break_by_source_and_limit_applies(self):
        self.make_knowledge_base()
        for name in ("b.txt", "a.txt", "c.txt"):
            self.write_text(name, "needle")

        completed = self.run_cli("needle")
        self.assertEqual(
            self.parse_stdout(completed),
            [
                {"title": "a", "score": 1.0, "source": "a.txt"},
                {"title": "b", "score": 1.0, "source": "b.txt"},
                {"title": "c", "score": 1.0, "source": "c.txt"},
            ],
        )

        limited = self.run_cli("needle", "--max-results", "2")
        self.assertEqual(
            [item["source"] for item in self.parse_stdout(limited)],
            ["a.txt", "b.txt"],
        )

        equals_form = self.run_cli("needle", "--max-results=1")
        self.assertEqual(
            [item["source"] for item in self.parse_stdout(equals_form)],
            ["a.txt"],
        )

    def test_default_limit_is_ten(self):
        self.make_knowledge_base()
        for number in range(12):
            self.write_text("file{:02d}.txt".format(number), "match")

        completed = self.run_cli("match")
        sources = [item["source"] for item in self.parse_stdout(completed)]
        self.assertEqual(len(sources), 10)
        self.assertEqual(
            sources, ["file{:02d}.txt".format(i) for i in range(10)]
        )

    def test_filtering_and_isolation(self):
        self.make_knowledge_base()
        self.write_text("keep.txt", "target")
        self.write_text("skip.md", "target")
        self.write_text("upper.TXT", "target")
        self.write_text("sub/nested.txt", "target")

        outside = self.temp_dir / "outside.txt"
        outside.write_text("target", encoding="utf-8")
        try:
            os.symlink(outside, self.knowledge_base / "link.txt")
        except (OSError, NotImplementedError):
            pass

        completed = self.run_cli("target")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(
            self.parse_stdout(completed),
            [{"title": "keep", "score": 1.0, "source": "keep.txt"}],
        )

    def test_double_dash_allows_dash_query(self):
        self.make_knowledge_base()
        self.write_text("dash.txt", "-needle appears here")

        completed = self.run_cli("--", "-needle")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(
            self.parse_stdout(completed),
            [{"title": "dash", "score": 1.0, "source": "dash.txt"}],
        )

    def test_utf8_output_is_not_ascii_escaped(self):
        self.make_knowledge_base()
        self.write_text("café.txt", "café café")

        completed = self.run_cli("café")
        self.assertEqual(completed.returncode, 0)
        self.assertIn("café", completed.stdout)
        self.assertEqual(
            self.parse_stdout(completed),
            [{"title": "café", "score": 1.0, "source": "café.txt"}],
        )

    def test_usage_errors_exit_two_with_empty_stdout(self):
        cases = [
            (),
            ("query", "extra"),
            ("--bogus", "query"),
            ("query", "--max-results", "0"),
            ("query", "--max-results", "-1"),
            ("query", "--max-results", "abc"),
            ("query", "--max-results"),
            ("query", "--max-results="),
            ("   ",),
            ("--max-results", "5"),
        ]
        for arguments in cases:
            with self.subTest(arguments=arguments):
                completed = self.run_cli(*arguments)
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(completed.stdout, "")
                self.assertNotEqual(completed.stderr, "")

    def test_missing_knowledge_base_is_exit_three_and_not_created(self):
        completed = self.run_cli("query")
        self.assertEqual(completed.returncode, 3)
        self.assertEqual(completed.stdout, "")
        self.assertNotEqual(completed.stderr, "")
        self.assertFalse(self.knowledge_base.exists())

    def test_knowledge_base_that_is_a_file_is_exit_three(self):
        self.knowledge_base.write_text("not a directory", encoding="utf-8")
        completed = self.run_cli("query")
        self.assertEqual(completed.returncode, 3)
        self.assertEqual(completed.stdout, "")

    def test_empty_knowledge_base_is_no_match(self):
        self.make_knowledge_base()
        completed = self.run_cli("query")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, "[]\n")

    def test_no_matches_is_exit_one(self):
        self.make_knowledge_base()
        self.write_text("a.txt", "hello")
        completed = self.run_cli("absent")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, "[]\n")
        self.assertEqual(completed.stderr, "")

    def test_undecodable_file_is_skipped_with_warning(self):
        self.make_knowledge_base()
        self.write_bytes("bad.txt", b"\xff\xfe\x00bad")
        self.write_text("good.txt", "target")

        completed = self.run_cli("target")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(
            self.parse_stdout(completed),
            [{"title": "good", "score": 1.0, "source": "good.txt"}],
        )
        self.assertIn("bad.txt", completed.stderr)

    @unittest.skipIf(
        hasattr(os, "geteuid") and os.geteuid() == 0,
        "root can read mode-000 files",
    )
    def test_unreadable_file_is_skipped_with_warning(self):
        self.make_knowledge_base()
        unreadable = self.write_text("locked.txt", "target")
        self.write_text("good.txt", "target")
        os.chmod(unreadable, 0)
        try:
            completed = self.run_cli("target")
        finally:
            os.chmod(unreadable, 0o600)

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(
            [item["source"] for item in self.parse_stdout(completed)],
            ["good.txt"],
        )
        self.assertIn("locked.txt", completed.stderr)


if __name__ == "__main__":
    unittest.main()
