---
id: computing-software.database-administration.couchdb.clustered-purge-internals
name: clustered-purge-internals
category: computing-software
field: database-administration
product: couchdb
tags: [purge, purge-seq, purged-infos-limit, internal-replication, tombstones]
level: sme
status: docs-checked
description: "How clustered purge keeps replicas and indexes consistent: purge trees, purge_seq, purged_infos_limit compaction, and eventual consistency via internal replication."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/purging.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Clustered purge mainly cleans databases with many deleted tombstones or documents with large numbers of conflicts, but can purge any document with any number of revisions. It maintains eventual consistency and avoids needlessly invalidating secondary indexes.

- Each database keeps a number of historical purges and its current `purge_seq`. Internal replication and indexes process purges and checkpoint their progress.
- Two internal trees: `purge_tree` (UUID to PurgeSeq, DocId, Revs) and `purge_seq_tree` (PurgeSeq to UUID, DocId, Revs). Each purge request gets a UUID.
- Compaction keeps only `purged_infos_limit` purges, but only removes those already processed by indexes and internal replication, so the trees may hold more.
- Internal replication first pulls purges from the target and applies them on the source, then pushes the source's purges. It filters requests whose UUID already exists in the replica.
- Each purge bumps the database `update_seq`, so indexes update and apply it.

Settings in `default.ini` or `local.ini`: `max_revisions_number` (default infinity), `allowed_purge_seq_lag` (100), `index_lag_warn_seconds` (86400).

## Checked

2026-11-04. Confirmed against the CouchDB cluster/purging page: purpose, purge_seq and checkpointing, purge_tree and purge_seq_tree layouts, purged_infos_limit compaction behaviour, pull-then-push internal replication with UUID filtering, update_seq bump, and the three settings with defaults. Nothing removed.

Method: documentation only; no commands were run.
