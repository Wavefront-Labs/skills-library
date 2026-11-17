---
id: computing-software.web-development.mkdocs.draft-docs
name: draft-docs
category: computing-software
field: web-development
product: mkdocs
tags: [draft-docs, drafts, mkdocs-serve, clean-flag]
level: practitioner
status: docs-checked
description: "Mark pages as drafts with draft_docs (1.6+) so they appear in mkdocs serve with a DRAFT mark but are left out of mkdocs build."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`draft_docs` (new in 1.6) lists .gitignore-style patterns under `docs_dir`. Matching files are available in `mkdocs serve` with a "DRAFT" mark but are not included in the build.

```yaml
draft_docs: |
  # A "drafts" directory anywhere.
  drafts/

  # A Markdown file ending in _unpublished.md anywhere.
  *_unpublished.md

  # But keep this particular file.
  !/foo_unpublished.md
```

To make serve behave exactly like build (no drafts shown):

```bash
mkdocs serve --clean
```

Use `draft_docs` rather than `exclude_docs` when you want to see a page while writing: since 1.6, `exclude_docs` no longer gives serve the drafts behaviour.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (draft_docs, exclude_docs): new in 1.6, .gitignore pattern format, DRAFT mark in serve, not in build, `mkdocs serve --clean`, and the 1.6 change to `exclude_docs`. Removed: a generic verify line.

Method: documentation only; no commands were run.
