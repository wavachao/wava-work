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
