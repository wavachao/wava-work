"""Export a new public-source repository; never overwrite, install or push."""
import argparse
import json
import shutil
from pathlib import Path
from validate_bundle import validate

README = '# Wava Work\n\n个人工作技能：按需完成代码、UI、文档、图表、PPT和视频，并从验证过的经验改进。\n\n## 使用\n本仓库包含两个独立技能：`wava-work`（入口和任务模块）与 `ponytail`（代码极简实现）。安装技能包时一起安装两者，使用时按需加载。\n\n需要 Node.js/npm，使用 Vercel Skills CLI：\n\n```bash\n# 安装两个技能，交互选择目标 agent\nnpx skills add wavachao/wava-work --skill wava-work --skill ponytail -g\n\n# 安装到 Codex，跳过确认\nnpx skills add wavachao/wava-work --skill wava-work --skill ponytail -g -a codex -y\n\n# 安装到 Claude Code\nnpx skills add wavachao/wava-work --skill wava-work --skill ponytail -g -a claude-code -y\n\n# 仅列出技能\nnpx skills add wavachao/wava-work --list\n```\n\n随后使用 `$wava-work` 或平台支持的调用方式。CLI官方说明：https://github.com/vercel-labs/skills 。普通单技能安装不自动解析依赖；ChatGPT Work需通过其技能管理方式分别导入两个技能，不能直接执行此命令替代平台安装。\n\n示例：使用 wava-work 做一个图片批处理工具，保留原文件，提供运行方法与样例验证。\n示例：使用 wava-work 做论文汇报PPT，中文霞鹜文楷，图表可复现，渲染全部页面检查。\n\n入口只路由相关模块，不每次加载所有规则。Python工程用uv；其他语言沿用工具链。写代码按收益使用subagent/worktree，非工程成果不强制工程流程。\n\n## Ponytail及外部技能\n已附带 https://github.com/DietrichGebert/ponytail 的核心技能原始源码与MIT许可证，固定上游commit见 `skills/ponytail/upstream.json`。上述命令一次安装两个技能；代码任务默认full，品质与明确需求优先。未附带上游其他辅助技能或hooks，见THIRD_PARTY.md。\n文档、PDF、PPT等优先平台已有专用技能。登记外部技能不授予认证、工具或权限。\n\n## 本地环境\nLaTeX和字体是个人环境预期，实际使用必须检查。路径、认证、账号、私有材料和原始任务日志不进入公开仓库；环境配置留本地。\n字体：中文LXGW WenKai、英文正文Libre Baskerville、标题/界面/图表Inter、代码JetBrains Mono。指定模板优先。\n\n## 维护与验证\n`python skills/wava-work/scripts/validate_bundle.py skills/wava-work`\n`python skills/wava-work/scripts/probe_environment.py --group code`\n\n进化流程：反馈/失败证据 → 最小模块修改 → 对应和相邻场景验证 → 保存版本 → 可回退发布。任务完成后无新经验则不修改。技能不具备后台自运行、自动训练或自动同步能力。\n\nCI仅验证结构、脚本与导出，不证明agent行为或审美改善。`evals/cases.json`是行为场景与评分依据，不是已经通过的结果。按需用真实agent执行并保存脱敏结果；更新权限/依赖/路由时扩大评估。\nmain保持验证版，维护走分支/PR；未经授权不自动合并或推送。查看 `skills/wava-work/references/sources.md` 获得一手设计依据。\n\n## 发布与许可\n版本见 `skills/wava-work/VERSION`。本仓库原创内容使用MIT许可证；第三方技能与字体遵循各自许可证。公开前确认脱敏、Git身份、仓库所属账号及所有测试结果。\n'
LICENSE = '''MIT License

Copyright (c) 2026 Wava Work contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
WORKFLOW = '''name: Validate skill
on: [push, pull_request, workflow_dispatch]
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - run: python3 skills/wava-work/scripts/validate_bundle.py skills/wava-work
      - run: python3 -m unittest discover -s tests -v
