from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pack_only.py"
GIF = b"GIF89a" + (b"\x00" * 24)
PNG = b"\x89PNG\r\n\x1a\n" + (b"\x00" * 24)


class PackOnlyTests(unittest.TestCase):
    def run_script(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_validates_and_exactly_deduplicates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "input"
            source.mkdir()
            (source / "a.gif").write_bytes(GIF)
            (source / "b.gif").write_bytes(GIF)
            (source / "c.png").write_bytes(PNG)
            (source / "photo.jpg").write_bytes(b"\xff\xd8\xff" + b"photo")
            output = root / "stickers.zip"

            result = self.run_script("--input", str(source), "--output", str(output))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("packaged=2", result.stdout)
            self.assertIn("duplicates=1", result.stdout)
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(archive.namelist(), ["sticker-001.gif", "sticker-002.png"])

    def test_rejects_disguised_media(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "input"
            source.mkdir()
            (source / "fake.gif").write_text("not a gif", encoding="utf-8")
            output = root / "stickers.zip"

            result = self.run_script("--input", str(source), "--output", str(output))

            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid=1", result.stdout)
            self.assertFalse(output.exists())

    def test_requires_force_to_replace_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "input"
            source.mkdir()
            (source / "a.gif").write_bytes(GIF)
            output = root / "stickers.zip"

            first = self.run_script("--input", str(source), "--output", str(output))
            second = self.run_script("--input", str(source), "--output", str(output))
            forced = self.run_script(
                "--input", str(source), "--output", str(output), "--force"
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("output already exists", second.stderr)
            self.assertEqual(forced.returncode, 0, forced.stderr)


if __name__ == "__main__":
    unittest.main()
