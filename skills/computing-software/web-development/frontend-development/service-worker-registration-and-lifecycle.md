---
id: computing-software.web-development.frontend-development.service-worker-registration-and-lifecycle
name: service-worker-registration-and-lifecycle
category: computing-software
field: web-development
product: frontend-development
tags: [progressive-web-app, pwa, service-worker-lifecycle, service-worker-registration, service-worker-scope, clients-claim, install-event, activate-event]
level: practitioner
status: docs-checked
description: "Registering a service worker safely and understanding install/waiting/activate, scope, clients.claim and why updates appear stuck."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Service-Worker-Allowed
  - https://developer.chrome.com/docs/workbox/service-worker-lifecycle
  - https://developer.chrome.com/docs/workbox/remove-buggy-service-workers
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service worker registration and lifecycle

**Goal:** register a service worker that installs predictably, controls the right URLs, and never leaves users stuck on an old version.

## 1. Register after load
```js
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .catch(err => console.error('SW registration failed', err));
  });
}
```
Registering after `load` is a common choice so that precaching does not compete with first-visit resources.

## 2. Scope
Default scope is the directory of the script: `/assets/sw.js` controls `/assets/` by default. Serve it from the root, or send a `Service-Worker-Allowed` header on the script response to broaden the scope (MDN). Service workers require a secure context (HTTPS; localhost is allowed for development).

## 3. The lifecycle
1. **install** - precache the shell. `event.waitUntil(promise)`; if the promise rejects, the SW is discarded.
2. **waiting** - a new SW waits while pages are still controlled by the old one; call `skipWaiting()` to activate without waiting (MDN).
3. **activate** - delete old caches here. On first install the worker activates without waiting, but existing documents are not controlled until reloaded; `clients.claim()` takes control of them immediately (MDN).
```js
const CACHE = 'shell-v42';
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(['/', '/app.css', '/app.js']))));
self.addEventListener('activate', e => e.waitUntil((async () => {
  for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
  await self.clients.claim();
})()));
```

## 4. Update checks
The browser re-fetches the worker script on navigations within scope and on `registration.update()`; the Workbox lifecycle guide mentions an update check when a functional event has not been checked in the last 24 hours. A byte-for-byte difference starts a new install, and scripts pulled in with `importScripts` are checked too. Browsers have safeguards against the HTTP cache serving a stale worker script (Workbox, remove-buggy-service-workers), but keep `sw.js` on a short `Cache-Control` lifetime anyway.

## 5. Killing a bad service worker
Workbox's guide says to deploy a no-op worker at the **same URL** that calls `skipWaiting()` on install, has no `fetch` handler and optionally reloads open windows. A more aggressive variant also deletes caches and unregisters:
```js
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', async () => {
  for (const k of await caches.keys()) await caches.delete(k);
  await self.registration.unregister();
  for (const c of await self.clients.matchAll()) c.navigate(c.url);
});
```
Optionally also send the response header `Clear-Site-Data: "storage"`: MDN says it unregisters service worker registrations and clears all other DOM storage for the origin, and Workbox warns it is not supported everywhere, so treat it as an addition to the no-op worker. Never change the SW URL to escape a bad worker: Workbox warns that the old worker stays active alongside the new one.

## Verify
- [ ] DevTools > Application > Service Workers shows one active SW with expected scope.
- [ ] Deploying a change shows a waiting worker; your update flow activates it.
- [ ] `chrome://serviceworker-internals` shows no stale registrations on other paths.

## Checked
Checked 2026-10-26 against MDN Using Service Workers (lifecycle, skipWaiting, clients.claim, default scope and Service-Worker-Allowed, secure context), the Workbox guides service-worker-lifecycle (24 hours, importScripts) and remove-buggy-service-workers (same-URL no-op worker, no fetch handler, Clear-Site-Data storage caveats) and MDN Clear-Site-Data (storage unregisters registrations). The chrome://serviceworker-internals page in the Verify list is confirmed by the Chrome DevTools service worker docs. Removed the unconfirmed claim that reloading a single tab never releases a waiting worker. Code was not run.

Method: documentation only; no commands were run.
