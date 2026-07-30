# MiniDist 设计文档（2026-07-30 草案）

## 定位

System-in-Miniature 系列的第六个项目：**分布式复制协议谱系的教学实现**。不是「第 101 个 mini-raft」，也不是给其他 Mini 项目复用的生产依赖，而是回答一个所有 Mini 项目都砍掉了的问题：**为什么 Kafka/Redis/Postgres/Qdrant 各自选了不同的复制协议，而不是都用教科书 Raft**。

核心设计决策：
- **独立教学项目**，与五个 Mini 仓库只靠文档映射连接，不靠代码依赖（避免五仓库耦合、避免通用接口被各系统语义差异撑到失真）。
- **同一个 KV 状态机 + 同一套故障注入，并排跑四种复制协议**，让差异可以用同一组实验直接对比。
- 全进程内仿真、确定性可复现（继承五个项目已验证的确定性测试风格）。

## 教学陷阱（为什么不做「通用 Raft 库」）

通用原语（Raft、心跳、quorum）已有大量教学实现（MIT 6.824、raft.github.io）。真正值得教、且现有教材没有的，是各系统**为什么不用教科书方案**：

- **Kafka 不用 quorum 复制**，用 ISR + HW：容忍 f 个副本失败只需 f+1 个副本（Raft 要 2f+1），换取吞吐；代价是需要外部 controller 做成员裁决。
- **Redis 主从是异步的**，明确接受已确认写丢失；Sentinel 只做 failover 裁决不做日志一致性——「为什么 Redis 敢这么弱」本身是一课。
- **Postgres 物理流复制**：复制的是 WAL 字节而非命令，同步/异步可调，failover 靠外部工具——「复制 WAL vs 复制状态机」的对比。
- **现代系统惯例（Qdrant 等）**：metadata 走 Raft、data 走自定义复制——「共识只管小数据」。

## 三层架构

### 第 1 层：仿真基座（真正值得通用化的资产）

把五个 Mini 项目各自的确定性测试基建提炼成公共库。这也是 FoundationDB / TigerBeetle 式 deterministic simulation testing 的教学点。

- `SimNet`：进程内消息网络，可注入延迟、丢包、乱序、单向/双向分区；所有随机性来自显式 seed。
- `SimClock`：逻辑时钟，手动步进；超时/租约全部基于它。
- `Scheduler`：确定性事件调度器，`tick()` 驱动，无真实线程/asyncio 竞态。
- `FailureInjector`：节点崩溃/重启（易失状态清空、持久状态保留）、磁盘 fsync 丢失窗口、消息级故障脚本。
- `Trace`：结构化事件日志（消息收发、状态转移、提交点），供实验断言与可视化。

### 第 2 层：原语层（独立模块，可单独实验）

- 故障检测：心跳 + 超时；租约（lease）与「租约为什么能防脑裂读」。
- 领导选举：bully 式最简版 + Raft 式任期选举（供第 3 层复用）。
- 成员管理：静态成员表 + 手动加减节点（动态成员变更列为 v2）。
- Quorum 读写：R+W>N 的可调一致性（为 MiniCassandra 预铺）。
- 分片路由：一致性哈希 **或** range 分片二选一 + 手动迁移协议（只做一种，不贪多）。

### 第 3 层：复制策略谱系（教学核心）

同一个 KV 状态机接口上并排实现四种协议：

| # | 协议 | 原型 | 关键机制 | 已确认写会丢吗 |
|---|---|---|---|---|
| 1 | 异步主从 | Redis | replica sink、复制 ID + offset、部分重同步、手动/协调 promote | 会（要能实验演示） |
| 2 | 主从 + 日志运输 | Postgres | WAL 字节流 shipping、sync/async commit 可调、timeline 切换 | async 会 / sync 不会 |
| 3 | ISR + HW + controller | Kafka | ISR 收缩扩张、HW 推进、min.insync、controller 裁决选举、leader epoch fencing | acks=all 且 min.insync 满足时不会 |
| 4 | Raft | 教科书 | 任期选举、日志复制、提交规则、崩溃恢复 | 不会 |

Raft 范围：election + log replication + crash recovery；snapshot 与 membership change 列为 v2（那两块占实现量一半但教学增量递减）。

#### 统一状态机接口（草案）

