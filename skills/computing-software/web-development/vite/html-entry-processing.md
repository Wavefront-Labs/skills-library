---
id: computing-software.web-development.vite.html-entry-processing
name: html-entry-processing
category: computing-software
field: web-development
product: vite
tags: [html-entry, html-asset-elements, vite-ignore-attribute, project-root]
level: practitioner
status: docs-checked
description: "How Vite treats index.html as source: served paths, which elements get processed and bundled, the vite-ignore opt-out, and URL rebasing."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HTML files in the project root are entry points and part of the module graph. Served paths:
- `<root>/index.html` at `/`
- `<root>/about.html` at `/about.html`
- `<root>/blog/index.html` at `/blog/index.html`

URLs in HTML are rebased automatically, so no `%PUBLIC_URL%` placeholder is needed. Processed and bundled elements include `<script type="module" src>`, `<link href>`, `<img src>` and `srcset`, `<video src>` and `poster`, `<audio>`, `<source>`, `<track>`, `<embed>`, `<object data>`, `<input src>`, `<use href>`, and `<meta content>` for tile images, `twitter:image` and `og:image` family names.

```html
<script type="module" src="/src/main.js"></script>
<img src="/src/images/logo.svg" alt="logo" />
```

Opt out per element with the `vite-ignore` attribute, useful for external assets or a CDN.

Absolute URLs in source resolve against the project root.

## Checked

2026-11-07. Confirmed against the "HTML" section of guide/features.md (read in full, including the Dynamic Import, Glob Import, JSON, JSX, HTML and TypeScript sections) and the "index.html and Project Root" section of guide/index.md (read in full): served paths, the processed element list including the `<meta content>` name and property rules, `vite-ignore`, no `%PUBLIC_URL%` placeholder, and absolute URLs resolving against the root. Nothing removed.

Method: documentation only; no commands were run.
