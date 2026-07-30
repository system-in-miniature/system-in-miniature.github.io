# MiniS3 设计文档（2026-07-30，v1 范围）

## 定位

System-in-Miniature 第八个项目：S3 式对象存储的教学版。与系列其他项目互补的教学主题：**不可变对象语义、HTTP 风格的条件请求语义、以及「list 是怎么从平面 key 空间造出目录幻觉的」**。协议照系列惯例简化：直接 Python API 为主，薄 HTTP adapter 可选（v2）。

## v1 教学主题（按优先级）

1. **对象与桶模型**：平面 key 空间（无目录，`/` 只是字符）；对象不可变——PUT 同 key 是整体替换不是修改；ETag = 内容 MD5（multipart 例外见下，这是 S3 著名的坑，必须忠实呈现：`md5(各part md5拼接)-N` 格式）。
2. **版本化**：bucket 开启 versioning 后 PUT 产生新版本、DELETE 产生 delete marker（教学重点：删除不删数据）；按 version-id GET/DELETE；未开启时的 null version 语义；suspend 后的行为。
3. **Multipart upload**：init → upload part（≥指定最小尺寸，最后一片除外）→ complete（part 清单校验、按序拼接、原子发布）/ abort（清理）；未完成上传对 list 不可见；complete 的原子性沿用系列 tmp+fsync+rename 惯例。
4. **条件请求**：If-Match / If-None-Match（GET 的缓存语义 + PUT 的乐观并发控制——S3 2024 年才支持条件写，教学点：为什么对象存储做 CAS 这么晚）；412/304 语义。
5. **List 语义**：prefix + delimiter → contents + common prefixes（目录幻觉的实现机制）；分页（continuation token）；**list 强一致**（对齐 2020-12 后的真实 S3，并在 mapping 里讲这段一致性演进史）。
6. **生命周期规则**：教学版 expiration（按 age 过期当前版本/非当前版本），手动步进的 lifecycle tick（沿用系列确定性惯例），不做 storage class 迁移。
7. **磁盘布局与崩溃安全**：每对象内容文件 + JSON 元数据 + manifest；所有可见性变更走原子 rename；崩溃恢复扫描测试（故障注入矩阵，沿用系列惯例）。

## 明确非目标（写进 DIFFERENCES）

IAM/policy/ACL、加密、storage class 与归档、replication（跨桶/跨区）、erasure coding（v2 教学版候选）、presigned URL、真实 XML wire protocol、事件通知。

## 架构

```
src/minis3/
  model.py       # ObjectRecord/Version/DeleteMarker/ETag 计算
  bucket.py      # 桶级操作、versioning 状态机
  multipart.py   # 分片上传状态机
  conditional.py # If-Match/If-None-Match 判定
  listing.py     # prefix/delimiter/分页
  lifecycle.py   # 规则求值 + 手动 tick
  storage/       # 磁盘布局、原子发布、崩溃恢复
  store.py       # 汇合层（Service：buckets）
labs/            # 至少 3 个：版本化与 delete marker 观察、multipart ETag 之谜、If-Match CAS 并发演示
docs/mapping.md, docs/DIFFERENCES.md
```

## 系列铁律（同 ROADMAP）

确定性（注入时钟；version-id/upload-id 用注入计数器或 seeded 生成）；模块头讲解性 docstring + why 注释；mapping 三档标注；背离必须声明；labs 只用公开 API；`uv run pytest -q` 全绿；崩溃安全用故障注入测试。

## 里程碑

- **M1**：对象/桶模型 + ETag + 版本化 + list（prefix/delimiter/分页）+ 磁盘持久化与崩溃恢复 + labs + 文档。
- **M2**：multipart + 条件请求 + lifecycle。
- **M3**（可选）：教学版 erasure coding（k+m 奇偶校验演示）+ 薄 HTTP adapter。
