"""Export a new public-source repository; never overwrite, install or push."""
import argparse
import json
import shutil
from pathlib import Path
from validate_bundle import validate
from bundle_registry import read_registry, verify

def export(skill, destination, ponytail=None, repo_root=None):
    errors = validate(skill)
    if errors:
        raise ValueError("Invalid bundle: " + "; ".join(errors))
    if destination.exists():
        raise FileExistsError("Destination exists; choose a new directory")
    if destination.resolve().is_relative_to(skill.resolve()):
        raise ValueError("Destination must not be inside the skill")
    repo_root = repo_root or skill.parent.parent
    errors = verify(repo_root)
    if errors:
        raise ValueError("Invalid registry: " + "; ".join(errors))
    data = read_registry(repo_root)
    destination.mkdir(parents=True)
    for name in data["skills"]:
        folder = repo_root / "skills" / name
        shutil.copytree(folder, destination / "skills" / name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    # Read current repository files rather than regenerating stale maintenance data.
    for name in ("README.md", "LICENSE", "THIRD_PARTY.md", "skills.lock.json", ".gitignore"):
        if (repo_root / name).is_file():
            shutil.copyfile(repo_root / name, destination / name)
    for name in ("tests", "evals", ".github"):
        if (repo_root / name).is_dir():
            shutil.copytree(repo_root / name, destination / name,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--ponytail-root", type=Path, help="Legacy argument; registry is authoritative")
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()
    try:
        export(args.skill_root, args.destination, args.ponytail_root, args.repo_root)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")
    print("Prepared public-source repository; not pushed or installed.")

if __name__ == "__main__":
    main()
