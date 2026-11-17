---
id: computing-software.web-development.htmx.htmx-history-cache-snapshots
name: htmx-history-cache-snapshots
category: computing-software
field: web-development
product: htmx
tags: [htmx, history, hx-history, hx-history-elt, localstorage, beforehistorysave, cache]
level: advanced
status: docs-checked
description: "Manage htmx's localStorage history cache: hx-history false for sensitive pages, hx-history-elt, cache size, cache-miss handling and cleaning 3rd-party DOM before snapshots."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-history.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-history-elt.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make back/forward restore correct, safe and clean.

How it works: when a URL is pushed, htmx snapshots the DOM into a `localStorage` cache. On back, it restores from the cache; on a miss it makes an AJAX request to the URL with the header `HX-History-Restore-Request` set to true and expects a FULL page. Config:
- `htmx.config.historyCacheSize` (default 10; `0` stores nothing).
- `htmx.config.historyEnabled` (default true; mainly for tests).
- `htmx.config.refreshOnHistoryMiss` (default false): if true do a hard browser refresh on a miss.
- `htmx.config.historyRestoreAsHxRequest` (default true): the miss request carries `HX-Request`. Docs say to set it to `false` so `HX-Request` can safely select partial responses.

`hx-history="false"` anywhere in the document (or in an htmx-loaded fragment) keeps the page out of the cache; navigation still works but the URL is fetched from the server. Use it for sensitive data on shared computers; it may be outside the snapshot element.

`hx-history-elt` marks the element to snapshot instead of `body` (not inherited). It must exist on every page or restore is unreliable; usually not recommended.

Cleaning third-party DOM mutations before the snapshot (example TomSelect):
```javascript
htmx.onLoad(t => t.querySelectorAll(".tomselect").forEach(e => new TomSelect(e)));
htmx.on('htmx:beforeHistorySave', () => {
  document.querySelectorAll('.tomSelect').forEach(e => e.tomselect.destroy());
});
```

Events: `htmx:beforeHistorySave` (`detail.path`, `detail.historyElt`), `htmx:historyCacheHit` (can `preventDefault()` for own restore), `htmx:historyCacheMiss`, `htmx:historyCacheMissLoad`, `htmx:historyCacheMissLoadError`, `htmx:historyCacheError` (localStorage write failed), `htmx:historyRestore`.

## Checked

2026-11-07. Confirmed on docs.md (History Support section, TomSelect example, config table defaults for `historyCacheSize`, `historyEnabled`, `refreshOnHistoryMiss`, `historyRestoreAsHxRequest`, `historyCacheSize` 0 in Security), hx-history.md, hx-history-elt.md (not inherited, body default) and events.md (all `htmx:history*` events and `htmx:beforeHistorySave` details).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
