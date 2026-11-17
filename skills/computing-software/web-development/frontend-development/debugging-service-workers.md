---
id: computing-software.web-development.frontend-development.debugging-service-workers
name: debugging-service-workers
category: computing-software
field: web-development
product: frontend-development
tags: [service-worker-debugging, devtools-application-panel, clear-site-data, sw-kill-switch, pwa]
level: practitioner
status: docs-checked
description: "Debugging service workers: DevTools Application panel controls, stuck waiting workers, stale caches, unregistering, Clear-Site-Data kill switches and per-browser tools."
sources:
  - https://developer.chrome.com/docs/devtools/progressive-web-apps
  - https://developer.chrome.com/docs/workbox/remove-buggy-service-workers
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data
  - https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging service workers

## 1. DevTools controls (Chrome > Application > Service workers)
- **Update on reload**: forces the worker to update on every reload (dev only).
- **Bypass for network**: requests skip the SW (but it stays registered).
- **Offline**: puts DevTools into offline mode.
- **skipWaiting** link on a waiting worker; **Unregister**; the **Push** button emulates a push without a payload and **Sync** emulates a background sync event.
- Cache Storage and IndexedDB views to inspect and delete entries; the Clear storage pane can unregister a service worker and wipe storage and caches in one click.
- Chrome: "See all registrations" opens `chrome://serviceworker-internals` for all origins.

## 2. Common symptoms
| Symptom | Cause | Fix |
|---|---|---|
| New deploy not showing | new SW waiting while any tab uses the old one | update prompt + `skipWaiting`, or close all tabs |
| Old HTML served forever | cache-first for navigations; precache not revisioned | network-first for HTML; hashed precache entries |
| SW not controlling page | first load (not yet claimed) or scope too narrow | `clients.claim()`; serve SW from root or `Service-Worker-Allowed` header |
| Fetch handler errors = blank page | `respondWith` rejected | always fall back to `fetch(event.request)` in a catch |

## 3. Kill switch for a broken SW in production
Ship a replacement at the **same URL** (Workbox warns a different URL leaves the buggy worker active). Workbox's own recommended version is a no-op worker with no `fetch` handler; this variant also unregisters:
```js
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", async () => {
  await self.registration.unregister();
  for (const k of await caches.keys()) await caches.delete(k);
  for (const c of await self.clients.matchAll()) c.navigate(c.url);
});
```
Or send the response header `Clear-Site-Data: "storage"` (MDN: it unregisters service worker registrations and clears localStorage, sessionStorage, IndexedDB and other DOM storage; Workbox notes it is not supported in all browsers and recommends it only in addition to the no-op worker). Keep `sw.js` on a short `Cache-Control` lifetime so the fix is picked up.

## 4. Logging
Workbox logs to the console in development builds; the service worker has its own DevTools console. Add a version constant and post it to pages to see which SW is running.

## Verify
- [ ] Deploy a change; the update prompt appears and reloading shows the new version without closing tabs.

## Checked
Checked 2026-10-26 against the Chrome DevTools progressive web apps docs (Update on reload, Bypass for network, Offline, Push without payload, Sync, Unregister, Clear storage, See all registrations), the Workbox remove-buggy-service-workers guide and MDN Clear-Site-Data. Removed unconfirmed items: Firefox and Safari debugging paths, the Chrome-versus-Safari troubleshooting row, the Shift+Reload remark and the 24 hour HTTP-cache sentence. Code was not run.

Method: documentation only; no commands were run.
