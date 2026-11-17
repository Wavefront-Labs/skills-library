---
id: computing-software.web-development.frontend-development.offline-fallback-and-offline-ux
name: offline-fallback-and-offline-ux
category: computing-software
field: web-development
product: frontend-development
tags: [progressive-web-app, pwa, offline-fallback, offline-first, navigator-online, offline-page, sync-queue, optimistic-ui]
level: practitioner
status: docs-checked
description: "Designing offline behaviour: offline fallback page, online/offline detection limits, queuing writes, and telling users what state their data is in."
sources:
  - https://developer.chrome.com/docs/workbox/managing-fallback-responses
  - https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine
  - https://developer.mozilla.org/en-US/docs/Web/API/NavigationPreloadManager
  - https://developer.mozilla.org/en-US/docs/Web/API/FetchEvent/preloadResponse
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline fallback and offline UX

**Goal:** when the network fails users see something useful and never lose what they typed.

## 1. Levels of offline support
1. **Offline page**: precache `/offline.html` (inline its CSS/images); serve it when a navigation fetch fails.
2. **Read offline**: previously visited pages/data served from cache or IndexedDB.
3. **Write offline (offline-first)**: user actions go into a local queue (IndexedDB), UI updates optimistically, a sync process sends them when online.

## 2. Fallback page in the SW
```js
self.addEventListener('install', e => e.waitUntil(caches.open('offline').then(c => c.add('/offline.html'))));
self.addEventListener('fetch', e => {
  if (e.request.mode !== 'navigate') return;
  e.respondWith(fetch(e.request).catch(() => caches.match('/offline.html')));
});
```
With navigation preload enabled (`registration.navigationPreload.enable()`), use `await e.preloadResponse` before `fetch` to avoid the SW boot delay.

## 3. Detecting connectivity honestly
MDN: `navigator.onLine` is `false` when the browser is offline, but browsers use differing heuristics and a connection to a LAN counts as online even without Internet access, so `true` is not proof. Treat failed requests as the real signal: on fetch failure mark the app offline and retry with backoff; on the `online` event try a lightweight request.

## 4. Queueing writes
- Store each pending mutation in IndexedDB with a client-generated id (UUID) so retries are idempotent on the server.
- Replay on `online`, on app start, and via Background Sync where supported.
- Show state per item: "Saved", "Waiting to sync", "Failed - retry". Never show a spinner forever.
- Conflicts: decide a rule (last-write-wins with server timestamp, or surface a merge UI); document it.

## 5. UX rules
- Offline banner is non-blocking and uses `role="status"`.
- Disable actions that truly need the network (payments) with an explanation, rather than letting them fail.
- Keep form drafts in storage so a reload doesn't lose input.

## Verify
- [ ] DevTools Offline: navigation to an uncached page shows the offline page, not the dino.
- [ ] Create items offline, reload, go online: all sync once, no duplicates.
- [ ] Captive-portal simulation (block API host only) triggers the offline state.

## Checked
Checked 2026-10-26 against MDN Navigator.onLine (differing heuristics, LAN counts as online), NavigationPreloadManager and FetchEvent.preloadResponse, and the Workbox managing-fallback-responses guide. The remaining text is design guidance with no version-specific or numeric claims; the snippets were not run.

Method: documentation only; no commands were run.
