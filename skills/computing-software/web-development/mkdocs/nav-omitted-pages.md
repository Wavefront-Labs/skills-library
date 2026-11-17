---
id: computing-software.web-development.mkdocs.nav-omitted-pages
name: nav-omitted-pages
category: computing-software
field: web-development
product: mkdocs
tags: [not-in-nav, hidden-pages, nav, omitted-files]
level: practitioner
status: docs-checked
description: "Keep pages out of the MkDocs navigation on purpose with not_in_nav, silencing the omitted-files warning (version 1.5+), and how exclude_docs interacts."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pages missing from `nav` are still built and reachable by direct link but are hidden from the menu and from previous/next links. Normally MkDocs reports them as omitted. Declare the intent with `not_in_nav` (new in 1.5), using .gitignore pattern format, paths relative to `docs_dir`:

```yaml
nav:
  - Foo: foo.md
  - Bar: bar.md

not_in_nav: |
  /private.md
```

- From 1.6, if `nav` is not specified at all, pages matching `not_in_nav` are excluded from the inferred navigation.
- Putting a file in `exclude_docs` takes precedence and implies `not_in_nav`.
- The related message level is `validation.nav.omitted_files` (default `info`).

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (not_in_nav, validation) and Writing Your Docs (pages not in nav are hidden unless linked to directly and left out of previous/next links). Removed: a generic verify line.

Method: documentation only; no commands were run.
