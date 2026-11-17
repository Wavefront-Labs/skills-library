---
id: computing-software.web-development.mkdocs.third-party-theme-caution
name: third-party-theme-caution
category: computing-software
field: web-development
product: mkdocs
tags: [third-party-themes, theme-catalog, supply-chain, theme-name]
level: intro
status: docs-checked
description: "Pick and install a third-party MkDocs theme: where to find them, how to select with theme.name, and the code-execution warning."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/choosing-your-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
MkDocs includes two themes, `mkdocs` and `readthedocs`. Others are third party. Find them in the community wiki (MkDocs-Themes page) and the ranked catalog at github.com/mkdocs/catalog.

Steps:
1. Install the theme's Python package (a theme is a Python package; follow that theme's own install instructions).
2. Set the theme name from that package's docs:

```yaml
theme:
  name: <installed-theme-name>
```

Warning from the docs: installing a theme means installing a Python package and executing any code the author put in it. There is no sandboxing, so apply the usual caution.

Theme-specific options go under `theme:` too; read that theme's documentation. If you only need small tweaks to an existing theme, use `theme.custom_dir` instead (see `theme-custom-dir`).

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Choosing your theme" (Third Party Themes: community wiki, ranked catalog, installation warning) and "Customizing your theme" (`custom_dir`). Removed the pip command, the extra advice and the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
