---
id: computing-software.web-development.mkdocs.readthedocs-theme-options
name: readthedocs-theme-options
category: computing-software
field: web-development
product: mkdocs
tags: [readthedocs-theme, sidebar, navigation-depth, collapse-navigation]
level: practitioner
status: docs-checked
description: "Configure the built-in readthedocs theme: sidebar behaviour, prev/next button placement, logo, analytics and highlight.js options with defaults."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/choosing-your-theme.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/getting-started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Select it with `theme: readthedocs` or the longer form:

```yaml
theme:
  name: readthedocs
  collapse_navigation: true
  navigation_depth: 4
  titles_only: false
  sticky_navigation: true
  prev_next_buttons_location: bottom
  include_homepage_in_sidebar: true
  logo: img/logo.png
```

Defaults:
- `highlightjs: True`, extra `hljs_languages`
- `analytics.gtag` (GA4 `G-` ID, default null) and `analytics.anonymize_ip` (`False`)
- `include_homepage_in_sidebar: True`
- `prev_next_buttons_location`: `bottom`, `top`, `both` or `none` (default `bottom`)
- `navigation_depth: 4`
- `collapse_navigation: True` (only current page's section headers)
- `titles_only: False`
- `sticky_navigation: True`
- `logo`: image location replacing the site name text (default `null`)

This theme is a clone of the Read the Docs service theme with a restricted feature set: only two levels of navigation are supported.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Choosing your theme" (readthedocs section: option names, defaults, two-level navigation note) and the Getting Started page (`theme: readthedocs`). Removed the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
