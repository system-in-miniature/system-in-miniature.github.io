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

import json
import os
import re
import shutil
from collections.abc import Mapping
from pathlib import Path

HUB = Path(__file__).resolve().parent
OUT_EN = HUB / "docs" / "en"
OUT_ZH = HUB / "docs" / "zh"

# project -> extra root-level docs beyond README + docs/*.md
PROJECT_EXTRAS: dict[str, list[str]] = {
    "MiniKafka": [],
    "MiniRedis": [],
    "MiniPostgres": [
        "ARCHITECTURE.md",
        "DIFFERENCES_FROM_POSTGRESQL.md",
        "SCOPE.md",
        "LABS.md",
        "BEHAVIORAL_CONTRACT.md",
        "BEHAVIOR_MATRIX.md",
    ],
    "MiniQdrant": ["ARCHITECTURE.md", "DIFFERENCES_FROM_QDRANT.md"],
    "MiniLucene": [],
    "MiniDist": [],
    "MiniS3": [],
    "MiniMongoDB": [],
}


def _resolve_repos(
    *,
    environ: Mapping[str, str] = os.environ,
    config_path: Path = HUB / "repos.local.json",
) -> dict[str, tuple[Path, list[str]]]:
    """Resolve source repositories from CI root or an ignored local config."""
    repos_root = environ.get("SIM_REPOS_ROOT")
    if repos_root:
        root = Path(repos_root)
        return {
            name: (root / name, extra_roots)
            for name, extra_roots in PROJECT_EXTRAS.items()
        }

    if not config_path.exists():
        raise RuntimeError(
            "Repository paths are not configured. Set SIM_REPOS_ROOT to a "
            "shared parent directory, or create repos.local.json with one "
            "absolute path per project."
        )

    try:
        configured = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"Could not read repository paths from {config_path}: {exc}"
        ) from exc

    if not isinstance(configured, dict):
        raise RuntimeError(
            f"{config_path} must contain a JSON object of project paths."
        )

    missing = sorted(set(PROJECT_EXTRAS) - set(configured))
    if missing:
        raise RuntimeError(
            f"{config_path} is missing project paths: {', '.join(missing)}"
        )

    invalid = sorted(
        name
        for name in PROJECT_EXTRAS
        if not isinstance(configured[name], str) or not configured[name]
    )
    if invalid:
        raise RuntimeError(
            f"{config_path} has invalid project paths: {', '.join(invalid)}"
        )

    return {
        name: (Path(configured[name]), extra_roots)
        for name, extra_roots in PROJECT_EXTRAS.items()
    }


REPOS = _resolve_repos()

SKIP_DIRS = {"superpowers", "zh"}  # internal build docs / the zh mirror itself

LANG_LINE = re.compile(r"^>\s*\*\*Language\*\*.*$", re.MULTILINE)
INLINE_LINK = re.compile(
    r"(?P<prefix>\]\()(?P<target><?[^)\s>]+>?)(?P<suffix>(?:\s+[\"'][^\"']*[\"'])?\))"
)
REFERENCE_LINK = re.compile(
    r"^(?P<prefix>\s*\[[^\]]+\]:\s*)(?P<target><?\S+>?)",
    re.MULTILINE,
)


def _clean(text: str, *, project: str) -> str:
    # Language-switch lines point at repo-relative paths that don't exist in
    # the hub tree; the site has its own language toggle via nav.
    text = LANG_LINE.sub("", text)
    # Internal planning artifacts are intentionally excluded from the public
    # hub. Keep README references useful without creating broken local links.
    return re.sub(
        r"\]\((?:(?:\./)?docs/|(?:\.\./)*|\./)?superpowers/([^)]+)\)",
        rf"](https://github.com/system-in-miniature/{project}/"
        rf"blob/main/docs/superpowers/\1)",
        text,
    )


def _rewrite_local_links(
    text: str,
    *,
    src: Path,
    dst: Path,
    source_map: Mapping[Path, Path],
) -> str:
    """Translate repo-relative Markdown links into hub-relative links."""

    def replace(match: re.Match[str]) -> str:
        target = match.group("target")
        wrapped = target.startswith("<") and target.endswith(">")
        raw_target = target[1:-1] if wrapped else target
        path_part, fragment_marker, fragment = raw_target.partition("#")
        if not path_part.lower().endswith(".md"):
            return match.group(0)

        source_target = (src.parent / path_part).resolve()
        hub_target = source_map.get(source_target)
        if hub_target is None:
            return match.group(0)

        relative = Path(os.path.relpath(hub_target, dst.parent)).as_posix()
        rewritten = relative
        if fragment_marker:
            rewritten += f"#{fragment}"
        if wrapped:
            rewritten = f"<{rewritten}>"
        suffix = match.groupdict().get("suffix") or ""
        return f"{match.group('prefix')}{rewritten}{suffix}"

    text = INLINE_LINK.sub(replace, text)
    return REFERENCE_LINK.sub(replace, text)


def _copy(
    src: Path,
    dst: Path,
    *,
    project: str,
    source_map: Mapping[Path, Path],
) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = _clean(src.read_text(encoding="utf-8"), project=project)
    text = _rewrite_local_links(text, src=src, dst=dst, source_map=source_map)
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

        source_map: dict[Path, Path] = {}
        for en_src, zh_src, rel_name in pairs:
            source_map[en_src.resolve()] = OUT_EN / name / rel_name
            if zh_src is not None and zh_src.exists():
                source_map[zh_src.resolve()] = OUT_ZH / name / rel_name

        for en_src, zh_src, rel_name in pairs:
            _copy(
                en_src,
                OUT_EN / name / rel_name,
                project=name,
                source_map=source_map,
            )
            zh_dst = OUT_ZH / name / rel_name
            if zh_src is not None and zh_src.exists():
                _copy(
                    zh_src,
                    zh_dst,
                    project=name,
                    source_map=source_map,
                )
            else:
                zh_dst.parent.mkdir(parents=True, exist_ok=True)
                zh_dst.write_text(_zh_stub(f"{name}/{rel_name}"), encoding="utf-8")
        print(f"{name}: {len(pairs)} pages")


if __name__ == "__main__":
    sync()
