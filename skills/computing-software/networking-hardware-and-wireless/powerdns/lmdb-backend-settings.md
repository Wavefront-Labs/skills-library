---
id: computing-software.networking-hardware-and-wireless.powerdns.lmdb-backend-settings
name: lmdb-backend-settings
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, lmdb, backend, lmdb-filename, lmdb-map-size, lmdb-shards, lmdb-sync-mode, lightning-stream]
level: practitioner
status: docs-checked
description: "Configure the PowerDNS LMDB backend: filename, shards, sync-mode, map-size, schema-version, Lightning Stream mode."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/lmdb.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LMDB backend settings

The backend creates its own schema and cannot be queried directly; use the API or `pdnsutil`. Stable since 4.4.0. Under systemd the shipped unit sets `ProtectSystem=full`, which can block writes to the database path.

- `lmdb-filename`: for example `/var/lib/powerdns/pdns.lmdb`.
- `lmdb-shards`: record shards; default 64 on 64-bit, 2 on 32-bit. Must be 1 in Lightning Stream mode.
- `lmdb-sync-mode`: `sync` (default since 4.9.0, safest), `nosync` (crash may corrupt), `nometasync` (keeps integrity, may lose the last transaction on an OS crash). `mapasync` was removed in 4.9.0.
- `lmdb-map-size`: MB per database; default 16000 on 64-bit, 100 on 32-bit. Can grow, never shrink. From 5.1.0 `lmdb-shards-map-size` sizes shards separately (0 means use `lmdb-map-size`).
- `lmdb-schema-version`: highest schema the backend may auto-upgrade to; defaults to the release's own. A schema is 1 for 4.2, 2 for 4.3, 3 for 4.4 to 4.6, 4 for 4.7, 5 for 4.8, 6 for 5.0 and later. To block upgrades, pin it to the current version before upgrading PowerDNS.
- `lmdb-random-ids` (no): random numeric IDs, useful when external tools sync databases.
- `lmdb-flag-deleted` (no): mark rather than remove deleted items; only for Lightning Stream.
- `lmdb-lightning-stream` (no): compatible mode; forces `lmdb-flag-deleted` and `lmdb-random-ids`, aborts startup if shards is not 1.
- `lmdb-write-notification-update` (yes): always persist notification and freshness timestamps. If disabled, run `pdns_control flush` before stopping to avoid spurious notifications.
- `lmdb-split-domains-table` (no, 5.1.0+): puts those timestamps in a separate table to cut I/O with many zones.
- `lmdb-page-size` (5.2.0+): power of two 256 to 65536, or 0 for the library default; only available with LMDB 1.0 and up, otherwise silently ignored.

## Checked

2026-11-08. Read in full: PowerDNS docs backends/lmdb.rst. Confirmed the stable-since-4.4.0 warning, ProtectSystem=full note, every setting listed with its default and version note, the schema version table, and the Lightning Stream mode effects. Added the LMDB 1.0 requirement for the page size.

Method: documentation only; no commands were run.
