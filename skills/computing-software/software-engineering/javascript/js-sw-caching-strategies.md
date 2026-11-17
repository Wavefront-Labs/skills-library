---
id: computing-software.software-engineering.javascript.js-sw-caching-strategies
name: js-sw-caching-strategies
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, stale-while-revalidate, js-service-workers]
level: advanced
status: docs-checked
description: "Implement a cache-first service worker with the Cache API (caches.match, cache.put, clone, waitUntil) and know where Workbox and navigation preload fit."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers", "https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage/delete", "https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration", "https://developer.chrome.com/docs/workbox/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service worker caching with the Cache API

- Cache-first (MDN's worked example): in the `fetch` event call `event.respondWith(cacheFirst(event.request, event))`. Look up `caches.match(request)`; if there is a match return it, otherwise `await fetch(request)`, store a clone, and return the original. `caches.match()` resolves to `undefined` when nothing matches, so always provide a fallback.
- Put a clone in the cache: `event.waitUntil(putInCache(request, responseFromNetwork.clone()))`. Streams can be read once, so the original goes to the page and the clone goes to `cache.put()`. Do not await the cache write before responding, but keep the worker alive with `waitUntil`.
- Version your caches (`caches.open("v1")`) and on `activate` delete those not on an allowlist using `caches.keys()` and `caches.delete()`.
- Other strategies (network-first, stale-while-revalidate) are built from the same pieces; the Workbox library from the Chrome team packages common strategies, and its documentation has a guide on navigation preload for network-first HTML (`ServiceWorkerRegistration.navigationPreload`).

Self-check: with the network offline, a previously visited page still loads from the cache.

## Checked

2026-11-03. Confirmed on MDN: Using Service Workers (cache-first code, `caches.match` returning `undefined`, clone and `waitUntil` reasoning), CacheStorage.keys/delete (allowlist cleanup), ServiceWorkerRegistration.navigationPreload property; Workbox landing page (library, navigation preload guide). Removed: the rules "only cache GET, status 200, same-origin or CORS", "never cache authenticated or Set-Cookie responses", the `workbox-routing`/`workbox-strategies` module names and "prefer Workbox over hand-rolled code", and the recommendations for which strategy suits which asset type, none of which is on a page read.
Method: documentation only; no commands were run.
