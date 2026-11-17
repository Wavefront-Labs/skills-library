---
id: computing-software.database-administration.couchdb.migrate-old-compaction-daemon-config
name: migrate-old-compaction-daemon-config
category: computing-software
field: database-administration
product: couchdb
tags: [smoosh, compaction, migration, compaction-daemon, db-fragmentation]
level: advanced
status: docs-checked
description: "Port the old CouchDB compaction_daemon and compactions rules to smoosh channels, including the min_priority formula for fragmentation percentages."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/compaction.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The smoosh configuration is not backwards-compatible with the old `[compaction_daemon]` and `[compactions]` settings, so customised setups must be ported.

Mapping:

- `min_file_size` becomes the per-channel `min_size` setting.
- `db_fragmentation` becomes a `priority = ratio` channel with `min_priority = 1.0 / (1 - db_fragmentation/100)`, listed in `[smoosh] db_channels`.
- `view_fragmentation` likewise, listed in `view_channels`.
- `from` / `to` / `strict_window` apply per channel. Behaviour change: compactions are now suspended on leaving the window, not cancelled.
- `parallel_view_compaction` is replaced by each channel's `concurrency` setting. Total parallelism is the sum over all active channels.

Obsolete: `check_interval` and `snooze_period_ms` (the new daemon is event-driven).

Not supported: database-specific thresholds like the old `mydb` rule. Instead, configure channels for classes of files (large databases, small view indexes and so on), since most named-database rules can be expressed through properties of the database and its views.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/compaction page (Migration Guide): non-backwards-compatible configuration, the min_file_size, db_fragmentation and view_fragmentation mappings with the min_priority formula, per-channel window settings and suspend behaviour, parallel_view_compaction versus channel concurrency, obsolete settings, no database-specific thresholds. Nothing removed.

Method: documentation only; no commands were run.
