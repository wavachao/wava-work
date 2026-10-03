"""Read-only, task-specific capability checks. No installation or broad scanning."""
import argparse
import importlib.util
import json
import shutil

GROUPS = {
    "code": ("git", "uv", "python3"),
    "ui": ("node", "npm"),
    "documents": ("xelatex", "lualatex", "pdflatex", "latexmk", "pdftoppm", "libreoffice", "fc-match"),
    "charts": ("python3", "fc-match"),
    "slides": ("libreoffice", "pdftoppm", "node", "fc-match"),
    "video": ("ffmpeg", "ffprobe", "fc-match"),
}
MODULES = {"charts": ("matplotlib",), "documents": ("docx", "pypdf"), "slides": ("pptx",)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", action="append", required=True, choices=GROUPS)
    args = parser.parse_args()
    result = {}
    for group in dict.fromkeys(args.group):
        result[group] = {"executables": {name: bool(shutil.which(name)) for name in GROUPS[group]}}
        result[group]["python_modules_in_current_interpreter"] = {
            name: importlib.util.find_spec(name) is not None for name in MODULES.get(group, ())
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
