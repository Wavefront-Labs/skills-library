---
id: computing-software.web-development.htmx.htmx-install-and-extensions
name: htmx-install-and-extensions
category: computing-software
field: web-development
product: htmx
tags: [htmx, install, cdn, npm, extensions, hx-ext, data-prefix]
level: intro
status: docs-checked
description: "Load htmx via CDN, download or npm, use the data- prefix, and enable or ignore extensions with hx-ext."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-ext.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get htmx running on a page and turn extensions on where needed.

Install (no build step needed; htmx is dependency-free):
- CDN: `<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.11/dist/htmx.min.js" integrity="..." crossorigin="anonymous"></script>` in `<head>`; `dist/htmx.js` is the unminified build. The docs advise considering not using CDNs in production.
- Download `htmx.min.js` and serve it: `<script src="/path/to/htmx.min.js"></script>`.
- npm: `npm install htmx.org@2.0.11`, then bundle `node_modules/htmx.org/dist/htmx.js` (or `.min.js`).
- Webpack: `import 'htmx.org';` and, to keep the global, `window.htmx = require('htmx.org');` in a custom file imported after it.

Optional prefix: any attribute may be written `data-hx-*`, e.g. `<a data-hx-post="/click">Click Me!</a>`.

Extensions:
- Always load htmx core first, then the extension script, e.g. `https://cdn.jsdelivr.net/npm/htmx-ext-response-targets@2.0.4`. npm name pattern is `htmx-ext-<name>`; Idiomorph is the exception (`idiomorph`, not `htmx-ext-idiomorph`).
- Enable with `hx-ext="name"` on `<body>` or any element; it applies to all children. Comma-separated list: `<body hx-ext="preload,morph">`.
- `hx-ext` is inherited and merged with parents. Opt a subtree out with `hx-ext="ignore:example"`.
- Core extensions: head-support, htmx-1-compat, idiomorph, preload, response-targets, sse, ws.

Extensions are defined in JavaScript and enabled via `hx-ext`; the docs say to enable the extension after loading it, so load the script and also set `hx-ext`.

## Checked

2026-11-07. Confirmed on docs.md (data- prefix, Installing: CDN with integrity and `crossorigin`, unminified build, CDN advice, download, npm, Webpack; Extensions: core list, installing extensions, Idiomorph naming note, enabling extensions) and attributes/hx-ext.md (comma list, inherited and merged, `ignore:`).
Removed: the unconfirmed gotcha wording and the invented Verify step.
Method: documentation only; no commands were run.
