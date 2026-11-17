---
id: computing-software.database-administration.cloudnative-pg.wal-archiving-plugin-and-archive-timeout
name: wal-archiving-plugin-and-archive-timeout
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [wal-archiving, barman-cloud-plugin, archive-timeout, iswalarchiver, pitr, rpo, deprecation]
level: practitioner
status: docs-checked
description: "Configure WAL archiving through the plugin mechanism (one isWALArchiver plugin), know the barmanObjectStore deprecation timeline and the 5 minute archive_timeout default."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/wal_archiving.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
WAL archiving continuously ships WAL files from the primary to an object store; it is required for point-in-time recovery and underpins both object-store and volume-snapshot backup strategies.

Archiving is done by a plugin declared under `spec.plugins` in the `Cluster`. **Only one plugin at a time** can be the archiver, selected by setting `isWALArchiver` to `true` in that plugin's configuration. The Barman Cloud Plugin is currently the only officially supported WAL archiving plugin from the community (docs: cloudnative-pg.io/plugin-barman-cloud).

**Deprecation:** native archiving via `.spec.backup.barmanObjectStore` still works but is deprecated. CloudNativePG 1.31 is the last minor release shipping it; it is removed from 1.32.0. New deployments should use the plugin, and existing ones should follow the plugin's guide "Migrating from Built-in CloudNativePG Backup".

**archive_timeout:** the operator sets it to `5min` by default, so a WAL file is closed and archived at least every five minutes even under light load. That gives a deterministic time-based worst case for your RPO. You can change `archive_timeout` in the PostgreSQL configuration, but the page says the default suits most use cases.

## Checked

2026-11-04. Plugin-based WAL archiving, native barmanObjectStore deprecation (removed from 1.32.0) and the archive_timeout default confirmed on the WAL archiving page.

Method: documentation only; no commands were run.
