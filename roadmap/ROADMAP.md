# System-in-Miniature Capability Roadmap

System-in-Miniature uses compact Python implementations to make the core
mechanisms of infrastructure systems inspectable. The projects favor semantic
clarity, explicit simplifications, and deterministic experiments over product
completeness.

All eight current project repositories have an initial committed baseline.
Milestone labels describe the capability delivered by each teaching kernel;
they are not claims of production readiness.

## Current milestones

| Project | Current milestone | Capabilities available now | Next capability milestone |
|---|---|---|---|
| **MiniKafka** | Implementation polished | Partitioned logs, replication, consumer groups, idempotence, and transactions | Deepen leader-epoch, rebalance, and offset-storage models |
| **MiniRedis** | Implementation polished | Typed data structures, expiration, eviction, persistence, and asynchronous replication | Broaden scan, eviction, pub/sub, and public example coverage |
| **MiniPostgres** | Implementation polished | SQL planning and execution, pages and indexes, MVCC, WAL, and vacuum concepts | Extend DDL, isolation syntax, and public-API teaching paths |
| **MiniQdrant** | Implementation polished | Filtered vector search, HNSW, immutable segments, optimization, WAL, and recovery | Explore filter-aware traversal, quantized scoring, and optimizer policies |
| **MiniLucene** | Implementation polished; labs pending | Analysis, positional inverted indexes, BM25, NRT readers, commits, and segment merging | Add cursor-based retrieval, collectors, and runnable labs |
| **MiniDist** | **M2** | One deterministic harness comparing asynchronous primary–replica replication with Raft | M3: add WAL-shipping and ISR/high-watermark protocols plus comparative experiments |
| **MiniMongoDB** | **M1** | Document values, CRUD, array-aware queries and updates, oplog replay, and journal recovery | M2: secondary indexes, planning, and a compact aggregation pipeline |
| **MiniS3** | **M1** | Immutable objects, versioning and delete markers, listing semantics, and crash-safe publication | M2: multipart upload, conditional requests, and lifecycle rules |

Documentation, translations, mappings, and labs are tracked per repository.
The series conventions are shared targets; availability is stated by each
project rather than inferred from a single portfolio-wide label.

## Batch 1 — Consolidate the current portfolio

The first batch strengthens the eight existing teaching kernels as a coherent
reader experience:

- keep mapping and difference documents aligned with executable behavior;
- expand runnable examples where a concept is currently demonstrated mainly by
  tests;
- make milestone and documentation availability visible independently; and
- improve cross-project navigation and static documentation checks.

MiniDist remains the shared comparison harness for replication protocols, while
the five mature single-system kernels continue to deepen their most distinctive
mechanisms.

## Batch 2 — Complete the next capability milestones

The second batch advances the three milestone-based projects:

- **MiniDist M3:** four replication protocols and a broader set of controlled
  failure experiments on one harness;
- **MiniMongoDB M2:** indexes, query planning, and aggregation; and
- **MiniS3 M2:** multipart upload, conditional operations, and lifecycle
  behavior.

This batch also grows bilingual coverage and converges the project mapping
documents on a common schema without hiding project-specific differences.

## Batch 3 — Extend the system spectrum

Future projects broaden the comparison space after the current portfolio has a
stable teaching and documentation baseline:

| Candidate | Teaching focus | Relationship to the portfolio |
|---|---|---|
| **MiniZooKeeper** | ZAB, znodes, sessions, watches, and coordination recipes | Reuses MiniDist's deterministic protocol harness |
| **MiniCassandra** | Leaderless replication, gossip, hinted handoff, read repair, tunable consistency, and LSM storage | Adds the leaderless/quorum branch to the replication spectrum |
| **MiniDocker** | Namespaces, cgroups, layered images, and container lifecycle | Extends the series beyond data systems and requires a Linux-specific teaching model |

Candidate scope and ordering may evolve as the existing projects reveal better
comparative teaching paths.
