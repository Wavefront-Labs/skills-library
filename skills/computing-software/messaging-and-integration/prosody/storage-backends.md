---
id: computing-software.messaging-and-integration.prosody.storage-backends
name: storage-backends
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, storage, sql, internal, memory]
level: intro
status: docs-checked
description: "Prosody storage backends: internal (default, file-based), sql, memory (tests only), null and none, and which support archives."
sources:
  - https://prosody.im/doc/storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage backends

Select the backend with the `storage` option. Storage plugins are loaded automatically on demand, so they need not be in `modules_enabled`.

| Backend | Description | Archive support |
|---|---|---|
| `internal` | Default file-based storage | Yes, see limits |
| `sql` | SQL database support | Yes |
| `memory` | Keeps data in memory only, intended for tests, not production | Yes |
| `null` | Always fails to load/save data | No |
| `none` | All stores always empty and saving always fails | No |

Additional backends are available from the Community modules project.

```lua
storage = "internal"
```

Per-store examples from the page: rosters in SQL and everything else in the default internal backend:

```lua
storage = {
    roster = "sql";
}
```

Everything in SQL except accounts:

```lua
default_storage = "sql"
storage = {
    accounts = "internal";
}
```

Prosody includes a migration tool for moving data between stores.

## Checked

2026-11-04: confirmed against prosody.im/doc/storage (backend table including archive support, on-demand loading, examples, migration tool). Corrected memory (page says archive support yes), and removed the migrator path and a generic verify line, which the page does not state.
Method: documentation only; no commands were run.
