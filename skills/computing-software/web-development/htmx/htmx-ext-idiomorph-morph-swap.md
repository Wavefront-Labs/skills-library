---
id: computing-software.web-development.htmx.htmx-ext-idiomorph-morph-swap
name: htmx-ext-idiomorph-morph-swap
category: computing-software
field: web-development
product: htmx
tags: [htmx, extensions, idiomorph, morph, hx-swap, dom-morphing]
level: practitioner
status: docs-checked
description: "Use the idiomorph extension for DOM-morphing swaps in htmx: load idiomorph-ext, enable hx-ext=morph, then hx-swap morph, morph:outerHTML or morph:innerHTML."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/extensions/idiomorph.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: swap new HTML in by morphing the existing DOM into its shape, reusing as many existing nodes as possible, for smoother transitions than a plain replace.

Install: core htmx first, then idiomorph's extension build, then enable it by the name `morph`:

```html
<head>
  <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.11/dist/htmx.min.js"></script>
  <script src="https://unpkg.com/idiomorph@0.7.4/dist/idiomorph-ext.min.js"></script>
</head>
<body hx-ext="morph">
```
Unminified: `https://unpkg.com/idiomorph/dist/idiomorph-ext.js`. npm: `npm install idiomorph`, then bundle `node_modules/idiomorph/dist/idiomorph-ext.js` (or `.min.js`). With a bundler, install `htmx.org` and `idiomorph` and import `htmx.org` and `idiomorph/htmx` in `index.js`. The source page also lists integrity hashes for the CDN tags.

Use: three swap strategies become available.

```html
<body hx-ext="morph">
  <button hx-get="/example" hx-swap="morph">Morph outer</button>
  <button hx-get="/example" hx-swap="morph:outerHTML">Morph outer</button>
  <button hx-get="/example" hx-swap="morph:innerHTML">Morph inner</button>
</body>
```

- `morph` and `morph:outerHTML` morph the target element and its children.
- `morph:innerHTML` morphs only the target's children and leaves the target itself untouched.

Compatibility note from the source: when combined with the SSE extension (htmx-ext-sse), idiomorph requires htmx-ext-sse 2.2.4 or later.

## Checked

2026-11-07. Confirmed on extensions/idiomorph.md (install tags and versions, unminified URL, npm and bundler imports, SSE 2.2.4+ note, `hx-ext="morph"`, the three swap values and their meaning). The general morphing description is on docs.md (Morph Swaps).
Removed: the invented Verify step with its focus-preservation claim; the page only says morphing reuses as much of the existing DOM nodes as possible.
Method: documentation only; no commands were run.
