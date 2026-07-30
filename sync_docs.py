#!/usr/bin/env python3
"""Sync reader docs from each Mini* repo into the MkDocs tree.

Convention (series-wide):
  English canonical:  <repo>/README.md, <repo>/docs/*.md, selected root docs
  Chinese full copy:  <repo>/README.zh-CN.md, <repo>/docs/zh/<same-name>.md

This script copies them into docs/en/<project>/ and docs/zh/<project>/ so the
site renders the repos' Markdown directly — no content is authored here.
Run before every `mkdocs build/serve`. Missing zh files fall back to a stub
pointing at the English page, so a half-translated repo never breaks the build.
"""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

HUB = Path(__file__).resolve().parent
OUT_EN = HUB / "docs" / "en"
OUT_ZH = HUB / "docs" / "zh"

# project -> (local repo path, extra root-level docs beyond README + docs/*.md)
LOCAL_REPOS: dict[str, tuple[Path, list[str]]] = {
    "MiniKafka": (Path("~/MiniKafka"), []),
    "MiniRedis": (Path("~/MiniRedis-workspace/MiniRedis"), []),
    "MiniPostgres": (
        Path("~/MiniPostgres-workspace/MiniPostgres"),
        ["ARCHITECTURE.md", "DIFFERENCES_FROM_POSTGRESQL.md", "SCOPE.md", "LABS.md", "BEHAVIORAL_CONTRACT.md", "BEHAVIOR_MATRIX.md"],
    ),
    "MiniQdrant": (
        Path("~/MiniQdrant-workspace/MiniQdrant"),
        ["ARCHITECTURE.md", "DIFFERENCES_FROM_QDRANT.md"],
    ),
    "MiniLucene": (Path("~/MiniLucene-workspace/MiniLucene"), []),
    "MiniDist": (Path("~/MiniDist-workspace/MiniDist"), []),
    "MiniS3": (Path("~/MiniS3-workspace/MiniS3"), []),
    "MiniMongoDB": (Path("~/MiniMongoDB-workspace/MiniMongoDB"), []),
}

# In CI every repository is checked out below one shared parent. Locally, keep
# using the verified absolute paths above.
if "SIM_REPOS_ROOT" in os.environ:
    repos_root = Path(os.environ["SIM_REPOS_ROOT"])
    REPOS = {
        name: (repos_root / name, extra_roots)
        for name, (_, extra_roots) in LOCAL_REPOS.items()
    }
else:
    REPOS = LOCAL_REPOS

SKIP_DIRS = {"superpowers", "zh"}  # internal build docs / the zh mirror itself

LANG_LINE = re.compile(r"^>\s*\*\*Language\*\*.*$", re.MULTILINE)


def _clean(text: str) -> str:
    # Language-switch lines point at repo-relative paths that don't exist in
    # the hub tree; the site has its own language toggle via nav.
    return LANG_LINE.sub("", text)


def _copy(src: Path, dst: Path, *, is_readme: bool = False, lang: str = "en") -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = _clean(src.read_text(encoding="utf-8"))
    proj = dst.parent.name
    # In the hub tree every page sits flat inside <lang>/<project>/, so
    # repo-relative links into docs/ or docs/zh/ lose those prefixes and
    # README.md itself becomes index.md.
    text = text.replace("](./docs/", "](").replace("](docs/", "](")
    text = text.replace("](./zh/", "](").replace("](zh/", "](")
    text = text.replace("](../README.md)", "](index.md)").replace("](README.md)", "](index.md)")
    text = text.replace("](README.zh-CN.md)", "](../../zh/" + proj + "/index.md)")
    if lang == "zh":
        # Upward links from a zh page point at the English canonical copy.
        text = re.sub(r"\]\((?:\.\./)+([\w.-]+\.md)", rf"](../../en/{proj}/\1", text)
    else:
        # Upward links from flattened docs/ pages target repo-root docs,
        # which live flat in the same hub folder.
        text = re.sub(r"\]\((?:\.\./)+([\w.-]+\.md)", r"](\1", text)
    dst.write_text(text, encoding="utf-8")


def _zh_stub(en_rel: str) -> str:
    return f"# 暂无中文版\n\n该页中文翻译尚未完成，请先阅读英文版：[{en_rel}](../../en/{en_rel})\n"


def sync() -> None:
    for out in (OUT_EN, OUT_ZH):
        if out.exists():
            shutil.rmtree(out)

    for name, (repo, extra_roots) in REPOS.items():
        pairs: list[tuple[Path, Path | None, str]] = []  # (en_src, zh_src, rel_name)

        readme = repo / "README.md"
        if readme.exists():
            pairs.append((readme, repo / "README.zh-CN.md", "index.md"))

        for extra in extra_roots:
            src = repo / extra
            if src.exists():
                pairs.append((src, repo / "docs" / "zh" / extra, extra))

        docs_dir = repo / "docs"
        if docs_dir.exists():
            for md in sorted(docs_dir.rglob("*.md")):
                rel = md.relative_to(docs_dir)
                if any(part in SKIP_DIRS for part in rel.parts):
                    continue
                pairs.append((md, docs_dir / "zh" / rel, str(rel)))

        for en_src, zh_src, rel_name in pairs:
            is_readme = rel_name == "index.md"
            _copy(en_src, OUT_EN / name / rel_name, is_readme=is_readme)
            zh_dst = OUT_ZH / name / rel_name
            if zh_src is not None and zh_src.exists():
                _copy(zh_src, zh_dst, is_readme=is_readme, lang="zh")
            else:
                zh_dst.parent.mkdir(parents=True, exist_ok=True)
                zh_dst.write_text(_zh_stub(f"{name}/{rel_name}"), encoding="utf-8")
        print(f"{name}: {len(pairs)} pages")


if __name__ == "__main__":
    sync()
