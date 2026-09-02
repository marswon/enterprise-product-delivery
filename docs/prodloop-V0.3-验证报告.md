# prodloop V0.3 与 codebase-audit V0.1 验证报告

验证日期：2026-09-02

## 本次目标

让 `prodloop` 对成熟已有项目执行显式、可验证的接管流程，同时提供一个不授权实施的轻量 `codebase-audit`，并让审计证据能够受控交接给后续产品交付。

## prodloop V0.3

- 项目上下文独立记录为 `greenfield` 或 `brownfield`；交付模式继续使用 `greenfield`、`feature`、`workflow-change`、`integration`、`migration` 和 `remediation`。
- 非 `greenfield` 模式默认进入 `brownfield`，也可以在初始化时显式指定上下文。
- brownfield 初始化会创建六项接管产物：真实系统基线、系统地图、行为契约、变更影响、回归范围和技术债边界。
- 六项产物初始为 `Status: pending`。G1 标记通过后，只要任一产物未标记 `Status: complete`，状态校验就失败。
- 状态 schema 升级为 V2；校验器继续接受 V1，避免破坏已有项目恢复。
- 先前的 `codebase-audit` 只能作为证据输入；必须核对仓库版本、范围、失败检查和时效，不能自动代替 G1。

## codebase-audit V0.1

- 默认只读，不授权修改产品文件、安装依赖、清理工作区、迁移数据、部署或实施修复。
- 通过拓扑、运行事实、关键路径、契约与变更面、风险与未知五个证据层完成审计。
- 每项重要结论标记为 `observed`、`documented`、`inferred`、`unknown` 或 `conflict`。
- 默认在对话中交付，不写仓库；只有用户明确要求持久化时才写 `CODEBASE_AUDIT.md` 或指定路径。
- 提供与 prodloop 六项 brownfield 接管产物的一一映射，但不扩大实施授权。

## 自动化验证

| 检查 | 结果 |
|---|---|
| Python 语法编译 | 通过 |
| Skill frontmatter 解析与名称匹配 | 2/2 通过 |
| OpenAI UI 元数据与调用名匹配 | 2/2 通过 |
| 新 brownfield 项目自动识别 | 通过 |
| greenfield 不创建接管产物 | 通过 |
| G1 拒绝 pending 接管产物 | 通过 |
| 六项接管产物 complete 后允许进入 S2 | 通过 |
| V1 状态继续通过校验 | 通过 |
| V0.1 旧目录继续自动识别 | 通过 |
| 新旧状态目录冲突时拒绝 | 通过 |
| 状态目录越出项目根时拒绝 | 通过 |
| `git diff --check` | 通过 |

prodloop 自动化行为测试共 8 项，全部通过。

## 证据边界

- `codebase-audit` 尚未在独立真实仓库完成前向行为测试；当前验证覆盖结构、路由、授权边界和交接协议，不冒充审计质量已被真实项目证明。
- prodloop brownfield 接管尚未在大型遗留系统验证分析覆盖率、时间成本和缺陷拦截率。
- `Status: complete` 是结构门禁，不会自动证明文档内容真实；最终仍依赖来源、命令输出、运行观察和独立检查。
- 官方 Codex `quick_validate.py` 在当前 Python 环境仍因缺少 `PyYAML` 无法运行；本次使用现有 YAML 解析器完成 frontmatter 与 UI 元数据检查，并保留该限制。
- Kimi Code 的格式与调用入口符合其官方 Skill 机制，但本轮未执行需要联网和写入 Kimi 会话目录的真实模型调用。

## 下一门禁

选择一个边界明确的成熟项目，先独立运行 `codebase-audit`，再将报告交给 `prodloop` 执行 brownfield S0-S2。检查重复调查量、遗漏契约、错误影响判断、人工干预次数和 G1 拦截效果，再决定 V0.4 的收敛方向。
