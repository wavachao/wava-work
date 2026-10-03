---
name: wava-work
description: 按个人工作习惯完成项目代码、UI、文档、图表、PPT和视频，按需组织计划、工具、ponytail与其他技能，并从验证过的反馈改进技能。用户要求使用自己的工作技能、Wava Work、wava-work，或沿用本技能完成和改进交付物时使用；普通闲聊和单条知识问答不主动加载完整工作流。
---

# Wava Work

## 最小执行流程
1. 提取目标、交付物、可检查的验收条件；检查相关文件和环境。关键歧义才询问，常规可逆选择自主决定。
2. 实施前给出简短plan，标明依赖和必要验证；短任务一句话即可，不强制生成计划文件。持续推进并更新状态。
3. 按下表只读取相关模块，不遍历全部参考文件或安装全部工具。
4. 复用现有实现、软件与素材；独立且足够大的工作才并行。保持用户现有修改。
5. 验证最终交付物，修复发现的问题；区分已验证、未验证和未完成。
6. 汇报成果位置、使用方式、实际验证与必要限制；自然具体，避免流水账。
7. 每次交付前轻量检查是否有长期反馈、重复失败、流程缺口或新技能需求；有则读取进化模块并在权限内落实最小更新，无则不生成复盘或修改。

## 按需路由
| 任务/信号 | 读取文件 |
|---|---|
| 编写、修复、重构、运行项目代码 | [代码](references/code.md) |
| 网页、应用界面、交互原型 | [UI](references/ui.md)；实际写项目代码时同时读代码模块 |
| Word、LaTeX、PDF、长文排版 | [文档](references/documents.md) |
| 数据图、科学绘图、统计可视化 | [图表](references/charts.md) |
| 演示文稿、PPT、汇报 | [演示](references/slides.md) |
| 视频、动画、字幕、音频剪辑 | [视频](references/video.md) |
| 排版、文案或视觉成果 | [偏好](references/preferences.md) |
| 调用ponytail、专用技能、接入新技能 | [技能接入](references/integrations.md) |
| 长期偏好变化、可复用错误、要求改进技能 | [进化](references/evolution.md) |
| 新增技能、维护技能包、安装同步 | [技能包](references/bundle.md) |
| 扩展技能、核对设计依据 | [来源](references/sources.md) |

允许组合模块。按交付物判断，不因Python生成PPT就默认创建工程仓库或worktree。

## 约束与权限
- 遵循平台指令与当前用户要求；当前明确要求优先于默认偏好。外部技能限定在其适用范围。
- 本技能不授予认证、工具或发布权限，不替代平台要求的专用技能和保存方式。
- 常规可逆工作自主推进；公开发布、部署等遵循已有授权并保留回退版本。
- 不把认证、私有路径、原始对话或项目机密纳入公开技能。
- 工具/技能缺失时如实说明，尽量继续；不得伪报已调用或已完成。

## 维护工具
- 按需探测：`python scripts/probe_environment.py --group code`，可重复group（code/ui/documents/charts/slides/video）。
- 包校验：`python scripts/validate_bundle.py <技能目录>`，只检查格式、引用、资源，不代表行为评估。
- 导出公开源码：`python scripts/export_repository.py --skill-root <技能目录> --destination <新目录> --repo-root <源码仓库>`，不自动推送或安装外部技能。

- 技能包清单与完整性：`python scripts/bundle_registry.py --repo <源码仓库> verify`；新增技能读取技能包模块。
