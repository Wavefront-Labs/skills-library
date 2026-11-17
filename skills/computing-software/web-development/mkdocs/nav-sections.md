---
id: computing-software.web-development.mkdocs.nav-sections
name: nav-sections
category: computing-software
field: web-development
product: mkdocs
tags: [nav, nav-sections, navigation-groups, nesting]
level: practitioner
status: docs-checked
description: "Group pages into nested navigation sections in mkdocs.yml and avoid the pitfall that a section cannot itself be assigned a page."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/choosing-your-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List related pages under a section title:

```yaml
nav:
  - Home: index.md
  - User Guide:
    - Writing your docs: writing-your-docs.md
    - Styling your docs: styling-your-docs.md
  - About:
    - License: license.md
    - Release Notes: release-notes.md
```

Result: three top-level items; "User Guide" and "About" are sections.

Gotchas:
- A section cannot have a page assigned to it; it is only a container for child pages and sub-sections.
- Sections can nest as deep as you like, but over-nesting makes the site hard to navigate.
- Sections need not mirror the directory structure.
- Themes may limit depth (the `readthedocs` theme supports two levels of navigation; sidebar depth is a theme option).

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Configure Pages and Navigation) and "Choosing your theme" (readthedocs: only two levels of navigation supported; `navigation_depth` option). Removed the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
