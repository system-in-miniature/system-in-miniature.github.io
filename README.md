# System-in-Miniature Website

This repository is the documentation hub and metadata home for the
[`system-in-miniature`](https://github.com/system-in-miniature) organization.
It renders documentation sourced from the eight project repositories and keeps
the organization roadmap and design documents. Synced project pages are build
artifacts and are not committed here.

本仓库是 `system-in-miniature` 组织的文档站与元资产仓库：从八个项目仓库同步
Markdown 并生成 MkDocs 站点，同时保存组织路线图与设计文档。同步生成的项目页面
属于构建产物，不提交到本仓库。

## Local build / 本地构建

The default mode uses the verified local absolute repository paths in
`sync_docs.py`. Set `SIM_REPOS_ROOT` when all eight repositories live under one
shared parent directory.

默认模式使用 `sync_docs.py` 中已验证的本机绝对路径；若八个仓库位于同一父目录，
可设置 `SIM_REPOS_ROOT`。

```bash
uv run python sync_docs.py
uv run mkdocs build

# Shared-parent layout / 同一父目录布局
SIM_REPOS_ROOT=/path/to/repos uv run python sync_docs.py
```

## CI triggers / CI 触发方式

GitHub Pages rebuilds on every push to this repository, a
`repository_dispatch` event with type `docs-update`, and the daily scheduled
run. Project repositories can send `docs-update` after their documentation
changes; the daily run provides a fallback.

GitHub Pages 会在本仓库每次 push、收到类型为 `docs-update` 的
`repository_dispatch`，以及每日定时任务时重建。各项目仓库可在文档变更后发送
该事件，每日任务作为兜底。
