---
id: computing-software.web-development.frontend-development.background-sync
name: background-sync
category: computing-software
field: web-development
product: frontend-development
tags: [progressive-web-app, pwa, background-sync, periodic-background-sync, sync-event, offline-queue, workbox-background-sync]
level: practitioner
status: docs-checked
description: "Retrying failed requests with the Background Sync API (and Workbox queue), periodic sync limits, and fallbacks for browsers without it."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Periodic_Background_Synchronization_API
  - https://developer.chrome.com/docs/workbox/retrying-requests-when-back-online
  - https://github.com/WICG/background-sync
  - https://github.com/mdn/browser-compat-data/blob/main/api/SyncManager.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Background Sync

**Goal:** writes made while offline are delivered once connectivity returns, even if the user closed the tab.

## 1. Support reality
MDN browser-compat data lists `SyncManager` (Background Sync) as Chrome 49 onwards and `PeriodicSyncManager` as Chrome 80 onwards, with no Firefox or Safari support, and both pages mark them as limited availability. Keep an in-page retry path (on `online`, on app start).

## 2. One-off sync
```js
// page: save to IndexedDB outbox, then register a sync
await outbox.add({ id: crypto.randomUUID(), url: '/api/notes', body });
const reg = await navigator.serviceWorker.ready;
if ('sync' in reg) await reg.sync.register('flush-outbox');
else flushOutbox();                       // fallback in page

// sw.js
self.addEventListener('sync', (e) => {
  if (e.tag === 'flush-outbox') e.waitUntil(flushOutbox());
});
async function flushOutbox() {
  for (const item of await outbox.all()) {
    const res = await fetch(item.url, { method: 'POST', body: JSON.stringify(item.body),
      headers: { 'Content-Type': 'application/json', 'Idempotency-Key': item.id } });
    if (res.ok || (res.status >= 400 && res.status < 500)) await outbox.delete(item.id);  // 4xx won't succeed on retry
    else throw new Error('retry later');   // rejecting makes the browser retry with backoff
  }
}
```
Rejecting the `waitUntil` promise tells the browser the sync failed so it can retry; `SyncEvent.lastChance` is true on the final attempt (WICG spec), and retry timing is up to the browser. Have the server honour the idempotency key you send, so a retry after a lost response doesn't duplicate.

## 3. Workbox shortcut
```js
import { BackgroundSyncPlugin } from 'workbox-background-sync';
registerRoute(/\/api\/notes/, new NetworkOnly({ plugins: [new BackgroundSyncPlugin('notes', { maxRetentionTime: 24 * 60 })] }), 'POST');
```
Workbox stores failed requests in IndexedDB and replays them on a `sync` event. It hooks the plugin's fetch-failed callback, so only network failures are queued (not HTTP error responses), and `maxRetentionTime` is in minutes. Where Background Sync is unavailable, Workbox's queue falls back to replaying when the service worker starts.

## 4. Periodic sync
`reg.periodicSync.register('refresh-feed', { minInterval: 24*60*60*1000 })` - controlled by the `periodic-background-sync` permission; in Chrome it is granted only to an installed web app launched as a separate application, and Chrome uses the site's engagement score to decide whether and how often the event fires. `minInterval` is a minimum; treat it as best-effort content refresh.

## Verify
- [ ] Go offline, submit, close the tab, go online: request arrives at the server (Chrome).
- [ ] DevTools > Application > Service Workers has a Sync button that fires a sync event for a tag.
- [ ] Browsers without Background Sync: the in-page fallback delivers when the app is next opened.

## Checked
Checked 2026-10-26 against MDN (Background Synchronization API, PeriodicSyncManager, Web Periodic Background Synchronization API: permission, installed app, engagement score), MDN browser-compat data, the WICG background-sync spec (SyncEvent.lastChance), the Workbox guide retrying-requests-when-back-online (network-failure only, maxRetentionTime minutes) and Chrome DevTools service worker docs (Sync button). Removed unconfirmed claims: 'Chrome gives up after a few attempts', 'replays on SW start in other browsers' stated as fact beyond the documented fallback, and the Application > Background services panel. Code was not run.

Method: documentation only; no commands were run.
