# System-in-Miniature Website

This repository is the documentation hub and metadata home for the
[`system-in-miniature`](https://github.com/system-in-miniature) organization.
It renders documentation sourced from the eight project repositories and keeps
the organization roadmap and design documents. Synced project pages are build
artifacts and are not committed here.

本仓库是 `system-in-miniature` 组织的文档站与元资产仓库：从八个项目仓库同步
Markdown 并生成 MkDocs 站点，同时保存组织路线图与设计文档。同步生成的项目页面
属于构建产物，不提交到本仓库。

## GitHub Pages repository name / GitHub Pages 仓库名

The GitHub remote repository **must be named
`system-in-miniature.github.io`**. This is the organization-root Pages site, so
the canonical URL remains <https://system-in-miniature.github.io> without a
project subpath. A local checkout may still use the directory name `website`.

GitHub 远端仓库名**必须为 `system-in-miniature.github.io`**。本站采用组织根
Pages 站点，因此规范 URL 保持为 <https://system-in-miniature.github.io>，
不添加项目子路径；本地检出目录仍可名为 `website`。

## Local build / 本地构建

Set `SIM_REPOS_ROOT` when all eight repositories live under one shared parent
directory. Otherwise create the gitignored `repos.local.json` with an explicit
path for each project; `SIM_REPOS_ROOT` takes precedence.

若八个仓库位于同一父目录，设置 `SIM_REPOS_ROOT`。否则创建被 git 忽略的
`repos.local.json`，为每个项目填写路径；`SIM_REPOS_ROOT` 优先。

```bash
uv run python sync_docs.py
uv run mkdocs build

# Shared-parent layout / 同一父目录布局
SIM_REPOS_ROOT=/path/to/repos uv run python sync_docs.py
```

## CI triggers / CI 触发方式

GitHub Pages rebuilds on every push to `main`, a
`repository_dispatch` event with type `docs-update`, and the daily scheduled
run. Project repositories can send `docs-update` after their documentation
changes; the daily run provides a fallback.

GitHub Pages 会在本仓库 `main` 分支每次 push、收到类型为 `docs-update` 的
`repository_dispatch`，以及每日定时任务时重建。各项目仓库可在文档变更后发送
该事件，每日任务作为兜底。
