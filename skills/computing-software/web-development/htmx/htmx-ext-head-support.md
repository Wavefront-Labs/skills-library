---
id: computing-software.web-development.htmx.htmx-ext-head-support
name: htmx-ext-head-support
category: computing-software
field: web-development
product: htmx
tags: [htmx, extensions, head-support, head, hx-boost, hx-head, merge]
level: practitioner
status: docs-checked
description: "Merge or append head tag content from htmx responses with the head-support extension: hx-ext setup, boosted merge rules, hx-head modes, re-eval, preserve, and events."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/extensions/head-support.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let htmx responses update `<head>` (styles, scripts) as well as body content.

Install: load core htmx first, then the extension, then enable it:

```html
<head>
  <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.11/dist/htmx.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/htmx-ext-head-support@2.0.5"></script>
</head>
<body hx-ext="head-support">
```
(npm: `npm install htmx-ext-head-support`, then bundle `node_modules/htmx-ext-head-support/dist/head-support.js`.) The page also gives integrity hashes; add them from the source in production.

Behaviour. Any response containing a `head` tag is processed, even if it is not a full document with an `<html>` root.
- Request from a boosted element: merge. Exact textual matches stay; new elements are added at the end of head; elements in the current head but not in the new head are removed.
- Request from a non-boosted element: all content is appended to the existing head.
- Override per response with `hx-head` on the new `<head>` tag: `hx-head="merge"` or `hx-head="append"`.

Per-element control
- `hx-head="re-eval"` on a head element: removed and re-appended on every request even if present (for example to run a script each time).
- `hx-preserve="true"` on a head element: it is never removed.

Example. Current head has `site1.css`, `script1.js`, `script2.js` plus `https://the.missing.style`; the response head has `site2.css`, `script2.js`, `script3.js` plus the same missing.style link. Result: missing.style and script2.js are left alone, site1.css and script1.js removed, site2.css and script3.js added (final order: missing.style, script2.js, site2.css, script3.js).

Events (cancelable ones use `preventDefault()`)
- `htmx:beforeHeadMerge` before a merge.
- `htmx:removingHeadElement` and `htmx:addingHeadElement`, with `event.detail.headElement`; cancelling stops that removal or addition.
- `htmx:afterHeadMerge`, with `event.detail.added`, `kept` and `removed`.

## Checked

2026-11-07. Confirmed on extensions/head-support.md (install, `hx-ext="head-support"`, boosted merge vs non-boosted append, `hx-head` merge/append/re-eval, `hx-preserve="true"`, worked example and final order, the four events and `detail.headElement` / `added` / `kept` / `removed`).
Removed: the invented Verify step. Nothing else needed changing.
Method: documentation only; no commands were run.
