# prodloop V0.2 验证报告

验证日期：2026-09-02

## 本次目标

让同一份 `prodloop` Skill 可由 Codex 和 Kimi Code 使用，同时避免脚本错误地从产品仓库解析 Skill 资源，并保持 V0.1 项目可恢复。

## 已完成

- `SKILL.md` 明确要求从已加载的 Skill 目录解析 `references/` 和 `scripts/`，不依赖产品仓库当前目录。
- 新项目状态目录改为工具中立的 `.prodloop/`。
- `validate_state.py` 与 `check_traceability.py` 会自动识别 V0.1 `.codex/delivery/`。
- `.prodloop/` 和 `.codex/delivery/` 同时存在时拒绝静默选择。
- 三个脚本都支持显式 `--state-dir`，且拒绝把状态写到项目根目录之外。
- README 提供 Codex、Kimi Code 以及 `~/.agents/skills/` 双端共享安装方式。
- Codex 调用保持 `$prodloop`；Kimi Code 调用为 `/skill:prodloop`。

## 自动化验证

| 检查 | 结果 |
|---|---|
| Python 语法编译 | 通过 |
| 新项目创建 `.prodloop/` | 通过 |
| 新状态自动发现与校验 | 通过 |
| V0.1 旧状态自动发现与校验 | 通过 |
| 新旧状态并存时拒绝校验 | 通过 |
| 已有旧状态时拒绝重复初始化 | 通过 |
| 状态目录越出项目根时拒绝初始化 | 通过 |
| `git diff --check` | 通过 |

回归测试共 5 项，全部通过，测试文件为 `tests/test_prodloop_scripts.py`。

## Kimi Code 兼容证据

- 本机 Kimi Code 版本为 `0.39.1`。
- 本机 `kimi --help` 明确提供 `--skills-dir <dir>`。
- Kimi Code 官方文档规定目录型 Skill 使用 `<name>/SKILL.md`，要求 `name` 与 `description`；当前 Skill 满足该格式。
- 官方调用语法为 `/skill:<name>`，因此本 Skill 的调用为 `/skill:prodloop`。
- 官方扫描目录包含 `~/.agents/skills/`，可与 Codex 共用一份安装。

## 未完成与证据边界

- 本轮 Kimi 真实模型调用因执行环境不允许写入 `~/.kimi-code` 并联网而未完成；当前结论证明格式与加载入口兼容，不冒充完整端到端执行验证。
- 官方 Codex `quick_validate.py` 在当前 Python 环境因缺少 `PyYAML` 无法启动；已保留失败事实，并使用脚本编译、引用检查、frontmatter 解析和行为测试覆盖结构与运行风险。
- 尚未完成新产品、已有系统功能、企业流程或集成三个真实仓库前向测试。
- 尚未证明在任一运行时都能不经人工裁决完成所有 Q2/Q3 产品；权限、业务歧义和高风险操作仍会按设计暂停。

## 下一门禁

在一个边界可控的真实已有系统功能上分别由 Codex 与 Kimi Code 执行 S0-S8，比较门禁结果、人工干预次数、恢复能力、最终体验和缺陷拦截率，再决定是否发布 V0.3。
