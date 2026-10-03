"""Export a new public-source repository; never overwrite, install or push."""
import argparse
import json
import shutil
from pathlib import Path
from validate_bundle import validate

README = '''# Wava Work

个人工作技能：按需完成代码、UI、文档、图表、PPT和视频，并从验证过的经验改进。

## 使用
把 `skills/wava-work` 安装到你的 agent 平台支持的个人技能位置，再使用该平台的技能调用方式，例如 `$wava-work`。各平台的发现、安装和工具权限不同；本仓库不提供自动跨平台安装。

示例：使用 wava-work 做一个图片批处理工具，保留原文件，提供运行方法与样例验证。
示例：使用 wava-work 做论文汇报PPT，中文霞鹜文楷，图表可复现，渲染全部页面检查。

入口只路由相关模块，不每次加载所有规则。Python工程用uv；其他语言沿用工具链。写代码按收益使用subagent/worktree，非工程成果不强制工程流程。

## Ponytail及外部技能
可选接入 https://github.com/DietrichGebert/ponytail ，不包含其源码，也不自动安装。代码任务默认使用可用的full模式；品质和明确需求优先。真实安装时记录commit/tag；本包仅核对上游入口，不把日期当固定版本。
文档、PDF、PPT等优先平台已有专用技能。登记外部技能不授予认证、工具或权限。

## 本地环境
LaTeX和字体是个人环境预期，实际使用必须检查。路径、认证、账号、私有材料和原始任务日志不进入公开仓库；环境配置留本地。
字体：中文LXGW WenKai、英文正文Libre Baskerville、标题/界面/图表Inter、代码JetBrains Mono。指定模板优先。

## 维护与验证
`python skills/wava-work/scripts/validate_bundle.py skills/wava-work`
`python skills/wava-work/scripts/probe_environment.py --group code`

进化流程：反馈/失败证据 → 最小模块修改 → 对应和相邻场景验证 → 保存版本 → 可回退发布。任务完成后无新经验则不修改。技能不具备后台自运行、自动训练或自动同步能力。

CI仅验证结构、脚本与导出，不证明agent行为或审美改善。`evals/cases.json`是行为场景与评分依据，不是已经通过的结果。按需用真实agent执行并保存脱敏结果；更新权限/依赖/路由时扩大评估。
main保持验证版，维护走分支/PR；未经授权不自动合并或推送。查看 `skills/wava-work/references/sources.md` 获得一手设计依据。

## 发布与许可
版本见 `skills/wava-work/VERSION`。本仓库原创内容使用MIT许可证；第三方技能与字体遵循各自许可证。公开前确认脱敏、Git身份、仓库所属账号及所有测试结果。
'''
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
TESTS = '''import importlib.util
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
'''

def export(skill, destination):
    errors = validate(skill)
    if errors:
        raise ValueError("Invalid bundle: " + "; ".join(errors))
    if destination.exists():
        raise FileExistsError("Destination exists; choose a new directory")
    if destination.resolve().is_relative_to(skill.resolve()):
        raise ValueError("Destination must not be inside the skill")
    destination.mkdir(parents=True)
    shutil.copytree(skill, destination / "skills/wava-work", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    files = {"README.md": README, "LICENSE": LICENSE,
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
    args = parser.parse_args()
    try:
        export(args.skill_root, args.destination)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")
    print("Prepared public-source repository; not pushed or installed.")

if __name__ == "__main__":
    main()
