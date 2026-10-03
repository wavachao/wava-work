"""Validate Wava Work's structure, links and Python syntax; not agent behavior."""
import argparse
import ast
import json
import re
from pathlib import Path

def validate(root):
    root = root.resolve()
    errors = []
    entry = root / "SKILL.md"
    if not entry.is_file():
        return ["Missing SKILL.md"]
    source = entry.read_text(encoding="utf-8")
    header = re.match(r"\A---\n(.*?)\n---\n", source, re.S)
    if not header:
        errors.append("Missing frontmatter")
    else:
        fields = dict(re.findall(r"^([a-z_]+):\s*(.+)$", header[1], re.M))
        if fields.get("name") != "wava-work" or not fields.get("description"):
            errors.append("Invalid name or description")
        if len(fields.get("description", "")) > 1024:
            errors.append("Description exceeds 1024 characters")
    if len(source.splitlines()) > 100:
        errors.append("Entry exceeds the project's 100-line budget")
    linked = set()
    for file in root.rglob("*.md"):
        content = file.read_text(encoding="utf-8")
        if "[TODO:" in content:
            errors.append(f"Unfinished template: {file.relative_to(root)}")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in target or target.startswith("#"):
                continue
            path = (file.parent / target.split("#", 1)[0]).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                errors.append(f"Missing or escaping reference: {target}")
            if file == entry:
                linked.add(path)
    for file in (root / "references").glob("*.md"):
        if file.resolve() not in linked:
            errors.append(f"Unrouted module: {file.name}")
    for file in (root / "scripts").glob("*.py"):
        try:
            ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
        except SyntaxError as exc:
            errors.append(str(exc))
    version = root / "VERSION"
    if not version.is_file() or not re.fullmatch(r"\d+\.\d+\.\d+\n?", version.read_text()):
        errors.append("Invalid VERSION")
    if not (root / "agents/openai.yaml").is_file():
        errors.append("Missing UI metadata")
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    errors = validate(args.root)
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))

if __name__ == "__main__":
    main()
