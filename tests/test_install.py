"""Offline tests for source selection and installer failure behavior."""
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_default_fetches_upstream_not_snapshot(self):
        plan = installer.commands(ROOT, yes=True)
        self.assertNotIn('ponytail', plan[0])
        self.assertEqual(plan[1][:6], ['npx', 'skills', 'add', 'DietrichGebert/ponytail', '--skill', 'ponytail'])
        self.assertNotIn('c982cd411abb53323c4baa1baa3c2f020b8d0b08', ' '.join(plan[1]))
        for command in plan:
            self.assertEqual(command[-4:], ['-a', 'codex', '-g', '-y'])

    def test_explicit_snapshot_uses_local_source(self):
        plan = installer.commands(ROOT, ponytail='bundled')
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0][3], str(ROOT.resolve()))
        self.assertIn('ponytail', plan[0])

    def test_project_scope_and_agent_apply_to_both_steps(self):
        for command in installer.commands(ROOT, agent='claude-code', project=True):
            self.assertNotIn('-g', command)
            self.assertNotIn('-y', command)
            self.assertEqual(command[-2:], ['-a', 'claude-code'])

    def test_new_skill_included_without_install_script_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            data = json.loads((ROOT / 'skills.lock.json').read_text())
            data['skills']['animation-fixture'] = {'kind': 'vendored'}
            (repo / 'skills.lock.json').write_text(json.dumps(data))
            self.assertIn('animation-fixture', installer.commands(repo)[0])

    def test_upstream_failure_does_not_fallback(self):
        plan = installer.commands(ROOT)
        with patch.object(installer.subprocess, 'run', side_effect=[None, subprocess.CalledProcessError(1, plan[1])]) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                installer.install(plan)
            self.assertEqual(run.call_count, 2)

    def test_bundle_failure_stops_before_upstream(self):
        plan = installer.commands(ROOT)
        with patch.object(installer.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, plan[0])) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                installer.install(plan)
            self.assertEqual(run.call_count, 1)

    def test_dry_run_executes_without_npx(self):
        with patch.object(installer.shutil, 'which', return_value=None), patch.object(installer, 'install') as run:
            with patch('sys.argv', ['install.py', '--dry-run']), patch('builtins.print'):
                installer.main()
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
