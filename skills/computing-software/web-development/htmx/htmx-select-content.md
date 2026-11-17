---
id: computing-software.web-development.htmx.htmx-select-content
name: htmx-select-content
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-select, hx-select-oob, response-filtering, reselect]
level: practitioner
status: docs-checked
description: "Swap only part of a response with hx-select and pull extra pieces out of band with hx-select-oob, including per-item swap strategies and HX-Reselect."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-select.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-select-oob.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/api.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/reference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reuse full-page or oversized responses by choosing which elements get swapped.

`hx-select="<CSS selector>"` picks the matching element(s) from the response and swaps only those.
```html
<button hx-get="/info" hx-select="#info-detail" hx-swap="outerHTML">Get Info!</button>
```
This GETs `/info`, takes `#info-detail` and replaces the button with it.

`hx-select-oob` is a comma-separated list of ids/selectors picked from the response and swapped out of band (almost always paired with `hx-select`). Each entry may add a strategy after a colon; the default strategy is `outerHTML`.
```html
<div id="alert"></div>
<button hx-get="/info" hx-select="#info-details" hx-swap="outerHTML"
        hx-select-oob="#alert">Get Info!</button>
<!-- prepend instead of replace -->
<button hx-get="/info" hx-select="#info-details" hx-swap="outerHTML"
        hx-select-oob="#alert:afterbegin">Get Info!</button>
```

Notes:
- Both attributes are inherited. Set `hx-select="unset"` on a child to ignore a parent's `hx-select`.
- A server can override the client with the `HX-Reselect` response header (a CSS selector), which beats `hx-select` on the triggering element.
- Event-time override: set `detail.selectOverride` in `htmx:beforeSwap`; per-status override via the `select` field in `htmx.config.responseHandling` entries.
- Full HTML document responses become useful when combined with `hx-select` (see `htmx-boost-links-and-forms`).
- Programmatic equivalents: `select` and `selectOOB` in `htmx.ajax` context and `htmx.swap` options.

## Checked

2026-11-07. Confirmed against the hx-select and hx-select-oob references (examples, `:afterbegin` strategy, `outerHTML` default, inheritance, `unset`), the reference `HX-Reselect` row, the events page (`detail.selectOverride`), the docs `responseHandling` `select` field and full-document note, and the API page (`select` and `selectOOB` in both the `htmx.ajax` context and `htmx.swap` options; page added to `sources`). Removed the invented Verify step; nothing else needed changing.
Method: documentation only; no commands were run.
