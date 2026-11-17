---
id: computing-software.web-development.mkdocs.source-extensions-dotfiles
name: source-extensions-dotfiles
category: computing-software
field: web-development
product: mkdocs
tags: [source-file-extensions, dot-files, markdown-files, exclude-docs]
level: practitioner
status: docs-checked
description: "Which Markdown file extensions MkDocs accepts and why files or directories beginning with a dot are skipped (and how to override that)."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Accepted Markdown extensions: `markdown`, `mdown`, `mkdn`, `mkd`, `md`. All such files under `docs_dir` are rendered.

Files and directories whose names begin with a dot (`.foo.md`, `.bar/baz.md`) are ignored. The `exclude_docs` default implicitly prepends these patterns:

```yaml
exclude_docs: |
  .*
  /templates/
```

To opt a dot-directory back in, negate it:

```yaml
exclude_docs: |
  !.assets
```

Symptom: a page or asset in `.something/` is missing from `site/`. Fix with the negated pattern above.

See also `exclude-docs`.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (File layout: accepted extensions, dot-file note) and "Configuration" (exclude_docs: implicit `.*` and `/templates/` defaults, `!.assets` example). Removed the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
