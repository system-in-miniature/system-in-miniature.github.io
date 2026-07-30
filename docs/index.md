# System-in-Miniature

**Teaching kernels of mainstream infrastructure systems, written in Python.**
用 Python 实现的主流基础设施教学内核。

Each project re-implements selected core mechanisms of a production system —
faithfully where it teaches and simplified where it does not. The series uses
the following conventions as portfolio-wide targets, with progress tracked in
each repository. / 每个项目选择性重现生产系统的核心机制：有教学价值处追求高保真，
其余部分明确简化。以下是系列约定目标，完成度在各仓库中分别追踪：

1. **Mapping docs** — map teaching mechanisms back to real-system concepts and classify semantic relationships explicitly.
   将教学机制映射回真实系统概念，并显式分类语义关系。
2. **Declared divergences** — any behavior that differs from the real system is documented, never silent.
   与真实系统的任何行为差异都必须声明，绝不静默。
3. **Runnable learning paths** — grow executable labs or examples alongside tests; availability is tracked per project.
   在测试之外逐步补齐可运行的 labs 或 examples，具体可用性按项目追踪。

## Projects / 项目

| Project | Real system | Core topics | Implementation | Docs |
|---|---|---|---|---|
| [MiniKafka](en/MiniKafka/index.md) | Apache Kafka | log segments, ISR/HW replication, idempotence, transactions, consumer groups | polished | expansion tracked |
| [MiniRedis](en/MiniRedis/index.md) | Redis | expiry, eviction (LRU/LFU), custom AOF-style log / snapshot (RDB analogue), partial resync, MULTI/WATCH | polished | expansion tracked |
| [MiniPostgres](en/MiniPostgres/index.md) | PostgreSQL | MVCC, WAL, isolation levels, B+Tree, cost-based planning, VACUUM/HOT | polished | expansion tracked |
| [MiniQdrant](en/MiniQdrant/index.md) | Qdrant | HNSW, payload filtering, quantization, segments, WAL, snapshots | polished | lab paths tracked |
| [MiniLucene](en/MiniLucene/index.md) | Apache Lucene | inverted index, segments/NRT, BM25, atomic commits | polished | labs pending |
| [MiniDist](en/MiniDist/index.md) | — (protocol spectrum) | async primary-backup vs Raft on one harness; acked-write-loss experiments | M2 | milestone docs available |
| [MiniMongoDB](en/MiniMongoDB/index.md) | MongoDB | document model, array matching semantics, idempotent oplog, journal | M1 | milestone docs available |
| [MiniS3](en/MiniS3/index.md) | Amazon S3 | versioning, delete markers, list/directory illusion, crash atomicity | M1 | milestone docs available |

中文版：将上表链接中的 `en/` 换为 `zh/`，或使用左侧导航的 Zh 目录。

## How to read / 阅读方式

Start with a project's README, then follow the mapping, differences, and
learning-path documents available for that project. Docs on this site are
rendered directly from each repository's Markdown — the repos are the single
source of truth.
先读项目 README，再查看该项目已有的 mapping、差异说明和学习路径文档。本站页面
直接渲染各仓库内的 Markdown，仓库是唯一事实源。

```bash
# rebuild this site / 重建本站
uv run python sync_docs.py && uv run mkdocs build
```
