---
id: computing-software.software-engineering.javascript.js-service-workers-and-caching
name: js-service-workers-and-caching
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-service-workers, cache-api, offline-first, pwa, workbox]
level: advanced
status: docs-checked
description: "Register service workers, understand install, waiting and activate, and cache with the Cache API: cache-first, clone before put, delete old caches."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers", "https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage/delete", "https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage/keys", "https://developer.mozilla.org/en-US/docs/Web/API/Cache/addAll", "https://developer.chrome.com/docs/workbox/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service workers

- Service workers need HTTPS; browsers treat `localhost` as a secure origin. `navigator.serviceWorker.register("/sw.js", { scope: "/" })`: the default scope is the directory holding the script (a worker at `/js/sw.js` controls `/js/` and below), and the `Service-Worker-Allowed` header can broaden or narrow it. One worker serves many pages, so be careful with global variables.
- Lifecycle: `install` is always first (precache with `event.waitUntil(cache.addAll(urls))`; a rejected promise fails installation). An updated worker installs while the old one keeps controlling pages, then waits; when old pages close it receives `activate`, which is the place to clean up old caches. `skipWaiting()` makes it activate at once and take over old pages; `clients.claim()` adopts already-open pages, which otherwise stay uncontrolled until reload.
- Serving: the `fetch` event fires for every resource in scope; `event.respondWith(...)` supplies the response. Cache-first: `caches.match(request)`, fall back to `fetch(request)`.
- Request and response bodies can be read once, so put a clone into the cache and return the original: `event.waitUntil(cache.put(request, response.clone()))`. Use `waitUntil` so the worker is not terminated before the cache is filled.
- Cache hygiene: name caches with a version (`"v1"`), and on `activate` list `caches.keys()` and `caches.delete(name)` for any not on an allowlist.
- Workbox is the Chrome team's service worker library, if you prefer not to hand-write strategies.

## Checked

2026-11-03. Confirmed on MDN: Using Service Workers (HTTPS and localhost, scope default and `Service-Worker-Allowed`, install and waitUntil, waiting, activate, skipWaiting, clients.claim, respondWith, cache-first, clone for single-read streams), CacheStorage.delete and keys (old-cache cleanup), Cache.addAll; Workbox landing page. Removed: stale-while-revalidate and network-first rules, "do not cache POST or opaque responses", the `Cache-Control: no-cache` header advice, DevTools "Update on reload" tips, and the preference to prompt users to reload (not on a page read).
Method: documentation only; no commands were run.
