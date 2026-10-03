# Wava Work

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
