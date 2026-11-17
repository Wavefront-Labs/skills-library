---
id: computing-software.web-development.mkdocs.markdown-extensions-config
name: markdown-extensions-config
category: computing-software
field: web-development
product: mkdocs
tags: [markdown-extensions, python-markdown, toc-options, extension-config]
level: practitioner
status: docs-checked
description: "Enable Python-Markdown extensions in mkdocs.yml, pass per-extension options, and use the key/value form needed for config inheritance."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`markdown_extensions` adds extensions beyond the defaults (`meta`, `toc`, `tables`, `fenced_code`). Default value `[]`.

```yaml
markdown_extensions:
  - smarty
  - toc:
      permalink: true
  - sane_lists
```

A colon follows the extension name, with options indented beneath, one per line. Extensions without options are plain list items.

Alternative key/value form, required if you want to override options via inheritance (empty value `{}` when no options):

```yaml
markdown_extensions:
  smarty: {}
  toc:
    permalink: true
  sane_lists: {}
```

Third-party extensions (Python-Markdown wiki, MkDocs catalog) must be installed and follow their own docs. Option values can come from environment variables or `!relative` paths.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (markdown_extensions): default extensions `meta`, `toc`, `tables`, `fenced_code`, default `[]`, option nesting, the key/value form for inheritance, and dynamic values. Removed: a generic verify line.

Method: documentation only; no commands were run.
