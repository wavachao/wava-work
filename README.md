# Wava Work

个人工作技能：按需完成代码、UI、文档、图表、PPT和视频，并从验证过的经验改进。

## 使用
本仓库包含两个独立技能：`wava-work`（入口和任务模块）与 `ponytail`（代码极简实现）。安装技能包时一起安装两者，使用时按需加载。

需要 Node.js/npm，使用 Vercel Skills CLI：

```bash
# 安装两个技能，交互选择目标 agent
npx skills add wavachao/wava-work --skill wava-work --skill ponytail -g

# 安装到 Codex，跳过确认
npx skills add wavachao/wava-work --skill wava-work --skill ponytail -g -a codex -y

# 安装到 Claude Code
npx skills add wavachao/wava-work --skill wava-work --skill ponytail -g -a claude-code -y

# 仅列出技能
npx skills add wavachao/wava-work --list
```

随后使用 `$wava-work` 或平台支持的调用方式。CLI官方说明：https://github.com/vercel-labs/skills 。普通单技能安装不自动解析依赖；ChatGPT Work需通过其技能管理方式分别导入两个技能，不能直接执行此命令替代平台安装。

示例：使用 wava-work 做一个图片批处理工具，保留原文件，提供运行方法与样例验证。
示例：使用 wava-work 做论文汇报PPT，中文霞鹜文楷，图表可复现，渲染全部页面检查。

入口只路由相关模块，不每次加载所有规则。Python工程用uv；其他语言沿用工具链。写代码按收益使用subagent/worktree，非工程成果不强制工程流程。

## Ponytail及外部技能
已附带 https://github.com/DietrichGebert/ponytail 的核心技能原始源码与MIT许可证，固定上游commit见 `skills/ponytail/upstream.json`。上述命令一次安装两个技能；代码任务默认full，品质与明确需求优先。未附带上游其他辅助技能或hooks，见THIRD_PARTY.md。
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
