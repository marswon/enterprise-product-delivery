# enterprise-product-delivery

面向 Codex / Kimi Code 的两项配套能力：`prodloop` 负责企业级软件产品端到端交付，`codebase-audit` 负责对已有代码库进行轻量、只读、证据化的接管审计。`prodloop V0.6` 已内置企业业务 UI、数据可视化、上下文预算和项目级持久记忆。

## Skills

- `prodloop`：从调查分析、产品定义、产品与 UX 设计、技术设计开始，持续进入开发、独立验收、发布准备和结果复盘。
- `codebase-audit`：还原已有系统架构、真实运行基线、行为契约、变更影响和关键风险，不实施修复。

## 适用场景

- 从零开发软件产品；
- 为已有系统增加完整功能；
- 改造企业业务流程；
- 系统集成和数据迁移；
- 对缺陷或质量问题进行系统治理。

不适用于只有几行改动且规格已经完整的小修复，也不应用于只要求建议、评审或解释而未授权实施的任务。

## 推荐：Codex 与 Kimi 共用安装

两者都会扫描 `~/.agents/skills/`。已安装 Codex 的电脑可直接运行：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo marswon/enterprise-product-delivery \
  --path skills/prodloop skills/codebase-audit \
  --dest ~/.agents/skills \
  --method git
```

仓库是公开仓库，无需 GitHub 登录即可安装。安装器发现目标目录已存在时会停止，不会覆盖旧版本。安装或更新后请新建任务或重启客户端。

## 分别安装

### 只给 Codex 使用

网页下载仓库 ZIP 后，将需要的 Skill 目录复制为：

```text
~/.codex/skills/prodloop/SKILL.md
~/.codex/skills/codebase-audit/SKILL.md
```

也可以通过 GitHub 安装：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo marswon/enterprise-product-delivery \
  --path skills/prodloop skills/codebase-audit \
  --method git
```

### 只给 Kimi Code 使用

Kimi Code 支持以下任一目录：

```text
~/.kimi-code/skills/prodloop/SKILL.md
~/.agents/skills/prodloop/SKILL.md
~/.kimi-code/skills/codebase-audit/SKILL.md
~/.agents/skills/codebase-audit/SKILL.md
```

也可以不安装，直接从本仓库临时加载：

```bash
kimi --skills-dir /absolute/path/to/enterprise-product-delivery/skills
```

## 使用 prodloop

在真实项目仓库中启动对应 Agent。

Codex 输入：

```text
$prodloop
```

Kimi Code 输入：

```text
/skill:prodloop
```

然后提供完整目标，例如：

```text
请接管这个产品功能，从现状调查开始，连续完成产品定义、交互设计、技术设计、交付规划、开发实现、独立验收和发布准备。

项目目标：[希望用户最终完成什么]
目标用户：[使用者和场景]
范围内：[本次必须完成]
范围外：[本次明确不做]
质量档位：Q1

不要只交付方案。门禁通过后继续实施，直到 G8 或明确的 BLOCKED/STOPPED 条件。
```

新项目的持续状态保存在 `.prodloop/`。中断后再次调用 Skill，它会读取 `STATE.json` 和 `next_action` 继续。V0.1 已经创建的 `.codex/delivery/` 会被自动识别并原地继续；如果两个目录同时存在，Skill 会停止并要求确认权威状态，避免错误合并。

已有项目会进入 `brownfield` 接管分支。在 G1 之前必须完成真实运行基线、系统地图、行为契约、变更影响、回归范围和技术债边界；不会把老项目当作新项目重做。

已有 V1-V4 交付状态继续兼容。Skill 会按需调用非破坏性的启用工具，先备份原状态，再补充 UI、数据可视化或上下文管理能力；不会覆盖已经存在的产物。

### 让 prodloop 处理业务 UI

调用方式不变，只需在目标中写明用户、业务场景和界面范围。例如：

```text
$prodloop

接管这个 CRM 的客户详情与跟进流程，从现状调查一直做到可发布候选。
主要用户是销售和销售主管，桌面端高频使用，移动端用于现场快速记录。
需要重新设计本次范围内的界面，但不要改动其他模块或替换现有前端技术栈。
界面必须覆盖长客户名称、无数据、加载失败、权限不足、编辑冲突和提交重试。
质量档位：Q2。
```

Kimi Code 将第一行改为 `/skill:prodloop` 即可。Skill 会自动：

1. 判断界面是否在本次范围内；
2. 根据 CRM、ERP、审批、数据控制台、工业运维等场景选择业务交互参考；
3. 优先复用项目现有组件系统，并冻结 `.prodloop/UI_CONTRACT.md`；
4. 将视觉参考转成项目自己的规则，不直接模仿 Linear、Notion 等品牌；
5. 在 G6 使用真实业务数据、角色、异常状态和多个视口完成浏览器验收，并记录 `.prodloop/UI_VERIFICATION.md`。

可选地提供喜欢或不喜欢的参考产品；没有参考时，Skill 会根据业务任务和现有技术栈选择可逆默认值。不要只输入“做得高级一点”或“照着某网站做”，这不能定义业务可用性。

