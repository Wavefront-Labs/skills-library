---
id: computing-software.web-development.htmx.htmx-polling-and-lazy-loading
name: htmx-polling-and-lazy-loading
category: computing-software
field: web-development
product: htmx
tags: [htmx, polling, load-polling, lazy-loading, revealed, intersect, hx-trigger]
level: practitioner
status: docs-checked
description: "Poll with hx-trigger every N, stop with HTTP 286, load-poll with load delay, and lazy-load using load, revealed and intersect options."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-trigger.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: refresh content on a timer or fetch it when it appears.

Polling: `every <timing>`.
```html
<div hx-get="/news" hx-trigger="every 2s"></div>
```
- To stop polling from the server, respond with HTTP status `286`; the element cancels polling.
- A filter goes after the poll declaration, e.g. only when the tab is visible: `hx-trigger="every 1s [!document.hidden]"`.

Load polling: trigger once on `load` with a delay and replace yourself with the response; if the endpoint keeps returning the same element, it keeps polling every second (useful where polling terminates at an end point, such as a progress bar).
```html
<div hx-get="/messages" hx-trigger="load delay:1s" hx-swap="outerHTML"></div>
```

Special events (non-standard):
- `load` - fires when the element is loaded (lazy-load content on page load).
- `revealed` - fires when the element scrolls into the viewport. If the element sits in a scroll container using CSS `overflow` (e.g. `overflow-y: scroll`), use `intersect once` instead.
- `intersect` - fires once when the element first intersects the viewport; options `root:<selector>` and `threshold:<float 0.0-1.0>`.

```html
<div hx-get="/more" hx-trigger="revealed" hx-swap="outerHTML">Loading...</div>
<div hx-get="/chart" hx-trigger="intersect once threshold:0.5"></div>
```

## Checked

2026-11-07. Confirmed against the htmx docs (Polling, Load Polling, the 286 stop code) and the hx-trigger reference (`every`, filter after the poll declaration, `load`, `revealed`, `intersect` with `root` and `threshold`, `intersect once` for `overflow`). Removed an unsourced swap-style gotcha and the invented Verify step.
Method: documentation only; no commands were run.
