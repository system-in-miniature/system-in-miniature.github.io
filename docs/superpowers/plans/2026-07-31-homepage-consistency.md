# Homepage Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the organization homepage actions and make all eight project Home pages fully English-Chinese bilingual.

**Architecture:** The organization site gets one narrowly scoped responsive grid and no global Material overrides. Each project keeps its current Home-page information architecture while pairing every prose unit with a Chinese translation; focused source checks prevent later regression.

**Tech Stack:** Markdown, MkDocs Material, CSS Grid, Python `unittest`, Playwright Chromium.

---

### Task 1: Equal organization-home actions

**Files:**
- Modify: `docs/index.md`
- Modify: `mkdocs.yml`
- Create: `docs/stylesheets/extra.css`
- Test: `tests/test_homepage_layout.py`

- [ ] **Step 1: Verify the structural regression test fails**

Run: `uv run python -m unittest tests.test_homepage_layout -v`

Expected: `FAIL` because the generated homepage has zero `md-button` links inside `.home-actions`.

- [ ] **Step 2: Group the actions**

Replace the two standalone links with this Markdown-in-HTML block:

```html
<div class="home-actions" markdown>
[Choose a learning path / 选择学习路线](#learning-paths){ .md-button .md-button--primary }
[Browse the document library / 浏览文档库](#document-library){ .md-button }
</div>
```

- [ ] **Step 3: Add the scoped layout stylesheet**

Create `docs/stylesheets/extra.css` with:

```css
.home-actions > p {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-auto-rows: 1fr;
  gap: 0.5rem;
}

.home-actions .md-button {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  text-align: center;
}

@media screen and (max-width: 44.984375em) {
  .home-actions > p {
    grid-template-columns: minmax(0, 1fr);
  }
}
```

Load it from `mkdocs.yml` using:

```yaml
extra_css:
  - stylesheets/extra.css
```

- [ ] **Step 4: Verify structure and rendering**

Run: `uv run python -m unittest tests.test_homepage_layout -v`

Expected: one passing test.

Build the site and use Playwright at widths 1440, 900, 600, and 390. At every width assert the two button bounding boxes have equal width and height; save a desktop and mobile screenshot under `/tmp` for visual inspection.

### Task 2: Fully bilingual project Home pages

**Files:**
- Modify: `/home/jrjyan/MiniKafka/docs/index.md`
- Modify: `/home/jrjyan/MiniRedis-workspace/MiniRedis/docs/index.md`
- Modify: `/home/jrjyan/MiniPostgres-workspace/MiniPostgres/docs/index.md`
- Modify: `/home/jrjyan/MiniQdrant-workspace/MiniQdrant/docs/index.md`
- Modify: `/home/jrjyan/MiniLucene-workspace/MiniLucene/docs/index.md`
- Modify: `/home/jrjyan/MiniDist-workspace/MiniDist/docs/index.md`
- Modify: `/home/jrjyan/MiniS3-workspace/MiniS3/docs/index.md`
- Modify: `/home/jrjyan/MiniMongoDB-workspace/MiniMongoDB/docs/index.md`
- Test: each repository's `tests/test_docs_homepage.py`

- [ ] **Step 1: Add and run the failing documentation contract**

Use this focused test in every repository:

```python
import re
import unittest
from pathlib import Path


class DocumentationHomepageTest(unittest.TestCase):
    def test_homepage_is_fully_bilingual(self) -> None:
        homepage = Path("docs/index.md").read_text(encoding="utf-8")
        headings = [line for line in homepage.splitlines() if line.startswith("#")]

        self.assertTrue(headings)
        self.assertTrue(all(" / " in heading for heading in headings))
        self.assertIn("[Chinese edition / 中文版]", homepage)
        self.assertGreaterEqual(len(re.findall(r"[\u4e00-\u9fff]", homepage)), 120)


if __name__ == "__main__":
    unittest.main()
```

Run `uv run python -m unittest tests.test_docs_homepage -v` in each repository.

Expected: all eight fail on English-only headings and/or insufficient Chinese content.

- [ ] **Step 2: Translate without changing technical claims**

For every `docs/index.md`:

- format the title and every section heading as `English / 中文`;
- retain the English paragraph or numbered item first and add its complete Chinese counterpart immediately after it;
- keep command blocks, source identifiers, paths, output literals, and URLs single-copy;
- keep the existing dedicated Chinese-documentation link;
- translate link labels when the surrounding navigation sentence is translated;
- do not alter feature scope, compatibility claims, experiment results, or reading order.

- [ ] **Step 3: Verify each source contract and build**

Run `uv run python -m unittest tests.test_docs_homepage -v` in each repository, followed by `uv run mkdocs build --strict`.

Expected: the focused test passes in every repository and every site build exits zero. Pre-existing MkDocs link or navigation notices may remain if they are not caused by these Home-page edits.

### Task 3: Cross-repository acceptance

**Files:**
- Inspect all files changed in Tasks 1 and 2.

- [ ] **Step 1: Run whitespace and scope checks**

Run `git diff --check` in all nine repositories and inspect `git status --short` plus `git diff --stat` in each.

Expected: no whitespace errors and no files outside the documented scope, tests, and design/plan records.

- [ ] **Step 2: Re-run the complete focused verification set**

Re-run the organization layout test and all eight project documentation tests from clean command invocations, then rebuild all nine MkDocs sites.

Expected: zero test failures and zero build failures.
