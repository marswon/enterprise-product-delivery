# enterprise-product-delivery

用于企业级软件产品端到端交付的 Codex Skill。从调查分析、产品定义、产品与 UX 设计、技术设计开始，持续进入开发、独立验收、发布准备和结果复盘，并通过持久化状态、阶段门禁和证据追溯防止 AI 跳步或虚假完成。

## 适用场景

- 从零开发软件产品；
- 为已有系统增加完整功能；
- 改造企业业务流程；
- 系统集成和数据迁移；
- 对缺陷或质量问题进行系统治理。

不适用于只有几行改动且规格已经完整的小修复，也不应用于只要求建议、评审或解释而未授权实施的任务。

## 安装

### 方法一：网页下载

1. 登录有权访问本仓库的 GitHub 账号。
2. 下载仓库 ZIP 并解压。
3. 将仓库中的 `skills/enterprise-product-delivery` 文件夹复制到 Codex skills 目录，确保最终目录为：

```text
~/.codex/skills/enterprise-product-delivery/SKILL.md
```

4. 重启 Codex 或新建任务。

### 方法二：通过 GitHub 安装

目标电脑需要先安装 Git，并通过 `gh auth login` 或 Git 凭证取得本私有仓库访问权限。运行：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo marswon/enterprise-product-delivery \
  --path skills/enterprise-product-delivery \
  --method git
```

这里明确使用 Git 克隆路径，避免部分 Python 环境缺少 HTTPS 下载支持。安装器发现目标目录已存在时会停止，不会自动覆盖旧版本。

## 使用

在真实项目仓库的 Codex 任务中输入：

```text
$enterprise-product-delivery

请接管这个产品功能，从现状调查开始，连续完成产品定义、交互设计、技术设计、交付规划、开发实现、独立验收和发布准备。

项目目标：[希望用户最终完成什么]
目标用户：[使用者和场景]
范围内：[本次必须完成]
范围外：[本次明确不做]
质量档位：Q1

不要只交付方案。门禁通过后继续实施，直到 G8 或明确的 BLOCKED/STOPPED 条件。
```

中断后再次调用 Skill，它会读取项目的 `.codex/delivery/STATE.json` 和 `next_action` 继续。

## 质量档位

- `Q0`：探索验证，不得冒充生产产品。
- `Q1`：有限内部用户使用的工具。
- `Q2`：真实客户或正式业务系统。
- `Q3`：关键流程、多租户、敏感数据、合规或明确 SLA。

## 当前状态

V0.1 已验证 Skill 结构、状态初始化、防覆盖、门禁顺序和追溯检查。尚未完成三个真实仓库前向测试，因此不声称已经证明能够高质量交付任意企业产品。

详细文档：

- [系统规格](docs/企业级AI自主产品交付系统规格-V0.1.md)
- [V0.1 验证报告](docs/enterprise-product-delivery-V0.1-验证报告.md)
