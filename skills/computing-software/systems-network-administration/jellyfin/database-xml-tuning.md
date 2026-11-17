---
id: computing-software.systems-network-administration.jellyfin.database-xml-tuning
name: database-xml-tuning
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, database-xml, sqlite, cachesize, pragma, locking-mode]
level: sme
status: docs-checked
description: "Tune Jellyfin's SQLite provider through the optional database.xml, including cacheSize, locking mode and arbitrary PRAGMAs, for very large libraries only."
sources: ["https://jellyfin.org/docs/general/administration/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tuning the SQLite database with database.xml

By default Jellyfin keeps library metadata in a SQLite file, `<Data Directory>/jellyfin.db`. An optional `database.xml` in the configuration directory tunes the SQLite provider; if it is absent the built-in defaults apply. The docs warn that these options are for advanced users, can corrupt the database if wrong, are not part of the stable API, and are not migrated between releases. Back up first.

The file root is `DatabaseConfigurationOptions` with `DatabaseType` (`Jellyfin-SQLite`), `LockingBehavior` (`NoLock` in the example) and `CustomProviderOptions/Options`, holding `CustomDatabaseOption` elements each with a `Key` and `Value`.

| Key | Default | Meaning |
| --- | --- | --- |
| `path` | `<Data Directory>/jellyfin.db` | database file |
| `cacheSize` | unset | SQLite `cache_size` per connection; negative means KiB, so `-262144` is about 256 MiB |
| `lockingmode` | `NORMAL` | `locking_mode` |
| `journalsizelimit` | `134217728` | `journal_size_limit` in bytes |
| `tempstoremode` | `2` | `temp_store`; 2 is memory |
| `syncmode` | `1` | `synchronous`; 1 is NORMAL |
| `pooling` | `True` | connection pooling |
| `command-timeout` | `60` | seconds |

Any other PRAGMA is set by prefixing the key with `#PRAGMA:`, for example `#PRAGMA:mmap_size` with value `268435456`.

A larger `cacheSize` helps some very large libraries and does nothing for others. Raise it in steps, measure each step, and keep the per-connection value well inside available memory.

## Checked

2026-11-03. Confirmed against the Jellyfin Configuration page, Database section: the warning, database.xml structure, all eight keys and defaults, #PRAGMA: prefix, cacheSize guidance. Nothing removed.

Method: documentation only; no commands were run.
