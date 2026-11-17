---
id: computing-software.web-development.mkdocs.exclude-docs
name: exclude-docs
category: computing-software
field: web-development
product: mkdocs
tags: [exclude-docs, gitignore-patterns, build-exclusion, dot-files]
level: practitioner
status: docs-checked
description: "Keep files out of the built site with exclude_docs (1.5+) using .gitignore pattern syntax, including the implicit dot-file and templates defaults."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`exclude_docs` (new in 1.5) lists patterns of files under `docs_dir` not to include in the built site, in .gitignore pattern format:

```yaml
exclude_docs: |
  # A file with this name anywhere.
  api-config.json

  # Top-level "docs/requirements.txt".
  /requirements.txt

  # Any file with this extension anywhere.
  *.py

  # But keep this particular file.
  !/foo/example.py
```

Implicit defaults, always prepended: `.*` (dot-files and dirs) and `/templates/`. To start fresh, negate them first; to re-include one dot-directory: `!.assets`.

Changed in 1.6: it no longer applies the drafts behaviour for `mkdocs serve`. For pages visible in serve but not build use `draft_docs`.

An excluded file implies `not_in_nav`, so no omitted-page warning appears.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (exclude_docs, not_in_nav): new in 1.5, .gitignore format, the example, implicit `.*` and `/templates/` defaults, `!.assets`, the 1.6 change, and precedence over `not_in_nav`. Removed: a generic verify line.

Method: documentation only; no commands were run.