```python
class AckLevel(Enum):
    NONE = auto()      # 发出即成功（Redis 式）
    LEADER = auto()    # leader 落盘即成功（acks=1）
    QUORUM = auto()    # 多数派确认（Raft / sync commit）
    ALL_ISR = auto()   # 当前 ISR 全确认（Kafka acks=all）

class ReadLevel(Enum):
    LOCAL = auto()         # 任意副本本地读（可能读到旧值）
    LEADER = auto()        # 只从 leader 读
    LINEARIZABLE = auto()  # 线性一致读（read index / lease read）

class ReplicationGroup(Protocol):
    """一个副本组：N 个节点，共同维护一个 KV 状态机。"""

    def client_write(self, key: bytes, value: bytes, ack: AckLevel) -> WriteResult:
        """返回 ACCEPTED（含 commit 位点）或错误；ack 语义由具体协议解释，
        不支持的级别显式报错（如异步主从不支持 QUORUM）。"""

    def client_read(self, key: bytes, level: ReadLevel, node: NodeId | None = None) -> ReadResult:
        ...

    def tick(self) -> None:
        """推进一个确定性时间步：心跳、超时、复制拉取/推送均在此发生。"""

    def crash(self, node: NodeId) -> None: ...
    def restart(self, node: NodeId) -> None: ...

    def probe(self) -> GroupState:
        """暴露内部状态供实验断言：各节点日志/位点、当前 leader、任期/epoch、ISR 等。"""
```

四个实现各自解释这套接口，**不强求语义完全对齐**——「同一个 `ack=QUORUM` 在协议 A 里合法、在协议 B 里报错」本身就是教学内容。接口的作用是让实验 harness 可以用同一套脚本驱动四个协议。

#### 统一实验清单（每个协议跑同一组）

1. **正常复制**：写入 → 各副本收敛，观察复制延迟（tick 数）。
2. **ack 后杀 leader**：client 收到成功确认后立刻 crash leader，failover 完成后读——已确认写还在吗？（谱系的核心对比实验，预期：协议 1 丢、2 取决于 sync 配置、3/4 不丢）
3. **网络分区（少数派含旧 leader）**：旧 leader 是否还能接受写？恢复后分叉如何收敛？（观察：协议 1 双主脏写、协议 3 的 epoch fencing、协议 4 的任期拒绝）
4. **慢副本**：一个 follower 持续滞后——写入可用性受影响吗？（观察：协议 3 的 ISR 收缩 vs 协议 4 的多数派不受单个慢节点影响）
5. **副本落后后重连**：增量追赶 vs 全量重传的触发条件（协议 1 的 backlog 窗口、协议 4 的日志回溯）。
6. **读一致性矩阵**：三种 ReadLevel × 四种协议，哪些组合能读到 stale 数据。
7. **脑裂读**：分区期间从旧 leader LOCAL 读——租约如何消除这个窗口。

每个实验产出一张「协议 × 结果」对照表，写进 `docs/experiments.md`，并配可直接运行的 `labs/` 脚本（吸取五个项目「实验只存在于测试里」的教训）。

## 与现有/未来项目的连接

- 每个 Mini 项目补一页 `docs/distribution.md`：本系统的分布式层对应 MiniDist 谱系第几条 + 偏差点（MiniKafka 的 leader-epoch 截断、MiniRedis 的 failover 缺席等审查发现的落差收敛到这里，不在五个仓库各补一遍）。
- **MiniRaft 不单独立项**，并入本项目谱系第 4 条。
- **MiniZookeeper**（ZAB、session/watch、共识服务的 API 设计）与 **MiniCassandra**（无主复制、gossip、hinted handoff、可调一致性——谱系里缺席的第 5 种范式）建在本项目的仿真基座之上，作为后续批次。

## 非目标

- 真实网络传输（进程内仿真即全部；可留一个薄 TCP demo adapter）
- Raft snapshot / joint consensus 成员变更（v2）
- 拜占庭容错、CRDT、向量时钟系（除非 MiniCassandra 需要最小版本）
- 性能（吞吐/延迟数字无意义，仿真 tick 是唯一时间单位）

## 规模与里程碑

预计 5–8k 行 Python（与现有项目同量级）。

1. **M1 仿真基座**：SimNet/SimClock/Scheduler/FailureInjector + 确定性回放测试。
2. **M2 协议 1+4**（谱系两端：最弱与最强）+ 实验 1/2/3 跑通出对照表。
3. **M3 协议 2+3** + 全部 7 组实验 + `docs/experiments.md`。
4. **M4 原语层收尾**（分片路由 + 迁移）+ 五个 Mini 项目的 `docs/distribution.md` 映射页。

## 从第一天就要避免的（来自五项目审查的教训）

1. 源码零注释——本项目要求每个协议模块头部有「对应真实系统的 XXX 机制」的讲解块，关键状态转移处有 why 注释。
2. 缺映射文档——`docs/` 从 M2 起就维护 mapping/experiments 两篇读者文档，不允许只有验收文档。
3. 未声明的语义背离——每处与原型系统不同的行为进 DIFFERENCES 清单，分「等价/有意简化/语义相反」三档。
4. 实验只存在于测试里——labs/ 脚本与测试同步交付，不用内部 debug 钩子。
