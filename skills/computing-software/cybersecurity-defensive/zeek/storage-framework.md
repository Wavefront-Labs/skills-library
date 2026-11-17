---
id: computing-software.cybersecurity-defensive.zeek.storage-framework
name: storage-framework
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, storage-framework, storage-backend, sqlite-backend, key-value-store]
level: advanced
status: docs-checked
description: "Zeek storage framework: backend and serializer plugins (Redis, SQLite, JSON), Storage::Sync versus Storage::Async, BackendOptions, open_backend and OperationResult codes."
sources: ["https://docs.zeek.org/en/current/frameworks/storage.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# storage framework

A plugin-based key-value store for short- and long-term data derived from packets, using Zeek values as keys.

- **Backend**: access to a storage system. Redis and SQLite are provided; others can come as packages. Backends may add fields to option records.
- **Serializer**: converts Zeek values to byte buffers; the JSON serializer is the default (`Storage::STORAGE_SERIALIZER_JSON`).

**Modes**: `Storage::Async` (load `base/frameworks/storage/async`) calls must be used inside `when` statements. `Storage::Sync` (load `base/frameworks/storage/sync`) calls block and work directly or in `when`. Arguments and results are the same. With `-r`, all backends run synchronously so timers behave, yet async functions still require `when`.

Every operation returns `Storage::OperationResult`: a `code` (see `Storage::ReturnCode`, extensible by backends), an optional error message, and a value for `open_backend` and `get`.

```
@load base/frameworks/storage/sync
@load policy/frameworks/storage/backend/sqlite

local opts: Storage::BackendOptions;
opts$sqlite = [$database_path="test.sqlite", $table_name="testing"];
opts$serializer = Storage::STORAGE_SERIALIZER_JSON;
local res = Storage::Sync::open_backend(Storage::STORAGE_BACKEND_SQLITE, opts, string, string);
if ( res$code == Storage::SUCCESS )
    backend = res$value;
```

The last two arguments are key and value types; other types give `Storage::KEY_TYPE_MISMATCH`. Open in `zeek_init`, keep the handle in a global, and close with `Storage::Sync::close_backend`. Events: `Storage::backend_opened` and `Storage::backend_lost`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
