---
id: computing-software.web-development.mkdocs.favicon-custom
name: favicon-custom
category: computing-software
field: web-development
product: mkdocs
tags: [favicon, docs-img, branding]
level: intro
status: docs-checked
description: "Replace the default MkDocs favicon by placing favicon.ico in docs/img, or by overriding it in a theme custom_dir."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/getting-started.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/customizing-your-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default MkDocs uses its own favicon. To use yours, create an `img` subdirectory in `docs` and put `favicon.ico` there; MkDocs detects and uses it automatically.

```text
mkdocs.yml
docs/
    index.md
    img/
        favicon.ico
```

Alternative when customizing the built-in `mkdocs` theme with `theme.custom_dir`: add the icon at `custom_theme/img/favicon.ico`, mirroring the parent theme's structure.

```yaml
theme:
  name: mkdocs
  custom_dir: custom_theme/
```

## Checked

2026-11-04. Confirmed against Getting Started (Changing the Favicon Icon) and Customizing Your Theme (`custom_dir`, `custom_theme/img/favicon.ico`). Removed: a precedence gotcha and a verify line the pages do not state.

Method: documentation only; no commands were run.
