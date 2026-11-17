---
id: computing-software.web-development.mkdocs.page-title-resolution
name: page-title-resolution
category: computing-software
field: web-development
product: mkdocs
tags: [page-title, title-meta, nav, setext-headers]
level: practitioner
status: docs-checked
description: "How MkDocs picks a page title: nav title, then title metadata, then the first level-1 header, then the file name, first match wins."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
MkDocs checks these in order and stops at the first hit:

1. A title for the page in the `nav` setting.
2. A `title` meta-data key in the document.
3. A level 1 Markdown header on the first line of the document body (Setext-style headers only since MkDocs 1.5).
4. The file name.

So if the menu shows a different title than the page heading, look for a `nav` entry:

```yaml
nav:
  - Home: index.md      # overrides any title in index.md
```

To control the title without touching nav, use front matter:

```text
---
title: My Document
---
```

Gotchas: a title defined in `nav` is used throughout the site for that page; the level 1 header counts only when it is on the first line of the document body.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Configure Pages and Navigation; Meta-Data, title key). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
