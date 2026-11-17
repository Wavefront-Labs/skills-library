---
id: computing-software.web-development.mkdocs.search-prebuild-indexing
name: search-prebuild-indexing
category: computing-software
field: web-development
product: mkdocs
tags: [prebuild-index, indexing, search-plugin, nodejs]
level: advanced
status: docs-checked
description: "Control search index size and speed with prebuild_index and indexing (full, sections, titles) on the MkDocs search plugin."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`prebuild_index` (default `False`) generates a pre-built index of all pages, a performance gain for larger sites. Confirm the theme supports it (the built-in themes do).

```yaml
plugins:
  - search:
      prebuild_index: true
      indexing: 'sections'
```

Gotchas for `prebuild_index`:
- Requires Node.js with `node` on the system path. If calling `node` fails the build only warns and continues; add `--strict` to make it an error.
- Not recommended for small sites: bandwidth rises with little visible gain. Worth it for hundreds of pages.

`indexing` (default `full`) is the strategy for what to index, helpful when the index becomes huge:

| Value | Indexes |
| --- | --- |
| `full` | title, section headings and full text |
| `sections` | title and section headings |
| `titles` | only page titles |

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (search plugin `prebuild_index` and `indexing`): defaults, Node.js requirement, warning-only failure and `--strict`, small-site advice, and the three indexing options. Removed: a generic verify line.

Method: documentation only; no commands were run.
