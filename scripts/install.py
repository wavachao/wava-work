"""Install the skill bundle and upstream Ponytail through the Skills CLI."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def commands(repo, agent="codex", project=False, yes=False, ponytail="latest", npx="npx"):
    registry = json.loads((repo / "skills.lock.json").read_text(encoding="utf-8"))
    names = list(registry["skills"])
    if ponytail == "latest":
        names = [name for name in names if name != "ponytail"]
    options = ["-a", agent]
    if not project:
        options += ["-g"]
    if yes:
        options += ["-y"]
    result = []
    if names:
        # Local source keeps the reviewed checkout and its manifest in agreement.
        result.append([npx, "skills", "add", str(repo.resolve()), "--skill", *names, *options])
    if ponytail == "latest":
        policy = registry["skills"]["ponytail"]["installation"]
        result.append([npx, "skills", "add", policy["source"], "--skill", policy["skill"], *options])
    return result


def install(plan):
    for command in plan:
        subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", default="codex", help="Skills CLI agent name (default: codex)")
    parser.add_argument("--project", action="store_true", help="Install to the current project instead of globally")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip Skills CLI confirmation prompts")
    parser.add_argument("--ponytail", choices=("latest", "bundled"), default="latest",
                        help="Upstream default-branch head or repository snapshot (default: latest)")
    parser.add_argument("--dry-run", action="store_true", help="Print commands as JSON without installing")
    args = parser.parse_args()
    executable = "npx" if args.dry_run else shutil.which("npx")
    if not executable:
        parser.exit(1, "npx was not found; install Node.js and npm first.\n")
    plan = commands(ROOT, args.agent, args.project, args.yes, args.ponytail, executable)
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    try:
        install(plan)
    except (OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Installation failed: {exc}\nEarlier successful steps may remain installed; no snapshot fallback was attempted.\n")
    print("Installation completed. Ponytail source: " + args.ponytail)


if __name__ == "__main__":
    main()
