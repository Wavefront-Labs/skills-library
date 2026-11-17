---
id: computing-software.web-development.frontend-development.indexeddb-transactions-and-schema
name: indexeddb-transactions-and-schema
category: computing-software
field: web-development
product: frontend-development
tags: [client-side-storage, indexeddb, idb, object-store, indexeddb-transactions, onupgradeneeded, dexie, offline-data, indexeddb-upgrade, idb-library]
level: practitioner
status: docs-checked
description: "Storing structured offline data in IndexedDB with the idb wrapper: versioned schema upgrades, indexes, transaction lifetimes and blocked upgrades across tabs."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB
  - https://github.com/jakearchibald/idb
  - https://web.dev/articles/indexeddb
  - https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria
  - https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/
  - https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IndexedDB transactions and schema

**Goal:** a versioned client database with indexes that upgrades safely and doesn't hit transaction pitfalls.

## 1. Use a thin wrapper
The raw API is event-based; `idb` (about 1.19 kB brotli-compressed, per its README) mirrors it with promises and small improvements.

```js
import { openDB } from 'idb';
const db = await openDB('app', 3, {
  upgrade(db, oldVersion, newVersion, tx) {
    if (oldVersion < 1) db.createObjectStore('notes', { keyPath: 'id' });
    if (oldVersion < 2) tx.objectStore('notes').createIndex('byUpdated', 'updatedAt');
    if (oldVersion < 3) db.createObjectStore('outbox', { keyPath: 'id' });
  },
  blocked() { alert('Close other tabs of this app to finish updating'); },
  blocking() { db.close(); location.reload(); },   // this connection is blocking a newer version from opening
});
```
- Schema changes only happen in `upgrade` and require bumping the version. Use cumulative `if (oldVersion < n)` steps so any old client migrates.
- **blocked/blocking**: an open connection in another tab prevents the upgrade. Always close on `versionchange` (the `blocking` callback) or the new version never opens.

## 2. Reads and writes
```js
await db.put('notes', { id, text, updatedAt: Date.now() });
const recent = await db.getAllFromIndex('notes', 'byUpdated');   // ascending
const tx = db.transaction(['notes', 'outbox'], 'readwrite');
await Promise.all([tx.objectStore('notes').put(note), tx.objectStore('outbox').add(op), tx.done]);
```
Multi-store writes in one transaction are atomic.

## 3. Transaction auto-commit trap
Transactions are tied to the event loop: if you return to the event loop without using one, it becomes inactive. **Awaiting anything that isn't an IDB request** (fetch, setTimeout) inside a transaction lets it close (the idb README: do not `await` other things between the start and end of a transaction), and the next operation throws `TransactionInactiveError`. Fetch first, then open the transaction.

## 4. What can be stored
Anything the structured clone algorithm supports (for example objects, Map, Blob, ArrayBuffer). Functions and DOM nodes throw `DataCloneError`, and the prototype chain is not preserved (class instances come back as plain objects).

## 5. Durability and limits
Data can be evicted under storage pressure unless persistent storage is granted (see storage quota skill). MDN notes that Safari proactively deletes script-created data for an origin with no user interaction in the last seven days of browser use (WebKit announced this in 2020 and said home-screen web apps count their own days of use) - plan for re-sync. IndexedDB offers no confidentiality: OWASP advises against storing session tokens or secrets there.

## Verify
- [ ] Open the app in two tabs, deploy a version bump: second tab reloads instead of hanging.
- [ ] DevTools > Application > IndexedDB shows expected stores/indexes per version.
- [ ] Upgrading from every previous version in tests works.

## Checked

Checked 2026-10-26 against the idb README (jakearchibald/idb, repository pushed 2026-10-06), MDN Using IndexedDB, IDBObjectStore.put() and Structured clone algorithm, the MDN storage quotas page, the WebKit ITP blog post of 2020 and the OWASP HTML5 Security Cheat Sheet: `upgrade(db, oldVersion, newVersion, transaction)`, `blocked` and `blocking` callback meanings, transaction inactivity and `TransactionInactiveError`, structured-clone limits, and Safari's seven-day script-storage deletion. Corrected the comment on `blocking()` and removed the unconfirmed Dexie description. The web.dev link was not re-fetched.

Method: documentation only; no commands were run.
