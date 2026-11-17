---
id: computing-software.messaging-and-integration.prosody.mod-mam-storage
name: mod-mam-storage
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, mam, storage, sql, archive, memory]
level: practitioner
status: docs-checked
description: "Where mod_mam keeps archives in Prosody: the archive store, SQL-only archives, memory-only archives with SQL for the rest, and the legacy archive2 store."
sources:
  - https://prosody.im/doc/modules/mod_mam
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_mam storage

mod_mam uses the store `archive`. To use mod_storage_sql only for MAM archives:

```lua
storage = {
  archive = "sql";
}
```

If no archive-capable storage backend can be opened, an in-memory one is used as fallback.

Memory-only archives with SQL for everything else. For performance and privacy reasons you might prefer to keep messages in memory only; this works best on smaller servers, and if Prosody restarts some clients may not receive messages. If all clients are offline, messages are still stored via mod_offline.

```lua
default_storage = "sql"
storage = {
    archive = "memory"
}
```

Early versions of mod_mam (in prosody-modules) stored data in a store called `archive2`; it is now just `archive`. To use the older store name if you still have data there:

```lua
archive_store = "archive2"; -- the old data
storage = {
  archive2 = "sql";
}
```

`archive_store` defaults to `"archive"` and should not be changed unless you are upgrading from an earlier version.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_mam (storage backend, fallback, memory-only example, archive2 example, archive_store default). Softened "archives are lost on restart" to the page's wording and removed a generic verify line.
Method: documentation only; no commands were run.
