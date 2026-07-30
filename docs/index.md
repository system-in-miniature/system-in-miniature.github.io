# System in Miniature

**Learn infrastructure by rebuilding its smallest faithful core in Python. / 用 Python 重建基础设施最小而可信的核心，在可运行实验中理解系统。**

From search and storage to logs and distributed protocols, each project makes
one production mechanism inspectable while stating simplifications explicitly. /
从搜索、存储到日志与分布式协议，每个项目都让一组生产机制变得可观察，并明确声明教学简化。

[Choose a learning path / 选择学习路线](#learning-paths){ .md-button .md-button--primary }
[Browse the document library / 浏览文档库](#document-library){ .md-button }

## Projects / 项目

<div class="grid cards" markdown>

-   🔎 **MiniLucene**

    ---

    Positional inverted indexes, BM25, NRT readers, commits, and segment
    merging. / 位置倒排索引、BM25、NRT reader、提交与段合并。

    `Difficulty 难度 · Beginner 入门` `Status 状态 · Polished; labs pending 实现成熟；实验待补`

    [教程 Tutorial](https://system-in-miniature.github.io/MiniLucene/){ .md-button .md-button--primary }
    [仓库 Repo](https://github.com/system-in-miniature/MiniLucene){ .md-button }

-   🧭 **MiniQdrant**

    ---

    Filtered vector search, HNSW, immutable segments, optimization, and
    recovery. / 过滤向量检索、HNSW、不可变段、优化与恢复。

    `Difficulty 难度 · Intermediate 中级` `Status 状态 · Polished; lab paths tracked 实现成熟；实验路线跟踪中`

    [教程 Tutorial](https://system-in-miniature.github.io/MiniQdrant/){ .md-button .md-button--primary }
    [仓库 Repo](https://github.com/system-in-miniature/MiniQdrant){ .md-button }

-   🐘 **MiniPostgres**

    ---

    SQL planning and execution over pages, indexes, MVCC, WAL, and vacuum. /
    基于页、索引、MVCC、WAL 与 vacuum 的 SQL 规划和执行。

    `Difficulty 难度 · Advanced 进阶` `Status 状态 · Polished; docs expanding 实现成熟；文档扩充中`

    [教程 Tutorial](https://system-in-miniature.github.io/MiniPostgres/){ .md-button .md-button--primary }
    [仓库 Repo](https://github.com/system-in-miniature/MiniPostgres){ .md-button }

-   🍃 **MiniMongoDB**

    ---

    Document semantics, array-aware queries and updates, oplog replay, and
    journal recovery. / 文档语义、数组感知查询与更新、oplog 重放及 journal 恢复。

    `Difficulty 难度 · Intermediate 中级` `Status 状态 · M1; milestone docs available M1；里程碑文档可用`

    [教程 Tutorial](https://system-in-miniature.github.io/MiniMongoDB/){ .md-button .md-button--primary }
    [仓库 Repo](https://github.com/system-in-miniature/MiniMongoDB){ .md-button }

-   🪣 **MiniS3**

    ---

    Object versioning, delete markers, listing, and crash-safe publication. /
    对象版本、删除标记、列举语义与崩溃安全发布。

    `Difficulty 难度 · Beginner 入门` `Status 状态 · M1; milestone docs available M1；里程碑文档可用`

    [教程 Tutorial](https://system-in-miniature.github.io/MiniS3/){ .md-button .md-button--primary }
    [仓库 Repo](https://github.com/system-in-miniature/MiniS3){ .md-button }

-   ⚡ **MiniRedis**

    ---

    Typed in-memory structures, expiry, eviction, persistence, and asynchronous
    replication. / 类型化内存结构、过期、淘汰、持久化与异步复制。

    `Difficulty 难度 · Intermediate 中级` `Status 状态 · Polished; docs expanding 实现成熟；文档扩充中`

    [教程 Tutorial](https://system-in-miniature.github.io/MiniRedis/){ .md-button .md-button--primary }
    [仓库 Repo](https://github.com/system-in-miniature/MiniRedis){ .md-button }

-   📜 **MiniKafka**

    ---

    Partitioned logs, ISR/HW replication, idempotence, transactions, and
    consumer groups. / 分区日志、ISR/HW 复制、幂等、事务与消费组。

    `Difficulty 难度 · Advanced 进阶` `Status 状态 · Polished; docs expanding 实现成熟；文档扩充中`

    [教程 Tutorial](https://system-in-miniature.github.io/MiniKafka/){ .md-button .md-button--primary }
    [仓库 Repo](https://github.com/system-in-miniature/MiniKafka){ .md-button }

-   🌐 **MiniDist**

    ---

    Compare asynchronous primary–replica replication with Raft in one
    deterministic fault harness. / 在同一确定性故障实验框架中对照异步主从复制与 Raft。

    `Difficulty 难度 · Advanced 进阶` `Status 状态 · M2; milestone docs available M2；里程碑文档可用`

    [教程 Tutorial](https://system-in-miniature.github.io/MiniDist/){ .md-button .md-button--primary }
    [仓库 Repo](https://github.com/system-in-miniature/MiniDist){ .md-button }

</div>

## Learning Paths / 学习路线 { #learning-paths }

### 1. Storage & Retrieval / 存储与检索

**MiniLucene → MiniQdrant → MiniPostgres → MiniMongoDB → MiniS3**

Start with the smallest retrieval loop, then add vector indexing, transactional
page storage, document semantics, and finally object-storage durability. This
order moves from “how results are found” to “how different data models are
stored and published safely.” /
先从最小检索闭环入手，再依次加入向量索引、事务型页存储、文档语义，最后学习对象存储的持久性。
这个顺序从“结果如何被找到”逐步走向“不同数据模型如何被存储并安全发布”。

1. **MiniLucene** — inverted indexes, scoring, and segment lifecycle / 倒排索引、评分与段生命周期。
2. **MiniQdrant** — approximate nearest-neighbor search, filtering, and vector segments / 近似最近邻检索、过滤与向量段。
3. **MiniPostgres** — pages, B+Tree indexes, MVCC, planning, and WAL / 页、B+Tree 索引、MVCC、查询规划与 WAL。
4. **MiniMongoDB** — document and array semantics, updates, oplog, and journal / 文档与数组语义、更新、oplog 与 journal。
5. **MiniS3** — flat keyspaces, versions, delete markers, and crash-safe publication / 平面 key 空间、版本、删除标记与崩溃安全发布。

### 2. Logs & Distributed Systems / 日志与分布式

**MiniRedis → MiniKafka → MiniDist**

Begin with one primary and its persistence/replication boundary, expand to
partitioned replicated logs and group coordination, then compare replication
protocols under controlled failures. The path turns local state transitions
into distributed safety questions one layer at a time. /
先理解单主节点的持久化与复制边界，再扩展到分区复制日志和消费组协调，最后在可控故障中比较复制协议。
这条路线逐层把本地状态变迁转化为分布式安全问题。

1. **MiniRedis** — expiry, persistence, asynchronous replication, and partial resync concepts / 过期、持久化、异步复制与部分重同步概念。
2. **MiniKafka** — partitioned logs, replication watermarks, idempotence, transactions, and groups / 分区日志、复制水位、幂等、事务与消费组。
3. **MiniDist** — deterministic failure experiments contrasting asynchronous replication with Raft / 用确定性故障实验对照异步复制与 Raft。

## Document Library / 文档库 { #document-library }

The existing aggregated documentation remains available as the detailed
reference layer. It is synchronized from each project repository, which remains
the source of truth. / 现有聚合文档继续作为详细参考层，并从各项目仓库同步；项目仓库仍是唯一事实源。

[English documentation](en/MiniLucene/index.md){ .md-button }
[中文文档](zh/MiniLucene/index.md){ .md-button }

## Community / 社区

Found a behavior that differs from the real system? Open the affected project's
**Issues**, choose **Semantic divergence / 语义偏差**, and include the project
version, a minimal reproduction, observed behavior, authoritative real-system
evidence, documentation status, and teaching impact. Deliberately omitted
features are not semantic mismatches. /
发现教学实现与真实系统行为不一致？请进入对应项目的 **Issues**，选择
**Semantic divergence / 语义偏差**，附上项目版本、最小复现、观察到的行为、真实系统的权威依据、
文档声明状态与教学影响。有意省略的功能不等同于语义偏差。

[Browse project repositories / 选择项目仓库](https://github.com/orgs/system-in-miniature/repositories){ .md-button .md-button--primary }
[Contribution guide / 贡献指引](https://github.com/system-in-miniature/.github/blob/main/CONTRIBUTING.md){ .md-button }

## About / 关于 { #about }

System in Miniature is a bilingual collection of compact Python teaching
kernels. It favors semantic clarity, declared divergence, deterministic
experiments, and runnable learning paths over product completeness. These
projects are educational kernels, not production replacements. /
System in Miniature 是一组双语的紧凑型 Python 教学内核，优先追求语义清晰、偏差显式、
实验确定且学习路径可运行，而非产品功能完备。所有项目均用于教学，不是生产系统替代品。
