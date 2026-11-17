---
id: computing-software.web-development.htmx.htmx-events-and-debugging
name: htmx-events-and-debugging
category: computing-software
field: web-development
product: htmx
tags: [htmx, events, debugging, logall, logger, request-lifecycle, htmx-load]
level: practitioner
status: docs-checked
description: "Listen to the htmx event system, know the request lifecycle events and their detail fields, and debug with htmx.logAll, logger, monitorEvents and the demo script."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/reference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: hook into and troubleshoot what htmx is doing.

Listening: `document.body.addEventListener('htmx:load', e => ...)` or `htmx.on("htmx:load", fn)`. Every event fires in camelCase and kebab-case (`htmx:afterSwap` and `htmx:after-swap`), which Alpine.js needs. `htmx:load` fires whenever htmx adds content, and once at initialization with `body` as `detail.elt`; `htmx.onLoad(fn)` is the convenience wrapper.

Request-cycle events (list order is not a guaranteed sequence): `htmx:confirm` (can delay/cancel), `htmx:configRequest` (edit `detail.parameters`/`headers`), `htmx:beforeRequest` (cancellable; `detail.boosted`), `htmx:beforeSend` (not cancellable), `htmx:beforeOnLoad` (cancel = no swap), `htmx:beforeSwap` (set `shouldSwap`, `target`, `swapOverride`, `selectOverride`, `isError`), `htmx:afterSwap`, `htmx:afterSettle` (swap before settle), `htmx:afterOnLoad`, `htmx:afterRequest` (`detail.successful`/`failed`, pairs with `beforeRequest`), plus `htmx:xhr:loadstart`/`loadend`/`progress`/`abort`. Common `detail` fields: `elt`, `xhr`, `target`, `requestConfig`.

Error events: `htmx:responseError`, `htmx:sendError`, `htmx:swapError`, `htmx:targetError` (bad selector), `htmx:timeout`, `htmx:onLoadError` (`detail.exception`), `htmx:oobErrorNoTarget`, `htmx:validateUrl` (check `detail.url`, `detail.sameHost`; `preventDefault()` blocks). `htmx:abort` is an event htmx listens for.

Node lifecycle: `htmx:beforeProcessNode`, `htmx:afterProcessNode`, `htmx:beforeCleanupElement`.

Debugging:
- `htmx.logAll()` logs every event; `htmx.logNone()` turns it off.
- Custom: set `htmx.logger` to `function(elt, event, data)` (docs example logs with `console.log`).
- Console only: `monitorEvents(htmx.find("#theElement"))` to learn what events an element fires (cannot be embedded in a page script).
- If stuck, use the unminified `htmx.js` and breakpoints in `issueAjaxRequest()` and `handleAjaxResponse()`.
- Demos: `<script src="https://demo.htmx.org"></script>` loads htmx, hyperscript and a mock server; `<template url="/foo" delay="500">${globalInt++}</template>` defines a mock response (demos only).

## Checked

2026-11-07. Confirmed on events.md (every event named above, its detail fields, cancel behaviour of `beforeRequest`/`beforeOnLoad`/`beforeSwap`/`validateUrl`, `htmx:load` at init with body, `htmx:abort`), docs.md (camelCase and kebab-case names, `htmx.logger`, `htmx.logAll()`, `monitorEvents` console-only, `issueAjaxRequest()`/`handleAjaxResponse()` breakpoints, demo.htmx.org script and `template url delay`) and api.md (`htmx.logNone`, `htmx.on`, `htmx.onLoad`).
Trimmed: the logger line no longer shows a body the docs print differently; the invented Verify step was removed.
Method: documentation only; no commands were run.
