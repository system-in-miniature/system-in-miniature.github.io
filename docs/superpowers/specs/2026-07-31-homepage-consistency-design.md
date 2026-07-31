# Homepage consistency design

## Goal

Make the System in Miniature landing-page actions visually aligned and make
every project site's root Home page fully bilingual in English and Simplified
Chinese.

## Scope

- The organization website's two introductory calls to action.
- The root `docs/index.md` page in MiniKafka, MiniRedis, MiniPostgres,
  MiniQdrant, MiniLucene, MiniDist, MiniS3, and MiniMongoDB.
- Focused regression checks and fresh MkDocs builds.

Tutorial chapters, reference pages, navigation structure, and implementation
code are outside this change.

## Design

The organization homepage will wrap its two introductory links in one
`home-actions` container. A small extra stylesheet will render the paragraph
MkDocs generates inside that container as two equal grid columns when space
permits and one equal-width column on narrow viewports. The links will fill
their tracks, center their labels, and stretch to the same height in a row.
This replaces the theme's intrinsic `inline-block` sizing without changing
Material's global button component.

Each project Home page will preserve its existing English structure and
technical details. Every title, section heading, explanatory paragraph, list
item, and navigation sentence on that page will receive a faithful Chinese
counterpart. Commands, paths, identifiers, and links remain shared instead of
being duplicated. The existing link to the dedicated Chinese documentation is
retained.

## Verification

- Build the organization site and assert that both CTA links are children of
  the dedicated container and that the extra stylesheet is loaded.
- Render the built homepage at desktop and mobile widths with Chromium; assert
  equal button width and height and inspect a screenshot.
- Add a small source-level documentation check to each project so future Home
  page headings remain bilingual and the page retains substantial Chinese
  content.
- Run each affected repository's focused check and MkDocs build, then inspect
  all worktree diffs for unrelated changes.

## Boundaries

No deployment, push, pull request, or generated `site/` output is included.
Existing unrelated warnings from MkDocs are reported separately from failures
introduced by this change.
