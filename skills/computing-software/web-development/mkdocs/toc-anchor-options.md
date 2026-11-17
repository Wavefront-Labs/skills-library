---
id: computing-software.web-development.mkdocs.toc-anchor-options
name: toc-anchor-options
category: computing-software
field: web-development
product: mkdocs
tags: [toc-extension, permalink, baselevel, separator]
level: practitioner
status: docs-checked
description: "Tune the toc Markdown extension in MkDocs: permalink, baselevel and separator options and how to combine them under one toc entry."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `toc` extension gives every header an ID. Options go under `markdown_extensions` in `mkdocs.yml`:

- `permalink` (default `False`): add a permanent link at the end of each header. `True` uses the paragraph symbol; a string is used as the link text.
- `baselevel` (default `1`): shift header levels; with `2`, `# Header` renders as `<h2>`.
- `separator` (default `-`): character replacing whitespace in generated IDs.

```yaml
markdown_extensions:
  - toc:
      permalink: "#"
      baselevel: 2
      separator: "_"
```

Gotcha: define all options under a single `toc` entry; do not list `toc` several times.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Internal links: toc extension settings `permalink`, `baselevel`, `separator`, single `toc` entry). Removed the note about updating links and the Verify line, which the page does not state.
Method: documentation only; no commands were run.
