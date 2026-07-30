# System-in-Miniature 组织仓库结构设计（2026-07-30）

## 结论概览

- 组织名建议：`system-in-miniature`（备选 `sys-in-mini`；全小写、连字符，GitHub 惯例）。
- **共 10 个仓库**：8 个项目仓库 + `.github`（组织门面）+ `system-in-miniature.github.io`（文档站 + 元资产；本地工作区目录可继续名为 `website`）。
- **需要门面，但不需要单独的"门面仓库"**：门面职责拆给 `.github`（组织首页）和 `system-in-miniature.github.io`（读者入口），不再建第三个 meta 仓库——仓库越少，"从组织首页到任一项目 ≤2 次点击"越容易保证。

## 仓库清单

```
system-in-miniature/
├── .github            # 组织门面 A：profile README + 共享模板/工作流
├── system-in-miniature.github.io
│                      # 组织门面 B：组织根 Pages 站 + roadmap/designs（元资产）
├── MiniKafka          # 8 个项目仓库，保持 CamelCase 命名
├── MiniRedis          #（与代码内包名 minikafka/miniredis 的小写形成
├── MiniPostgres       #  "仓库名=品牌名、包名=Python 惯例" 的固定对应）
├── MiniQdrant
├── MiniLucene
├── MiniDist
├── MiniMongoDB
└── MiniS3
```

### `.github`（组织门面 A：3 秒钟说清这是什么）

- `profile/README.md`：组织首页自动渲染。双语，一屏内容：一句话定位（"主流基础设施的 Python 教学内核：核心机制高保真 + 差异显式声明 + 可运行实验"）、8 项目表格（名称/对标系统/一句话主题/状态徽章）、指向 website 的"开始阅读"链接、系列三条铁律。
- `workflow-templates/`：共享 CI 模板（见下"每仓库标准件"），各项目仓库引用同一份，避免 8 份漂移。
- `ISSUE_TEMPLATE/`：两类模板——"语义偏差报告"（声称与真实系统等价的行为实际不一致，系列最高优先级 issue 类型）与普通 bug/建议。

### `system-in-miniature.github.io`（组织门面 B：读者真正停留的地方）

GitHub 远端仓库名**必须为 `system-in-miniature.github.io`**，以启用组织根
Pages URL `https://system-in-miniature.github.io`。本地检出目录可以继续使用
`website`，但不能以 `website` 作为最终远端仓库名。

现在的 `portfolio/docshub` 整体迁入，外加元资产：

```
system-in-miniature.github.io/
├── mkdocs.yml
├── sync_docs.py        # 改造：本地绝对路径 → CI 里 actions/checkout 各仓库后按相对路径同步
├── docs/index.md       # 站点首页（双语落地页）
├── roadmap/ROADMAP.md  # 现 portfolio/ROADMAP.md
├── designs/*.md        # 现 portfolio/designs/（MiniDist/MiniMongoDB/MiniS3/本文档）
└── .github/workflows/deploy.yml  # checkout 8 仓库 → sync → mkdocs build → GitHub Pages
```

- GitHub Pages 挂在此仓库，站点即组织根 URL `https://system-in-miniature.github.io`。
- 各项目仓库 push 到 main 时通过 `repository_dispatch`（或定时任务）触发本仓库重建，文档站始终跟随各仓库 md——保持"仓库是唯一事实源"的现有设计。
- 旧手写 `portfolio/site/` 不迁移，就此废弃。

### 8 个项目仓库

保持现状结构（`src/ + tests/ + labs|examples/ + docs/ + 双语约定`），组织化只需补"标准件"。

## 每仓库标准件（发布前 checklist）

| 项 | 内容 |
|---|---|
| LICENSE | MIT，8 仓库统一 |
| CI | 引用 `.github` 共享模板：`uv sync --dev && uv run pytest -q` + labs 冒烟（每个 lab 跑通即过）；Python 3.12/3.13 矩阵 |
| README 头部 | 徽章（CI/license/python 版本）+ 一句话定位 + 指向 website 对应项目页的链接 |
| topics | 统一打 `education` `system-in-miniature` + 各自领域标签（`kafka` `raft` …），组织内可发现性靠它 |
| About 栏 | 一句话 + website 项目页链接 |
| tag | 公开时打 `v0.1.0`，此后语义化版本 |

组织首页 pin 6 个：五个已打磨项目 + MiniDist（谱系是系列最独特的卖点）。

## 发布顺序

1. 八个项目仓库的初始基线已提交；发布前确认各仓默认分支与 CI 触发条件一致。
2. 建组织 + `.github` + `system-in-miniature.github.io`（本地目录可名为 `website`；迁入 docshub 与 portfolio 元资产，改造 sync 脚本为 CI 模式）。
3. 各项目仓库补标准件（LICENSE/CI/badges/topics）→ push → 打 v0.1.0。
4. `system-in-miniature.github.io` 首次 Pages 部署，验证全站链接。
5. 组织首页 pin + profile README 上线。

## 已确认决策

1. **审查报告不迁入公开文档站**：审查报告是独立资产，另行发布。
2. **`portfolio/` 本地目录的去向**：迁入文档站仓库后本地 sim-workspace 保留 symlink 工作区形态不变；`portfolio/site/`（旧手写站）删除。
