---
id: computing-software.web-development.htmx.htmx-js-helpers-and-integration
name: htmx-js-helpers-and-integration
category: computing-software
field: web-development
product: htmx
tags: [htmx, javascript-api, onload, process, third-party, alpine, helpers]
level: practitioner
status: docs-checked
description: "htmx helper functions (find, closest, on/off, onLoad, process, class helpers, parseInterval) and integrating 3rd-party libraries, Alpine templates and fetch-inserted HTML."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/api.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use htmx's small helper API and wire libraries into swapped content.

Helpers (all on the global `htmx`):
- `find([elt,] selector)` / `findAll([elt,] selector)` - first/all matches; with `elt`, search inside it (not the root itself). `closest(elt, selector)` includes `elt`.
- `on([target,] event, listener[, options])` returns the listener; `off([target,] event, listener)` removes it. `options` is addEventListener options.
- `onLoad(callback(elt))` - runs for newly loaded content (`htmx:load`).
- `process(elt)` - activate htmx attributes in content you inserted without htmx.
- `addClass(elt, class[, delayMs])`, `removeClass(elt, class[, delayMs])`, `toggleClass(elt, class)`, `takeClass(elt, class)` (only this element keeps the class among its siblings), `remove(elt[, delayMs])`.
- `trigger(elt, name, detail)`, `values(elt[, type])`.
- `parseInterval(str)` - `"3s"` gives 3000; `"3m"` gives 3 (only `s` and `ms` handled; other inputs use `parseFloat`).
- `defineExtension(name, ext)`, `removeExtension(name)`; properties `htmx.config`, `htmx.logger`, `htmx.createEventSource(url)`, `htmx.createWebSocket(url)` (replaceable factories).

Library init pattern: initialize only the newly loaded subtree rather than the whole document.
```js
htmx.onLoad(function(content) {
  content.querySelectorAll(".sortable").forEach(el => new Sortable(el, {animation: 150}));
});
```
(`<form class="sortable" hx-post="/items" hx-trigger="end">` then lets SortableJS's `end` event trigger the request.)

Inserted HTML must be processed:
```js
fetch('/movies').then(r => r.text()).then(html => { myDiv.innerHTML = html; htmx.process(myDiv); });
```
Same for `<template>` content a library adds later (e.g. Alpine `x-if`): call `htmx.process(document.querySelector('#new_content'))` once it is in the DOM.

Pair with scripting tools that fit htmx: vanilla JS event listeners, Alpine.js, jQuery, hyperscript.

## Checked

2026-11-07. Confirmed on api.md (every helper listed, parameter forms, `parseInterval` caution, `values` default, replaceable factories) and docs.md (3rd Party Javascript: SortableJS `onLoad` pattern, `fetch` plus `htmx.process`, Alpine `x-if` template case; scripting options list).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
