---
id: computing-software.web-development.htmx.htmx-js-ajax-and-swap
name: htmx-js-ajax-and-swap
category: computing-software
field: web-development
product: htmx
tags: [htmx, javascript-api, htmx-ajax, htmx-swap, programmatic, promise]
level: advanced
status: docs-checked
description: "Drive htmx from JavaScript: htmx.ajax signatures and context options, htmx.swap swapSpec and swapOptions, and the HX-Location context mapping."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/api.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/headers/hx-location.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: issue htmx-style requests and swaps from scripts.

`htmx.ajax(verb, path, target)` returns a Promise that resolves after the content is inserted (after `htmx:afterOnLoad`, before `htmx:xhr:loadend`). Forms:
- `htmx.ajax('GET', '/example', '#myDiv')` - third arg a selector or element (default target `body`).
- `htmx.ajax('GET', '/example', {target:'#myDiv', swap:'outerHTML'})` - context object.
```js
htmx.ajax('GET', '/example', '#myDiv').then(() => console.log('Content inserted successfully!'));
```
Context keys: `source` (element whose `hx-*` attributes, with ancestors, apply), `event`, `handler` (callback receiving the response HTML), `target`, `swap`, `values`, `headers`, `select`, `selectOOB`, `push` (`'true'` or a path), `replace` (`'true'` or a path). The `HX-Location` response header JSON requires `path` and the rest of its data mirrors this context; that page lists `source` through `select`, `push` and `replace` but not `selectOOB`, and describes `push` as `'false'` or a path (here it is `'true'` or a path).

`htmx.swap(target, content, swapSpec, swapOptions)` swaps and settles HTML you already have:
```js
htmx.swap("#output", "<div>Swapped!</div>", {swapStyle: 'innerHTML'});
```
- `target`: element or selector. `content`: HTML string.
- `swapSpec`: `swapStyle` (required), `swapDelay`, `settleDelay`, `transition`, `ignoreTitle`, `head` (`merge` or `append`; empty disables head handling), `scroll`, `scrollTarget`, `show`, `showTarget`, `focusScroll`.
- `swapOptions` (optional): `select`, `selectOOB`, `eventInfo` (attached to `htmx:afterSwap`/`htmx:afterSettle`), `anchor`, `contextElement` (used to find extensions enabled for that element), `afterSwapCallback`, `afterSettleCallback` (no args).

Related: `htmx.trigger(elt, name, detail)` triggers an event on an element. `htmx.values(elt, type)` returns the values htmx would send (non-GET includes the enclosing form; default `post`).

## Checked

2026-11-07. Confirmed on api.md (`htmx.ajax` forms, context keys, Promise timing example, `htmx.swap` parameters and example, `htmx.trigger`, `htmx.values`) and headers/hx-location.md (path required, context mirror list).
Fixed: the HX-Location mapping sentence now states the differences the page shows; removed the unconfirmed claim that `htmx.trigger` can start a request and the invented Verify step.
Method: documentation only; no commands were run.
