# System-in-Miniature

**Teaching kernels of mainstream infrastructure systems, written in Python.**
用 Python 实现的主流基础设施教学内核。

Each project re-implements the core mechanisms of a production system — faithfully where it teaches, simplified where it doesn't — with three series-wide rules / 系列三条铁律：

1. **Mapping docs** — every module maps back to the real system's concepts, tagged *equivalent / simplified / semantically different*.
   每个模块映射回真实系统概念，按「等价 / 有意简化 / 语义相反」三档标注。
2. **Declared divergences** — any behavior that differs from the real system is documented, never silent.
   与真实系统的任何行为差异都必须声明，绝不静默。
3. **Runnable labs** — the key lessons are executable scripts, not just tests.
   核心教学流程是可直接运行的脚本，而不只是测试。

## Projects / 项目

| Project | Real system | Core topics | Status |
|---|---|---|---|
| [MiniKafka](en/MiniKafka/index.md) | Apache Kafka | log segments, ISR/HW replication, idempotence, transactions, consumer groups | polished |
| [MiniRedis](en/MiniRedis/index.md) | Redis | expiry, eviction (LRU/LFU), AOF/RDB, partial resync, MULTI/WATCH | polished |
| [MiniPostgres](en/MiniPostgres/index.md) | PostgreSQL | MVCC, WAL, isolation levels, B+Tree, cost-based planning, VACUUM/HOT | polished |
| [MiniQdrant](en/MiniQdrant/index.md) | Qdrant | HNSW, payload filtering, quantization, segments, WAL, snapshots | polished |
| [MiniLucene](en/MiniLucene/index.md) | Apache Lucene | inverted index, segments/NRT, BM25, atomic commits | polished |
| [MiniDist](en/MiniDist/index.md) | — (protocol spectrum) | async primary-backup vs Raft on one harness; acked-write-loss experiments | M2 |
| [MiniS3](en/MiniS3/index.md) | Amazon S3 | versioning, delete markers, list/directory illusion, crash atomicity | M1 |
| [MiniMongoDB](en/MiniMongoDB/index.md) | MongoDB | document model, array matching semantics, idempotent oplog, journal | M1 |

中文版：将上表链接中的 `en/` 换为 `zh/`，或使用左侧导航的 Zh 目录。

## How to read / 阅读方式

Start with a project's README, then its `mapping` doc (module ↔ real system), then run the labs. Docs on this site are rendered directly from each repository's Markdown — the repos are the single source of truth.
先读项目 README，再读 mapping 文档（模块 ↔ 真实系统对照），然后跑 labs。本站页面直接渲染各仓库内的 Markdown，仓库是唯一事实源。

```bash
# rebuild this site / 重建本站
uv run python sync_docs.py && uv run mkdocs build
```
