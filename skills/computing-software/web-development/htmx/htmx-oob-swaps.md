---
id: computing-software.web-development.htmx.htmx-oob-swaps
name: htmx-oob-swaps
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-swap-oob, out-of-band, template, svg, tables, nested-oob]
level: practitioner
status: docs-checked
description: "Update several page regions from one response with hx-swap-oob: values, selector targets, wrapping tags for tables, template and svg tricks, nested OOB config."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-swap-oob.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: piggy-back extra updates on a response so elements elsewhere in the page change too.

Put `hx-swap-oob` on top-level elements in the response. The main content swaps into the target normally; OOB elements swap into the matching element and do not land in the target.

```html
<div>main content ...</div>
<div id="alerts" hx-swap-oob="true">Saved!</div>
```

Value of `hx-swap-oob`: `true` (same as `outerHTML`, matched by id), any `hx-swap` value, or `<swap>:<CSS selector>`. With a selector all matching elements swap; without one the element with the same id is used. For any strategy other than `outerHTML`, the wrapper tag is stripped, so wrap the payload in a tag valid for the context:
```html
<tbody hx-swap-oob="beforeend:#table tbody"><tr>...</tr></tbody>
<ul hx-swap-oob="beforeend:#list1"><li>...</li></ul>
<span hx-swap-oob="beforeend:#text"><p>...</p></span>
```

Troublesome elements (`tr`, `td`, `th`, `thead`, `tbody`, `tfoot`, `colgroup`, `caption`, `col`, `li`) cannot stand alone in HTML; wrap in `<template>` (removed after processing):
```html
<template><tr id="row" hx-swap-oob="true">...</tr></template>
```
SVG children need `<template><svg>...</svg></template>` so the namespace applies, e.g. `<template><svg hx-swap-oob="beforebegin:#circle1">...</svg></template>`.

Nested OOB: by default any `hx-swap-oob` element anywhere in the response is processed, even inside the main element (which removes it from the DOM there). Set `htmx.config.allowNestedOobSwaps=false` to process only elements adjacent to the main response element.

Notes: `hx-swap-oob` is not inherited. An OOB swap with no matching element in the DOM fires `htmx:oobErrorNoTarget`; use `htmx:oobBeforeSwap` / `htmx:oobAfterSwap` to adjust. Compare `htmx-partial-swap-commands`.

## Checked

2026-11-07. Confirmed on attributes/hx-swap-oob.md (values, selector rule, tag stripping, table/list/p wrappers, template and SVG sections, nested OOB config, not inherited), docs.md (Out of Band Swaps, `allowNestedOobSwaps` default true) and events.md (`htmx:oobBeforeSwap`, `htmx:oobAfterSwap`, `htmx:oobErrorNoTarget`).
Fixed: the missing-target wording now matches events.md. Removed the invented Verify step.
Method: documentation only; no commands were run.
