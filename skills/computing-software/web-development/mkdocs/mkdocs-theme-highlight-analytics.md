---
id: computing-software.web-development.mkdocs.mkdocs-theme-highlight-analytics
name: mkdocs-theme-highlight-analytics
category: computing-software
field: web-development
product: mkdocs
tags: [highlightjs, hljs-languages, analytics, gtag]
level: practitioner
status: docs-checked
description: "Set highlight.js styles and extra languages and enable Google Analytics v4 (gtag) in the built-in mkdocs theme."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/choosing-your-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
theme:
  name: mkdocs
  highlightjs: true
  hljs_style: github
  hljs_style_dark: github_dark
  hljs_languages:
    - yaml
    - rust
  analytics:
    gtag: G-ABC123
```

- `highlightjs` (default `True`): highlight code blocks with highlight.js.
- `hljs_style` (default `github`) for light mode; `hljs_style_dark` (default `github_dark`) for dark mode.
- `hljs_languages`: by default highlight.js supports only 23 common languages; list others here.
- `analytics.gtag`: a Google Analytics v4 tracking ID in `G-` format. Default `null` leaves analytics off. Only GA4 is supported.

Note: the `readthedocs` theme documents `highlightjs`, `hljs_languages` and `gtag` too, lists no `hljs_style` options, and adds `anonymize_ip`.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Choosing your theme" (mkdocs and readthedocs sections: `highlightjs`, `hljs_style`, `hljs_style_dark`, `hljs_languages` and its 23-language note, `analytics.gtag`, `anonymize_ip`). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
