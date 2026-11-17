---
id: computing-software.web-development.mkdocs.customize-with-extra-css
name: customize-with-extra-css
category: computing-software
field: web-development
product: mkdocs
tags: [customize-theme, css-tweak, extra-css, docs-dir]
level: intro
status: docs-checked
description: "Make minor look-and-feel tweaks to any MkDocs theme by putting CSS or JavaScript in docs and listing it in extra_css or extra_javascript."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/customizing-your-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For small tweaks that need only CSS and/or JavaScript, use the docs directory; no theme override needed.

1. Create `docs/style.css` next to the Markdown:

```css
h1 {
  color: red;
}
```

2. List it in `mkdocs.yml`:

```yaml
extra_css:
  - style.css
```

If `mkdocs serve` is running, the change is picked up and the page updates automatically.

Gotcha: extra CSS and JavaScript files are added to the generated HTML after the page content. If you need to include a JavaScript library earlier (in the head scripts), use the theme `custom_dir` and its `libs` block instead (see `theme-custom-dir`).

## Checked

2026-11-04. Confirmed against Customizing Your Theme (Using the docs_dir, Combining the custom_dir and Template Blocks): the `style.css` example, `extra_css`, serve picks up changes, after-content note, and the `libs` block for libraries. Removed: a generic verify line.

Method: documentation only; no commands were run.
