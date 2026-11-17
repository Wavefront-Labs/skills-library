---
id: computing-software.web-development.htmx.htmx-target-selectors
name: htmx-target-selectors
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-target, selectors, closest, find, next, previous, extended-css]
level: practitioner
status: docs-checked
description: "Pick where a response lands with hx-target and htmx extended CSS selectors: this, closest, find, next, previous and the <sel/> query literal."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-target.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-trigger.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: swap the response into an element other than the one that made the request.

`hx-target` values:
- CSS selector: `hx-target="#response-div"`.
- `this` - the element carrying the attribute.
- `closest <sel>` - nearest ancestor-or-self (`closest tr`).
- `find <sel>` - first descendant matching.
- `next` / `previous` - the next/previous sibling element; `next <sel>` / `previous <sel>` scan the document forward/backward for the first match (`next .error`).
- A selector may be wrapped in `<` and `/>` (hyperscript query-literal style), e.g. `<#id/>`.

```html
<button hx-post="/register" hx-target="#response-div" hx-swap="beforeend">Register!</button>
<div id="response-div"></div>
<a hx-post="/new-link" hx-target="this" hx-swap="outerHTML">New link</a>
```

Relative targets avoid peppering the DOM with ids, e.g. `hx-target="closest tr"` in a table row.

Notes:
- `hx-target` is inherited and may sit on a parent.
- The docs say `hx-target` "and most attributes that take a CSS selector" support the extended syntax; for example `from:` in hx-trigger and `<hx-partial hx-target>` are documented as accepting it. Check each attribute's page for its supported subset.
- A bad selector (such as an element id without a preceding `#`) triggers the `htmx:targetError` event.
- A response can override the target with the `HX-Retarget` response header (a CSS selector), and an `htmx:beforeSwap` handler can set `evt.detail.target`.

## Checked

2026-11-07. Confirmed against the hx-target reference (all value forms, both examples, inheritance), the docs Extended CSS Selectors section (including the `<` `/>` query-literal form and relative-target advice), the `<hx-partial>` docs passage, `HX-Retarget`, and the events page (`htmx:targetError`, `htmx:beforeSwap` `detail.target`). Narrowed the "most attributes" note to what the docs and hx-trigger page state, and removed the invented Verify step (including the `htmx.logAll()` tip).
Method: documentation only; no commands were run.
