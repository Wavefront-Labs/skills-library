---
id: computing-software.web-development.htmx.htmx-response-status-handling
name: htmx-response-status-handling
category: computing-software
field: web-development
product: htmx
tags: [htmx, responsehandling, status-codes, 422, 204, beforeswap, errors]
level: practitioner
status: docs-checked
description: "Decide which HTTP status codes htmx swaps or treats as errors: htmx.config.responseHandling rules, 204/422 patterns, htmx:beforeSwap and error events."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: swap validation-error HTML (e.g. 422) or handle failures instead of htmx silently ignoring them.

Defaults: `204 No Content` does nothing and is not an error; 2xx/3xx are swapped; 4xx/5xx are not swapped and count as errors (fires `htmx:responseError`); a connection failure fires `htmx:sendError`.

`htmx.config.responseHandling` is an ordered array; the first entry whose `code` (a string treated as a regular expression) matches the status wins:
```js
responseHandling: [
  {code:"204", swap: false},
  {code:"[23]..", swap: true},
  {code:"[45]..", swap: false, error:true},
  {code:"...", swap: false}
]
```
Entry fields: `code`, `swap` (bool), `error` (bool), `ignoreTitle`, `select` (CSS selector into the response), `target` (alternate target selector), `swapOverride` (alternate swap style).

Swap 422 too, via the meta tag:
```html
<meta name="htmx-config" content='{"responseHandling":[
  {"code":"204","swap":false},{"code":"[23]..","swap":true},{"code":"422","swap":true},
  {"code":"[45]..","swap":false,"error":true},{"code":"...","swap":true}]}' />
```
Swap everything: `{"responseHandling":[{"code":".*","swap":true}]}`.

Per-event alternative: in `htmx:beforeSwap` set `detail.shouldSwap`, `detail.isError` (false avoids console error logging), `detail.target`, `detail.selectOverride`, `detail.swapOverride`, `detail.ignoreTitle`; `preventDefault()` cancels the swap.
```javascript
document.body.addEventListener('htmx:beforeSwap', e => {
  if (e.detail.xhr.status === 422) { e.detail.shouldSwap = true; e.detail.isError = false; }
  else if (e.detail.xhr.status === 418) { e.detail.shouldSwap = true; e.detail.target = htmx.find("#teapot"); }
});
```
Declarative alternative: the response-targets extension (`hx-target-404="#not-found"` with `hx-ext="response-targets"`).

Related events: `htmx:afterRequest` has `detail.successful` / `detail.failed`; `htmx:swapError`, `htmx:timeout`.

## Checked

2026-11-07. Confirmed against the htmx docs (Requests and Responses, Configuring Response Handling, examples, beforeSwap and response-targets passages) and the events page (`htmx:beforeSwap` details, `detail.successful`/`detail.failed`, `htmx:swapError`, `htmx:timeout`). Removed the invented Verify step; nothing else needed changing.
Method: documentation only; no commands were run.
