---
id: computing-software.software-engineering.javascript.js-web-storage-and-indexeddb
name: js-web-storage-and-indexeddb
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-web-storage, localstorage, indexeddb, storage-quota, structured-clone]
level: practitioner
status: docs-checked
description: "Choose between localStorage, sessionStorage, IndexedDB and Cache storage and handle quota and private-mode failures."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/Using_the_Web_Storage_API", "https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria", "https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Browser storage

- `localStorage` and `sessionStorage`: keys and values are always strings, so `JSON.stringify` objects and arrays. `localStorage` is shared by all tabs of the same origin; `sessionStorage` lasts for the page session and is shared only within the tab (among same-origin iframes).
- Limit: browsers store up to 5 MiB of local storage and 5 MiB of session storage per origin. When it is reached they throw `QuotaExceededError`: wrap writes in `try...catch`, and consider deleting data before storing new data.
- In private browsing some browsers give an empty `localStorage` with a quota of zero, so feature-detect storage by actually writing, and tell a real `QuotaExceededError` (storage exists but is full) from an unusable store; render without storage when it fails.
- The `storage` event fires in other same-origin documents sharing the storage space (not in the page making the change): use it for cross-tab sync.
- IndexedDB: asynchronous API (the synchronous API was removed from the spec). `open(name, version)` returns a request handled through events; version numbers are integers (2.1 and 2.4 both round to 2 and fire no upgrade). `onupgradeneeded` runs when a database is created or its version increases and is the only place to create or delete object stores and indexes.
- Eviction: data is best-effort by default and may be evicted without asking the user. `navigator.storage.persist()` requests persistent storage, which is only deleted if the user chooses; `navigator.storage.estimate()` returns estimated (not exact) usage and quota. Eviction deletes all of an origin's data at once (IndexedDB and Cache API together), so keep the server as source of truth for anything you cannot lose.

## Checked

Checked 2026-11-09 against MDN "Using the Web Storage API", "Storage quotas and eviction criteria" and "Using IndexedDB" (search-targeted reads of the sections cited, not full reads of the IndexedDB page).
Confirmed: every point above.
Removed as unconfirmed: the "synchronous, blocks the main thread" claim, `SecurityError`, transaction auto-commit behaviour, the `idb` wrapper advice, the XSS and `HttpOnly` cookie advice, and the ECMAScript spec and MDN JavaScript landing sources.

Method: documentation only; no commands were run.
