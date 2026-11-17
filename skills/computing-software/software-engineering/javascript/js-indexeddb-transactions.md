---
id: computing-software.software-engineering.javascript.js-indexeddb-transactions
name: js-indexeddb-transactions
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, indexeddb-transaction, js-storage]
level: advanced
status: docs-checked
description: "Open, upgrade and query IndexedDB safely: versionchange transactions, transaction lifetime, key ranges, cursors, multi-tab upgrades."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB", "https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IndexedDB transactions and versioning

- Schema changes (creating or deleting object stores and indexes) happen only in `onupgradeneeded`, which fires when a database is created or opened with a higher version. That transaction is in `versionchange` mode, opened by `indexedDB.open(name, version)`. Versions are integers: 2.1 and 2.4 both round to 2 and fire no upgrade.
- Modes: `readonly` (the default when none is given), `readwrite` and `versionchange`. Pass the object stores you need as the scope; an empty array for "all stores" is a `InvalidAccessError` per the spec. Non-overlapping scopes can run concurrently; multiple `readonly` transactions may overlap, but only one `readwrite` transaction can run for an object store at a time. Use `readwrite` only when needed.
- Transaction lifetime is tied to the event loop: if you return to the event loop without making a request on the transaction, it becomes inactive. Only a pending request keeps it active, and its callback can make another request. `TRANSACTION_INACTIVE_ERR` means this went wrong.
- Errors bubble to the transaction; the default is to abort and roll back the whole transaction unless you call `stopPropagation()` on the error event. A transaction receives `error`, `abort` and `complete` events.
- Use indexes and key ranges instead of scanning: `IDBKeyRange.only`, `lowerBound`, `upperBound`, `bound(lower, upper, lowerOpen, upperOpen)`, passed to `openCursor()` or `openKeyCursor()`. Cursors run ascending by default; pass `prev`, `nextunique` or `prevunique` for other directions. Use `getAll()` when you want every object and a cursor when you only need keys, since cursor values are created lazily.
- Multi-tab upgrades: when `open()` asks for a higher version, other open connections must acknowledge it; `onblocked` fires until they close. Set `db.onversionchange` to call `db.close()`, otherwise the upgrade waits until the user closes the tab. Also handle `VersionError` for apps opened with an outdated version.
- Browser shutdown, lost permissions or a removed disk abort every transaction with `AbortError` and then fire `close` on the connection (`IDBDatabase.onclose`). Keep the database consistent at the end of every transaction (combine a clear and its rewrite), and never tie transactions to `unload` events.
- MDN lists wrappers such as `idb` (mirrors the API with small usability improvements) and `idb-keyval` (promise-based key-value store).
- Persistence and quota: data is best-effort by default; `navigator.storage.persist()` requests persistence and `navigator.storage.estimate()` returns estimated usage. A write over quota fails with `QuotaExceededError`.

Self-check: bump the version in a second tab and confirm the first closes gracefully via `onversionchange`.

## Checked

2026-11-08. Confirmed on MDN Using IndexedDB (versioning, modes, scope and concurrency rules, transaction lifetime, error behaviour, key ranges, cursors, multi-tab upgrade flow, shutdown behaviour, library list) and the Storage quotas page for `persist()`, `estimate()` and `QuotaExceededError`. Removed the claim that awaiting a non-IDB promise commits a transaction early with `TransactionInactiveError`; the page describes the inactive transaction and the `TRANSACTION_INACTIVE_ERR` code only.

Method: docs-only read of cited pages, 2026-11-08