### 让 prodloop 处理图表和 Dashboard

调用方式仍然不变。在目标中写明图表服务的角色、业务判断、指标口径和后续动作。例如：

```text
$prodloop

接管销售管理看板，从指标口径核验、图表与下钻流程设计开始，持续做到可发布候选。
主要用户是销售主管；需要判断本月风险客户并进入对应客户记录采取行动。
成交额、赢单率和销售周期必须写明来源、分母、时间范围、时区和刷新时间。
覆盖无数据、延迟数据、查询失败、超长分类、极端值和不同角色权限。
质量档位：Q2。
```

Skill 会自动把 `visualization_scope` 设为 `in-scope`，在 G3 前冻结 `.prodloop/DATA_VIS_CONTRACT.md`，并在 G6 用独立计算、代表性数据和真实浏览器完成 `.prodloop/DATA_VIS_VERIFICATION.md`。它会检查指标来源、图型选择、坐标轴与比例、单位、缺失值、颜色语义、筛选、下钻、权限、失败状态、响应式、可访问性和性能，不把“图看起来合理”当作数据正确。

旧状态不会被强制重建。检测到已有项目需要新增数据可视化门禁时，Skill 会先备份状态，再非破坏性补充范围和两份产物。第三方图表模板只作为可选参考；采用其代码或资产前必须单独核对许可证。

### 控制上下文消耗和长任务续跑

V0.6 默认把 `120K tokens` 作为软上限，在宿主能提供准确用量时约于 `80%`（约 `96K`）建立上下文检查点。宿主不提供用量时，改用可观察触发器：每 8 个实质动作、阶段门禁、切换开发切片、长输出之前以及会话交接之前。

检查点使用三份项目文件：

- `.prodloop/CONTEXT.md`：最多 12000 字符的当前工作集和精确下一步；
- `.prodloop/CONTEXT_HISTORY.md`：检查点时间、原因、阶段和代码版本索引；
- `.prodloop/MEMORY_CANDIDATES.md`：经过证据支持、可能跨项目复用的候选经验。

Skill 会用计数工具持续记录实质动作与宿主报告的 context 用量。到期后先把事实、合同、测试和失败证据保存到各自权威文件，再重写短摘要，并校验摘要中的下一步与 `STATE.json` 完全一致。这里的 `120K/96K` 是 prodloop 准备持久检查点的阈值，不是 Codex 内部自动压缩的阈值。

在 Codex 中，Skill 会在预计自动压缩前先建立并验证检查点，压缩后从 `STATE.json`、`CONTEXT.md`、manifest、阻塞项和当前阶段产物恢复。在 Kimi Code 中，只有检查点验证成功且已积累有意义的上下文后才执行 `/compact`，随后读取同一最小恢复集；不会在持久事实和精确下一步保存前压缩，也不会无新增上下文时反复 `/compact`。检查点历史会记录运行时和选择的压缩路径，但只有宿主界面或命令证据才能证明压缩实际发生。

目前不默认引入向量数据库或知识图谱。单项目开发优先使用 Git、结构化状态和按需读取，可靠性更高、维护成本更低。只有跨项目复用频繁、现有索引检索确实失效且有治理负责人时，才升级为外部长记忆系统。

## 使用 codebase-audit

Codex 输入 `$codebase-audit`，Kimi Code 输入 `/skill:codebase-audit`。例如：

```text
请只读审计这个已有项目，重点回答它如何启动、核心业务流程如何穿过界面/逻辑/数据层、有哪些权限和兼容契约，以及修改目标模块会影响什么。不要改代码或安装依赖。
```

默认在对话中交付报告，不修改仓库。只有明确要求保存时才写 `CODEBASE_AUDIT.md`。审计报告可以交给 `prodloop` 复用，但必须核对版本、范围和时效，不能自动视为 G1 已通过。

## 质量档位

- `Q0`：探索验证，不得冒充生产产品。
- `Q1`：有限内部用户使用的工具。
- `Q2`：真实客户或正式业务系统。
- `Q3`：关键流程、多租户、敏感数据、合规或明确 SLA。

## 当前状态

V0.6 已加入上下文预算、可验证的工作摘要、检查点历史和候选长期记忆，并明确区分 Codex 自动压缩与 Kimi Code `/compact`。状态 schema V5 继续兼容 V1-V4；brownfield 接管、UI、数据可视化、上下文启用、门禁顺序和旧状态兼容均有自动化测试。Skill 负责在压缩前保存可恢复状态并在压缩后按证据恢复，不会声称检查点本身降低了当前请求的 token 用量。

详细文档：

- [系统规格](docs/企业级AI自主产品交付系统规格-V0.1.md)
- [V0.1 验证报告](docs/prodloop-V0.1-验证报告.md)
- [V0.2 验证报告](docs/prodloop-V0.2-验证报告.md)
- [V0.3 验证报告](docs/prodloop-V0.3-验证报告.md)
- [V0.4 验证报告](docs/prodloop-V0.4-验证报告.md)
- [V0.5 验证报告](docs/prodloop-V0.5-验证报告.md)
- [V0.6 验证报告](docs/prodloop-V0.6-验证报告.md)