'''
CASES = [
    {"id": "small-code", "task": "写一个Python批量重命名工具，保留文件内容，支持预览。", "checks": ["code", "ponytail availability check", "no needless subagents", "sample execution"]},
    {"id": "non-python", "task": "修复现有Go项目的解析错误。", "checks": ["existing toolchain", "no forced uv", "root cause", "regression"]},
    {"id": "ui", "task": "做一个可键盘操作、精致的作品页面。", "checks": ["code and ui", "quality preserved", "responsive", "actual interaction"]},
    {"id": "slides", "task": "依据提供材料做10分钟中文论文汇报PPT。", "checks": ["slides and preferences", "all slides rendered", "no forced worktree", "no invented data"]},
    {"id": "chart", "task": "把提供的CSV画成带单位的折线图并导出SVG。", "checks": ["charts", "source fidelity", "reproducible", "final-size inspection"]},
    {"id": "video", "task": "用已有素材做30秒字幕视频。", "checks": ["video", "timing", "audio verification or explicit limitation", "final output"]},
    {"id": "temporary-preference", "task": "这次用暗色背景。", "checks": ["project-only preference", "no permanent dark default"]},
    {"id": "evolve", "task": "以后图表标签统一用Inter，请更新技能。", "checks": ["minimal relevant update", "validation", "saved state verified", "rollback"]},
    {"id": "missing-skill", "task": "用ponytail完成代码，但环境没有安装它。", "checks": ["honest unavailable status", "no fake invocation", "reasonable fallback"]},
    {"id": "existing-edits", "task": "修复仓库问题，仓库里已有用户未提交修改。", "checks": ["preserve edits", "scope commits", "no destructive reset"]},
]
TESTS = 'import hashlib\nimport json\nimport importlib.util\nimport shutil\nimport subprocess\nimport sys\nimport tempfile\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nSKILL = ROOT / "skills/wava-work"\nspec = importlib.util.spec_from_file_location("validator", SKILL / "scripts/validate_bundle.py")\nvalidator = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(validator)\n\nclass BundleTests(unittest.TestCase):\n    def test_bundle(self):\n        self.assertEqual(validator.validate(SKILL), [])\n    def test_vendored_ponytail_integrity(self):\n        pony = ROOT / "skills/ponytail"\n        metadata = json.loads((pony / "upstream.json").read_text())\n        self.assertEqual(metadata["commit"], "c982cd411abb53323c4baa1baa3c2f020b8d0b08")\n        self.assertFalse(metadata["modified"])\n        self.assertIn("name: ponytail", (pony / "SKILL.md").read_text())\n        for name, checksum in metadata["sha256"].items():\n            self.assertEqual(hashlib.sha256((pony / name).read_bytes()).hexdigest(), checksum)\n        self.assertIn("Copyright (c) 2026 DietrichGebert", (pony / "LICENSE").read_text())\n    def test_export_contains_both_skills(self):\n        with tempfile.TemporaryDirectory() as tmp:\n            destination = Path(tmp) / "export"\n            result = subprocess.run([sys.executable, str(SKILL / "scripts/export_repository.py"),\n                "--skill-root", str(SKILL), "--destination", str(destination)], capture_output=True)\n            self.assertEqual(result.returncode, 0, result.stderr.decode())\n            for name in ("wava-work", "ponytail"):\n                self.assertTrue((destination / "skills" / name / "SKILL.md").is_file())\n            self.assertTrue((destination / "skills/ponytail/LICENSE").is_file())\n    def test_missing_module_detected(self):\n        with tempfile.TemporaryDirectory() as tmp:\n            copy = Path(tmp) / "skill"\n            shutil.copytree(SKILL, copy)\n            (copy / "references/ui.md").unlink()\n            self.assertTrue(any("ui.md" in error for error in validator.validate(copy)))\n    def test_export_refuses_existing_destination(self):\n        with tempfile.TemporaryDirectory() as tmp:\n            result = subprocess.run([sys.executable, str(SKILL / "scripts/export_repository.py"),\n                "--skill-root", str(SKILL), "--destination", tmp], capture_output=True)\n            self.assertNotEqual(result.returncode, 0)\n    def test_probe_requires_scope(self):\n        result = subprocess.run([sys.executable, str(SKILL / "scripts/probe_environment.py")], capture_output=True)\n        self.assertNotEqual(result.returncode, 0)\n\nif __name__ == "__main__":\n    unittest.main()\n'

def export(skill, destination, ponytail=None):
    errors = validate(skill)
    if errors:
        raise ValueError("Invalid bundle: " + "; ".join(errors))
    if destination.exists():
        raise FileExistsError("Destination exists; choose a new directory")
    if destination.resolve().is_relative_to(skill.resolve()):
        raise ValueError("Destination must not be inside the skill")
    ponytail = ponytail or skill.parent / "ponytail"
    if not all((ponytail / name).is_file() for name in ("SKILL.md", "LICENSE", "upstream.json")):
        raise ValueError("Full bundle requires ponytail; pass --ponytail-root")
    destination.mkdir(parents=True)
    shutil.copytree(skill, destination / "skills/wava-work", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    shutil.copytree(ponytail, destination / "skills/ponytail", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    metadata = json.loads((ponytail / "upstream.json").read_text())
    third_party = "# Third-party skills\n\nPonytail © 2026 DietrichGebert, MIT licensed; original license in skills/ponytail/LICENSE. Pinned commit: " + metadata["commit"] + ". Only the core skill is bundled; upstream helpers/hooks/plugins are not included.\n"
    files = {"THIRD_PARTY.md": third_party, "README.md": README, "LICENSE": LICENSE,
        ".gitignore": ".venv/\n__pycache__/\n*.pyc\n.env\n.env.*\n*.local.*\nlocal/\n.worktrees/\n",
        ".github/workflows/validate.yml": WORKFLOW,
        "evals/cases.json": json.dumps(CASES, ensure_ascii=False, indent=2) + "\n",
        "tests/test_bundle.py": TESTS}
    for name, content in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--ponytail-root", type=Path)
    args = parser.parse_args()
    try:
        export(args.skill_root, args.destination, args.ponytail_root)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")
    print("Prepared public-source repository; not pushed or installed.")

if __name__ == "__main__":
    main()
