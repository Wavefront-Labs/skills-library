---
id: computing-software.web-development.htmx.htmx-ext-preload
name: htmx-ext-preload
category: computing-software
field: web-development
product: htmx
tags: [htmx, extensions, preload, performance, hx-get, cache]
level: practitioner
status: docs-checked
description: "Preload GET links and hx-get elements with the htmx preload extension: preload attribute, mousedown/mouseover/custom-event/always triggers, forms, images, limits, HX-Preloaded."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/extensions/preload.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: fetch likely next pages early so navigation feels instant. Use sparingly: too many preloads waste user bandwidth and server capacity.

Install: core htmx first, then `https://cdn.jsdelivr.net/npm/htmx-ext-preload@2.1.2`, then `<body hx-ext="preload">` (npm: `htmx-ext-preload`, bundle `dist/preload.js`).

Mark what to preload with the `preload` attribute on links and `hx-get` elements:

```html
<body hx-ext="preload">
  <a href="/server/1" preload>requested with a standard XMLHttpRequest</a>
  <button hx-get="/server/2" preload>requested with additional htmx headers</button>
  <a href="/server/3">NOT preloaded: no preload attribute</a>
  <a hx-post="/server/4" preload>NOT preloaded: it is a POST</a>
</body>
```
Every preload request carries the request header `HX-Preloaded` with value `true`. `preload` on a container (for example `<ul preload>`) covers all links and `hx-get` elements inside it; be careful about wasted bandwidth.

When it fires (value of `preload`)
- `mousedown` (default): starts on mouse down, a 100-200 ms head start over the click completing.
- `mouseover`: starts after the pointer rests 100 ms on the element; leaving earlier cancels it. More server load.
- a custom event name, such as `preload="preload:init"`; the extension itself emits `preload:init` once htmx has processed the element, so content preloads as soon as the page is ready.
- `always`: by default each element preloads once; `always` repeats it (useful when `hx-target` is not the element itself). Combine like `preload="always mouseover"`.
- For `mouseover` and `mousedown`, an `ontouchstart` handler is added that fires immediately on touch.

Forms. A form with `hx-get` or `method="get"` can preload via `preload` on the form or its inputs: radio and checkbox (as if toggled and submitted), `select` (one request per unselected option), and submit inputs.

Images: `<a href="/my-next-page" preload="mouseover" preload-images="true">` also preloads linked images. JavaScript and CSS (linked or embedded) are never loaded or run.

Limits
- Only GET is preloaded; POST, PUT and DELETE never are.
- The browser caches a preloaded response only if headers allow it: `Cache-Control: private, max-age=60` yes, `Cache-Control: no-cache` no.

## Checked

2026-11-07. Confirmed on extensions/preload.md (install, `preload` attribute, what does and does not preload, `HX-Preloaded` header, container inheritance, `mousedown` default with 100-200ms head start, `mouseover` with 100ms delay, `preload:init`, `always`, touch handler, form element rules, `preload-images`, GET-only, Cache-Control examples).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
