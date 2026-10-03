"""Exercise the commit gate against actual temporary Git commit objects."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_commits.py'


class CommitChecks(unittest.TestCase):
    def test_real_history_accepts_single_lines_and_rejects_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            def git(*args):
                return subprocess.run(['git', *args], cwd=repo, check=True, capture_output=True, text=True)
            git('init')
            git('config', 'user.name', 'Commit Test')
            git('config', 'user.email', 'test@example.invalid')
            git('commit', '--allow-empty', '-m', 'chore: initialize test repository')
            git('commit', '--allow-empty', '-m', 'feat(api)!: remove legacy response field')
            run = subprocess.run([sys.executable, str(SCRIPT)], cwd=repo, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr.decode())
            git('commit', '--allow-empty', '-m', 'docs: update usage', '-m', 'Forbidden body')
            bad = git('rev-parse', 'HEAD').stdout.strip()
            run = subprocess.run([sys.executable, str(SCRIPT)], cwd=repo, capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn(bad, run.stdout.decode())
            git('commit', '--amend', '--allow-empty', '-m', 'Update usage')
            run = subprocess.run([sys.executable, str(SCRIPT), '--ref', 'HEAD^..HEAD'], cwd=repo, capture_output=True)
            self.assertNotEqual(run.returncode, 0)


if __name__ == '__main__':
    unittest.main()
