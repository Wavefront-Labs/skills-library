---
id: computing-software.web-development.frontend-development.storage-quota-and-persistence
name: storage-quota-and-persistence
category: computing-software
field: web-development
product: frontend-development
tags: [client-side-storage, storage-quota, storage-persistence, navigator-storage-estimate, storage-persist, eviction, clear-site-data]
level: practitioner
status: docs-checked
description: "Checking storage quota with navigator.storage.estimate, requesting persistent storage, understanding eviction per browser and clearing site data."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria
  - https://web.dev/articles/storage-for-the-web
  - https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage quota and persistence

**Goal:** know how much an origin can store, keep important offline data from being evicted, and handle quota errors.

## 1. How much is available
```js
const { usage, quota } = await navigator.storage.estimate();
console.log(`${(usage/1e6).toFixed(1)} MB of ${(quota/1e6).toFixed(0)} MB`);
```
IndexedDB, the Cache API and OPFS are governed by a browser-specific storage management system; Web Storage has its own limit of about 5 MiB per storage type. Per MDN (checked 2026-10-26): Chromium browsers allow an origin up to 60% of total disk size; Firefox allows the smaller of 10% of disk or a 10 GiB group limit in best-effort mode (up to 50% of disk, capped at 8 TiB, once persistent); Safari on macOS 14 / iOS 17 and later allows around 60% of disk for browser apps and around 15% for embedded WebViews. Limits are computed from total disk size and may vary to avoid fingerprinting, and `estimate()` returns estimates only - always handle `QuotaExceededError`.

## 2. Best-effort vs persistent
By default storage is **best-effort**: the browser may evict whole origins (least recently used) under disk pressure. Ask for persistence when the data is the user's work:
```js
if (navigator.storage?.persist && !(await navigator.storage.persisted())) {
  const granted = await navigator.storage.persist();
}
```
Safari and most Chromium-based browsers approve or deny automatically from the user's history of interaction with the site (no prompt); Firefox shows a prompt. Persistent data is evicted only if the user chooses to delete it. `persist()` is not available in Web Workers.

## 3. Eviction is all-or-nothing per origin
When a browser evicts, it deletes all of an origin's data, not parts of it, so your IndexedDB and caches vanish together. Triggers are storage pressure (least recently used origin first, skipping persistent origins), the browser exceeding its overall maximum, and, only in Safari, proactive deletion after seven days of browser use without user interaction. Design: server is source of truth, client storage is a cache plus an outbox that is flushed promptly.

## 4. Handling full storage
Wrap writes to IndexedDB, Cache and OPFS in try/catch for `QuotaExceededError`; free space by deleting your own oldest cached content before storing new data, retry once, and tell the user if offline content can't be saved.

## 5. Resetting
Server header `Clear-Site-Data: "cache", "storage"` (on logout, for example): `"cache"` removes locally cached data and `"storage"` removes DOM storage for the origin (localStorage, sessionStorage, IndexedDB, service worker registrations and more). Directives must be quoted strings. In dev, use your browser DevTools storage panel to clear site data.

## Verify
- [ ] Simulated small quota: app handles write failure without crashing.
- [ ] `persisted()` true after granting on an installed PWA.
- [ ] Logout clears user data from all storage types.

## Checked

Checked 2026-10-26 against MDN Storage quotas and eviction criteria, StorageManager.estimate(), StorageManager.persist() and the Clear-Site-Data header (mdn/content main). Corrected: Firefox's best-effort limit is the smaller of 10% of disk or a 10 GiB group limit; Safari figures are around 60% (browser apps) and 15% (embedded WebViews) from macOS 14 / iOS 17; automatic persistence approval applies to Safari as well as Chromium; Safari's seven-day proactive eviction is its own trigger. Removed the unconfirmed 'service worker registrations share quota' and the named DevTools quota-simulation setting. The web.dev link was not re-fetched.

Method: documentation only; no commands were run.
