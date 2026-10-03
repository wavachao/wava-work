# Wava Work

[![Latest release](https://img.shields.io/github/v/release/wavachao/wava-work)](https://github.com/wavachao/wava-work/releases/latest)
[![Validation](https://github.com/wavachao/wava-work/actions/workflows/validate.yml/badge.svg)](https://github.com/wavachao/wava-work/actions/workflows/validate.yml)

面向 Codex、Claude Code 等 AI 编程助手的模块化个人工作技能，覆盖软件开发、界面设计、文档排版、数据可视化、演示文稿与视频制作。它将工作偏好、任务流程和技能接入规则拆分为独立模块，由任务入口按需加载，并通过可验证、可回退的维护流程持续改进。

## 功能与设计

| 能力 | 执行方式 |
| --- | --- |
| 任务规划 | 明确交付物与验收条件，在实施前给出与任务规模相符的计划 |
| 软件开发 | Python 项目使用 `uv`；其他语言沿用原生工具链；按工作量和依赖组织 subagent 与 Git worktree |
| 界面与视觉交付 | 同时检查功能、交互、排版与最终呈现，避免通用模板式输出 |
| 文档与媒体制作 | 优先使用平台专用技能和现有工具；文档、PPT 与视频执行相应渲染检查 |
| 技能组合 | 按用途选择技能，保持第三方技能独立，避免将全部指令写入入口 |
| 持续改进 | 将长期反馈和可复用经验转化为最小模块修改，验证后保存版本及回退依据 |

## 快速开始

### 环境要求

- Git、Python 3.10 或更高版本、Node.js 与 npm。
- 支持 Agent Skills 的客户端。安装工具采用 [Vercel Skills CLI](https://github.com/vercel-labs/skills)。
- LaTeX、字体及媒体工具按任务需要检查，不属于安装脚本自动配置的依赖。

### 推荐安装

稳定版与更新说明见 [GitHub Releases](https://github.com/wavachao/wava-work/releases/latest)。以下示例固定 Wava Work v0.4.3，默认安装到 Codex 用户目录，同时从 Ponytail 上游获取最新核心技能。

```bash
git clone --branch v0.4.3 --depth 1 https://github.com/wavachao/wava-work.git wava-work-v0.4.3
cd wava-work-v0.4.3
python scripts/install.py -y
```

安装到 Claude Code：

```bash
python scripts/install.py --agent claude-code -y
```

安装到当前项目，或先查看安装命令：

```bash
python scripts/install.py --project -y
python scripts/install.py --dry-run
```

安装入口读取 `skills.lock.json`，安装当前检出的技能集合，并单独处理 Ponytail 的版本策略。因此，后续加入技能无需修改安装命令。项目模式以运行命令时的当前目录为安装目标。

### 仅安装核心技能

无需克隆仓库时，可使用 Skills CLI 分别安装入口与最新 Ponytail：

```bash
npx skills add wavachao/wava-work --skill wava-work -g -a codex -y
npx skills add DietrichGebert/ponytail --skill ponytail -g -a codex -y
```

这两条命令只安装指定技能；完整技能集合请使用推荐安装入口。ChatGPT Work 使用平台自身的技能管理方式分别导入，CLI 命令不能替代平台安装。

## Ponytail 版本策略

默认策略为 **latest**：安装时由 Skills CLI 从 [Ponytail 官方仓库](https://github.com/DietrichGebert/ponytail) 的默认分支获取当前版本，仅选择核心 `ponytail` 技能。这里的“最新”指上游默认分支的当前内容，不限定为某个 Release 标签，也不表示安装后后台自动更新。

仓库保留经过来源校验的 Ponytail 快照，供显式复现安装使用：

```bash
python scripts/install.py --ponytail bundled -y
```

快照来源、提交和校验值分别记录于 `skills/ponytail/upstream.json` 与 `skills.lock.json`。这些记录描述仓库内容，不代表使用 latest 策略后客户端所安装的上游版本。客户端安装来源及更新信息由 Skills CLI 管理；latest 安装失败时脚本返回错误，不自动改用快照。

代码任务默认使用 Ponytail 的 `full` 模式；用户可指定 `lite` 或 `ultra`。Ponytail 的简化原则用于减少不必要的实现，不降低明确功能、界面质量或验证要求。上游辅助技能、hooks 与插件不在默认安装范围内。

## 使用

通过客户端支持的调用方式指定 `wava-work`，例如 Codex 中的 `$wava-work`。入口根据交付物选择所需模块，允许组合使用。

```text
使用 wava-work 开发一个图片批处理工具。
保留原始文件，使用 uv 管理 Python 项目，提供运行说明和样例验证。
```

```text
使用 wava-work 制作论文汇报 PPT。
图表应可复现，中文使用霞鹜文楷，并渲染检查全部页面。
```

默认排版偏好为：中文 **LXGW WenKai**，英文正文 **Libre Baskerville**，标题、界面与图表 **Inter**，代码 **JetBrains Mono**。具体任务模板和用户要求优先；字体可用性在实际制作前检查。

## 项目结构

| 路径 | 用途 |
| --- | --- |
| `skills/wava-work/SKILL.md` | 技能入口、任务路由与执行约束 |
| `skills/wava-work/references/` | 开发、UI、文档、图表、PPT、视频及维护模块 |
| `skills/wava-work/scripts/` | 环境探测、结构校验、清单管理与源码导出 |
| `skills/ponytail/` | 保留原始许可证和来源记录的第三方快照 |
| `scripts/install.py` | 技能集合安装与 Ponytail 版本选择 |
| `skills.lock.json` | 仓库技能清单、来源版本及文件完整性记录 |
| `releases/` | 稳定版本发布说明 |
| `tests/` | 脚本与技能包回归测试 |
| `evals/` | 行为评估场景及脱敏维护记录 |

## 扩展与维护

新增技能先核对实际说明、资源、依赖、许可证和规则冲突，再登记用途及触发条件。可分发的技能以独立目录纳入清单，补充路由与验证；仅在相关任务中加载。详细流程见 [技能包维护](skills/wava-work/references/bundle.md)。

每次交付前，入口轻量检查是否出现长期偏好、重复失败、流程缺口或新技能需求。有可核查依据时修改对应模块，执行相关验证并记录回退点；无新经验时直接交付。第一方规则可持续改进，第三方内容通过审核后的上游升级维护。详见 [进化流程](skills/wava-work/references/evolution.md)。

技能更新需要 agent 实际执行，并具备源码访问及保存权限。公开源码、客户端安装和平台技能保存是独立步骤；本项目不提供后台训练或跨设备自动更新服务。

查看 [最新 Release](https://github.com/wavachao/wava-work/releases/latest) 的版本和更新说明，再按目标 tag 检出源码并重新安装；完整安装入口会包含新增技能，并重新获取最新 Ponytail。固定 tag 的安装目录处于 detached HEAD，不使用 `git pull` 更新。

```bash
git fetch --tags origin
git switch --detach v0.4.3  # 换成目标 Release 的 tag
python scripts/install.py -y
```

`main` 用于持续开发。直接通过 Skills CLI 安装仓库入口会跟踪默认分支；需要稳定、可复现的 Wava Work 版本时使用上述 tag 安装方式。

## 稳定发布

VERSION、Git tag 与 Release 一致，例如 `0.4.3` / `v0.4.3` / `Wava Work v0.4.3`。发布说明存放于 `releases/`，说明变化、兼容性、验证范围和安装/回退方法。已发布 tag 和内容保持不变；修正使用新版本。

更新 VERSION、清单及发布说明并推送到 main 后，发布工作流执行校验，通过后创建附注 tag 和 GitHub Release；支持在 Actions 手动重跑。只有确认 Release 已公开且 tag 指向正确提交，才报告发布完成。默认最新 Ponytail 与固定 Wava Work 版本独立管理。

## 提交规范

本仓库及 Wava Work 创建的提交采用 [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)，提交信息严格为单行：

```text
feat(install): support project-scoped skill installation
fix(registry): reject conflicting skill names
docs(readme): clarify installation targets
```

使用小写类型和英文祈使句；范围可省略。提交不包含正文或 trailers；破坏性变更使用 `type(scope)!: description`，并在同一行说明影响。合并采用符合规范的 squash 提交信息。历史重写需明确授权，并使用带预期远端 SHA 的 `--force-with-lease`。

## 验证

在仓库根目录运行：

```bash
python skills/wava-work/scripts/validate_bundle.py skills/wava-work
python skills/wava-work/scripts/bundle_registry.py --repo . verify
python -m unittest discover -s tests -v
python scripts/check_commits.py
```

CI 执行结构、清单、脚本与导出检查。安装测试使用本地模拟，不等于已在所有客户端完成在线安装。`evals/cases.json` 定义行为评估场景与评分依据，不能视为已经通过的结果；成果质量和工作流效果需通过真实任务评估。

## 许可

本项目原创内容采用 [MIT License](LICENSE)。Ponytail 保留其原始 MIT 许可证，第三方说明见 [THIRD_PARTY.md](THIRD_PARTY.md)。字体、软件和用户素材遵循各自许可；本仓库不包含字体文件、认证信息或私有任务材料。
