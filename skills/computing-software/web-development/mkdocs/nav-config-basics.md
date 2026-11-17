---
id: computing-software.web-development.mkdocs.nav-config-basics
name: nav-config-basics
category: computing-software
field: web-development
product: mkdocs
tags: [nav, navigation, nav-titles, auto-navigation]
level: intro
status: docs-checked
description: "Define the MkDocs nav setting: plain paths, titled entries, paths relative to docs_dir, and what the default alphanumeric navigation does."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/getting-started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without `nav`, MkDocs discovers all Markdown under `docs_dir` and sorts alphanumerically by file name, with index files first in each sub-section. Set `nav` to control order and titles:

```yaml
nav:
  - index.md
  - about.md
```

Titles are inferred from the file (or file name). Override by putting a title before the path:

```yaml
nav:
  - Home: index.md
  - About: about.md
```

Rules:
- All paths are relative to `docs_dir`.
- A title set in `nav` is used throughout the site and overrides any title in the page itself.
- Pages not listed in `nav` are still built but are hidden: not in the menu and not in previous/next links.

See `nav-sections`, `nav-external-links`, `page-title-resolution`.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Configure Pages and Navigation) and "Configuration" (nav). Removed the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
