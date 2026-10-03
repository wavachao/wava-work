import hashlib
import json
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/wava-work"
spec = importlib.util.spec_from_file_location("validator", SKILL / "scripts/validate_bundle.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class BundleTests(unittest.TestCase):
    def test_bundle(self):
        self.assertEqual(validator.validate(SKILL), [])
    def test_vendored_ponytail_integrity(self):
        pony = ROOT / "skills/ponytail"
        metadata = json.loads((pony / "upstream.json").read_text())
        self.assertEqual(metadata["commit"], "c982cd411abb53323c4baa1baa3c2f020b8d0b08")
        self.assertFalse(metadata["modified"])
        self.assertIn("name: ponytail", (pony / "SKILL.md").read_text())
        for name, checksum in metadata["sha256"].items():
            self.assertEqual(hashlib.sha256((pony / name).read_bytes()).hexdigest(), checksum)
        self.assertIn("Copyright (c) 2026 DietrichGebert", (pony / "LICENSE").read_text())
    def test_export_contains_both_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "export"
            result = subprocess.run([sys.executable, str(SKILL / "scripts/export_repository.py"),
                "--skill-root", str(SKILL), "--destination", str(destination)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            for name in ("wava-work", "ponytail"):
                self.assertTrue((destination / "skills" / name / "SKILL.md").is_file())
            self.assertTrue((destination / "skills/ponytail/LICENSE").is_file())
    def test_missing_module_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "skill"
            shutil.copytree(SKILL, copy)
            (copy / "references/ui.md").unlink()
            self.assertTrue(any("ui.md" in error for error in validator.validate(copy)))
    def test_export_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(SKILL / "scripts/export_repository.py"),
                "--skill-root", str(SKILL), "--destination", tmp], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
    def test_probe_requires_scope(self):
        result = subprocess.run([sys.executable, str(SKILL / "scripts/probe_environment.py")], capture_output=True)
        self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__":
    unittest.main()
