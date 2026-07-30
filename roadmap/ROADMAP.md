# System-in-Miniature 路线图（2026-07-30）

系列定位：用 Python 实现主流基础设施系统的教学版内核——**单机核心机制高保真 + 有选择地体现生产特性 + 简化协议/传输**。每个项目的三条铁律（来自 2026-07-30 五项目审查的教训）：

1. 关键模块必须有 why 级注释 + 一份「mini ↔ 真实系统」映射文档（等价 / 有意简化 / 语义相反 三档标注）；
2. 与真实系统的语义背离必须声明，静默的错误答案比缺特性伤害大；
3. 核心教学流程要有可直接运行的 labs/examples，不能只存在于测试里。

## 第一批（打磨完成，当前焦点）

目标：五个已有项目达到「可对外」质量 + MiniDist 落地。审查报告另行发布。

| 项目 | 状态 | P0（正确性 bug，必修） | P1（结构性/教学） |
|---|---|---|---|
| **MiniKafka** | 已验收，需返工 | 事务 acks=1 破坏原子性 | leader-epoch 截断（现为 pre-KIP-101 且新 leader 自截）、两阶段 rebalance、offset 存储改内部 compacted topic、mapping 文档 |
| **MiniRedis** | 已验收，需返工 | 副本过期删除导致复制链路永久 FAILED；`_applied_batches` 无界内存泄漏 | SCAN 全家桶、volatile-* 淘汰、PSUBSCRIBE、拆分 1531 行 executor、mapping 文档 + examples/ |
| **MiniPostgres** | 已验收，需返工 | UPDATE 后 CREATE UNIQUE INDEX 必误报；RR 写冲突静默丢更新（无 SerializationConflict）；RC 无 EPQ；int64 除法/SUM 溢出 | hot_eligible 死代码、DROP TABLE/INDEX、BEGIN ISOLATION LEVEL 语法、docs/tour.md |
| **MiniQdrant** | 已验收，需返工 | flush × optimize 并发产生重复命中 | filter-aware HNSW 遍历（现为后过滤）、量化改 int8 整数打分、消除每查询 O(N)、接线 optimizer policy、WAL 轮转、mapping 文档 |
| **MiniLucene** | 已验收，需返工 | 引号 keyword 查询 0 命中；连字符 ID 不可查 | DAAT 迭代器最小版、collect-then-fetch、phrase frequency 打分、rollback + stale lock、mapping 文档 |
| **MiniDist** | M2 完成（2026-07-30，未 commit） | — | 设计见 `portfolio/designs/MiniDist-design.md`。已交付：M1 仿真基座 + 协议 1（异步主从）+ 协议 4（Raft，883 行）+ 实验 1/2/3（含双协议对照与任期 fencing 演示），28 测试全绿。待做 M3：协议 2（WAL 运输）+ 协议 3（ISR+HW）+ 实验 4-7。**MiniRaft 并入本项目，不单独立项** |

第一批完成标准：每项目 P0 清零、mapping 文档就位、语义背离清单进 DIFFERENCES、labs/examples 可运行；MiniDist 到 M3（四协议 + 七组实验）。

## 第二批（新系统：单机内核为主）

| 项目 | 核心教学主题 | 备注 |
|---|---|---|
| **MiniS3** | 对象存储：不可变对象 + 版本化、multipart upload、ETag/条件请求、生命周期规则、erasure coding（教学版）、list 一致性 | **M1 完成**（2026-07-30，未 commit）：模型/版本化状态机/list 目录幻觉/崩溃原子性，19 测试 + 3 labs。设计：`designs/MiniS3-design.md`。待做 M2：multipart/条件请求/lifecycle |
| **MiniMongoDB** | 文档模型：BSON 类比、_id 与二级索引、聚合管道（match/project/group 最小集）、oplog + replica set 选举 | **M1 完成**（2026-07-30，未 commit）：bson 值模型/CRUD/查询更新算子（数组匹配语义）/幂等 oplog/journal 恢复，54 测试 + 3 labs。设计：`designs/MiniMongoDB-design.md`。待做 M2：二级索引/规划器/聚合管道 |

## 第三批（分布式与运行时）

| 项目 | 核心教学主题 | 依赖 |
|---|---|---|
| **MiniZookeeper** | 共识**服务**的 API 设计：ZAB（与 Raft 对照）、znode 树、session/ephemeral、watch、配方（锁/选举/成员） | 建在 MiniDist 仿真基座上 |
| **MiniCassandra** | 谱系里缺席的第 5 种范式：无主复制、gossip、hinted handoff、read repair、可调一致性（R+W>N）、LSM 存储 | 强依赖 MiniDist（quorum 原语、仿真基座）；LSM 部分与 MiniLucene segment 经验互补 |
| **MiniDocker** | 完全不同领域：namespace/cgroup/overlayfs、镜像分层、容器生命周期 | 独立项目，需真 Linux 特性，仿真策略与其他项目不同，放最后单独设计 |

## 排序理由

- MiniDist 排第一批：MongoDB（replica set）、Cassandra、Zookeeper 都需要它的基座或谱系做参照；先有谱系，后续项目的分布式层就是「引用 + 差异」而不是重写。
- MiniS3/MiniMongoDB 排第二批：单机内核为主，不被 MiniDist 阻塞，可与第一批打磨并行穿插。
- MiniDocker 排最后：唯一不属于「数据系统」谱系的项目，教学基建（确定性仿真）几乎不可复用，需要独立的设计讨论。

## 目录约定

- 各项目审查报告作为独立资产另行发布
- `portfolio/designs/` — 新项目设计文档
- 各项目仓库内 — 修复与 mapping 文档落在各自 repo，portfolio 只放跨项目资产
