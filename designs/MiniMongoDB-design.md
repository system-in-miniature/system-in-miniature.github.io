# MiniMongoDB 设计文档（2026-07-30，v1 范围）

## 定位

System-in-Miniature 第七个项目：MongoDB 的教学版单机文档数据库内核。与 MiniPostgres 形成「关系 vs 文档」对照——同样有查询/索引/持久化，但数据模型、查询语言、更新语义完全不同。复制层（replica set/oplog 选举）v1 只打地基（oplog），完整复制引用 MiniDist 谱系，不在本仓库重造。

## v1 教学主题（按优先级）

1. **文档模型与更新算子**：文档 = 嵌套 dict/list；`$set/$unset/$inc/$push/$pull` 的路径语义（`a.b.c` 点路径、数组下标）；替换 vs 算子更新；`_id` 不可变。
2. **查询算子与匹配语义**：`$eq/$gt/$lt/$gte/$lte/$in/$ne/$exists/$and/$or/$not`；MongoDB 特有的「标量查询自动匹配数组元素」语义；嵌套文档的精确匹配 vs 点路径匹配的区别（教学重点，新手最大困惑源）。
3. **索引与查询计划**：`_id` 主索引自动创建；二级索引（单字段 + 复合，支持嵌套路径）；unique 索引；查询规划器选 IXSCAN vs COLLSCAN（基于简单选择度估计），`explain()` 暴露计划与扫描计数。
4. **聚合管道**：`$match/$project/$group/$sort/$limit`（最小集）；管道即算子流水线——与 MiniPostgres 的 Volcano 模型对照（在 mapping 文档里显式对比）。
5. **oplog**：所有写操作产出幂等的 oplog 条目（可重放、重放两次结果相同——这是 MongoDB oplog 的核心设计约束，教学点：为什么 `$inc` 在 oplog 里被改写成 `$set`）；oplog 是 capped 的（有界环形）。v1 只做「产出 + 幂等重放验证」，不做跨节点拉取。
6. **持久化**：journal（WAL 类比，CRC 帧 + 尾部截断修复，沿用系列惯例）+ checkpoint 快照 + 启动恢复（checkpoint + journal 重放，幂等）。简化声明：真实 MongoDB 由 WiredTiger 提供 MVCC/压缩/checkpoint，此处为教学版单写者模型。

## 明确非目标（写进 DIFFERENCES）

分片/mongos、事务（多文档 ACID）、`$lookup`、change streams、TTL 索引、文本/地理索引、BSON 二进制格式（用 JSON 可表示子集 + 类型标签模拟，声明与真实 BSON 类型序的差异）、WiredTiger 级并发。

## 架构

```
src/minimongodb/
  bson/        # 文档值模型：类型标签、比较序（简化版 BSON type ordering）、点路径读写
  query/       # 查询算子树、匹配器（含数组自动展开语义）
  update/      # 更新算子、路径修改、oplog 改写（$inc → $set）
  index/       # _id 索引 + 二级索引（有序结构）、unique 约束
  plan/        # 规划器（IXSCAN/COLLSCAN 选择 + 选择度估计）、explain
  aggregate/   # 管道算子
  oplog/       # 幂等条目模型、capped 环形、重放器
  storage/     # journal + checkpoint + 恢复
  collection.py / database.py  # 汇合层
labs/          # 至少 3 个可运行演示：数组匹配语义、explain 对比、oplog 幂等重放
docs/mapping.md, docs/DIFFERENCES.md
```

## 系列铁律（同 ROADMAP）

确定性（注入时钟/计数器造 ObjectId，禁 time.time/裸 random）；模块头讲解性 docstring + 关键处 why 注释；mapping 三档标注；背离必须声明；labs 只用公开 API；`uv run pytest -q` 全绿。

## 里程碑

- **M1**：bson 值模型 + CRUD + 查询/更新算子 + `_id` 索引 + journal 持久化 + oplog 产出与幂等重放 + labs + 文档。
- **M2**：二级/复合/unique 索引 + 规划器 + explain + 聚合管道。
- **M3**：capped oplog 收尾 + 与 MiniDist 的复制映射文档（oplog ≈ 逻辑日志运输 + Raft 式选举）。
