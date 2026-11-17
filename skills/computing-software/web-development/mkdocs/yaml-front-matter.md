---
id: computing-software.web-development.mkdocs.yaml-front-matter
name: yaml-front-matter
category: computing-software
field: web-development
product: mkdocs
tags: [yaml-front-matter, meta-data, page-meta, front-matter]
level: practitioner
status: docs-checked
description: "Add YAML front matter to a MkDocs page: delimiters, typed values, lowercase keys, and what happens when the YAML is invalid."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Meta-data is stripped before Markdown processing and passed to the page template (themes decide whether to display it). YAML style: the first line must be `---`; it ends at the first line of `---` or `...`.

```text
---
title: My Document
summary: A brief description of my document.
authors:
    - Waylan Limberg
    - Tom Christie
date: 2018-07-10
some_url: https://example.com
---
This is the first paragraph of the document.
```

- YAML detects types: `authors` is a list, `date` becomes a date object.
- Keys are case sensitive and MkDocs expects them all lowercase.
- The top level must be key/value pairs (a dict).
- If the YAML is invalid or not a mapping, MkDocs does not treat it as meta-data: `page.meta` is empty and the block is not removed from the page.

See `multimarkdown-metadata`, `page-template-key`.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Meta-Data; YAML Style Meta-Data). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
