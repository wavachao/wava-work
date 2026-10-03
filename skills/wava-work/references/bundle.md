# 可扩展技能包

## 来源与安装
- 公共源码：https://github.com/wavachao/wava-work 。维护前读取最新版本；使用已授权的GitHub连接或本地checkout，不假定安装目录就是源码仓库。
- 仓库skills.lock.json是包清单，skills/<name>是可独立安装的技能；清单记录role、when、来源、快照固定commit、许可证、文件校验值；可另记安装策略，快照锁定与客户端latest安装分开。
- 默认使用仓库统一安装入口：`python scripts/install.py -y`。读取当前清单安装技能集合，但排除Ponytail快照，另从官方上游默认分支安装当时最新的核心ponytail。
- 默认目标codex、用户范围；Claude Code加`--agent claude-code`，项目范围加`--project`。安装入口位于公开源码仓库，不假定已安装技能目录包含它。
- Ponytail的latest策略不固定上游commit；仓库清单的固定commit与哈希仅描述保留的快照。用户指定复现时用`--ponytail bundled`；不得用快照冒充最新或在失败后静默降级。
- 增加新技能后更新源码checkout并重新运行完整安装入口；普通update只更新已安装项，不能据此保证新增技能已安装。不要默认--all，它还会影响所有agent。
- 不把一次安装视为后台持续更新。核对客户端实际安装状态与来源；上游内容需要按正常技能接入流程阅读，不因latest策略扩大授权。
- ChatGPT Work按其技能管理方式分别安装。仓库修改不等于所有客户端已更新，不伪报本地安装状态。

## 新增技能流程
1. 用户提供链接或出现真实能力缺口时发现候选；不因发现新skill就全部纳入。
2. 读取实际SKILL.md和相关脚本/资源，确认适用任务、权限、依赖、许可证、与已有规则的冲突及是否值得增加。
3. 锁定上游完整commit，获取实际使用所需完整目录与原始许可证。保留相对资源路径，不仅拷贝SKILL.md。第三方内容保持独立，不自我改写。
4. 在公开仓库新增skills/<name>。同名不覆盖；新技能若需要重命名或平台适配，记录具体差异并验证。
5. 运行registry登记：
   `python skills/wava-work/scripts/bundle_registry.py --repo . register --name <name> --role <用途> --when <触发条件> --source-url <仓库URL> --source-ref <完整commit> --license <许可证>`
6. 补充相关接入说明与一个真实/独立工作流场景，避免所有技能默认加载。清单不是可执行授权；agent只读取与任务相关项的说明。
7. 核对来源真实性和许可证；registry只检查文件与登记的一致性，不证明上游可信或许可证允许再分发。
8. 更新本技能VERSION，在评估记录写脱敏证据与验证，刷新第一方校验值：
   `python skills/wava-work/scripts/bundle_registry.py --repo . refresh --name wava-work`
9. 跑verify、结构校验和相关测试，按已有授权保存/发布，确认远端与客户端状态。

## 更新与删除
- 第三方更新要比较固定版本间差异，审核后更新来源和哈希；不要盲目刷新第三方哈希来掩盖变更。
- 用户明确要求删除或长期无效时移除对应目录、清单和路由；保留Git回退记录。不要顺带卸载用户单独管理的技能。
- 新技能默认进入当前技能包安装集合；若是实验或外部不可再分发，则留本地候选/引用，不放入发布集合。
