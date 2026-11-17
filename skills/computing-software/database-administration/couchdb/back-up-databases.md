---
id: computing-software.database-administration.couchdb.back-up-databases
name: back-up-databases
category: computing-software
field: database-administration
product: couchdb
tags: [backup, replication, couch-files, snapshots, shards]
level: practitioner
status: docs-checked
description: "Back up CouchDB databases by replication, by copying .couch files, or by storage snapshots, and why secondary indexes must be backed up first."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/backups.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CouchDB creates database files (including secondary indexes), configuration `*.ini` files and log files. Three ways to back up the databases:

- **Replication** to another CouchDB installation: the simplest approach. Choose one-shot or continuous replication to suit.
- **Copy the `.couch` files** from the data directory (default `data/`) at any time. The append-only storage format of databases and indexes makes this safe.
- **Storage snapshots** (ZFS, LVM, Amazon EBS): near-instantaneous on block storage. Quiesce the file system first if necessary, for example with Linux `fsfreeze`.

Order matters when copying files:

1. Back up secondary indexes first (`data/.shards`).
2. Then back up the main database files (`data/shards`) and the system databases in the parent `data/` directory.

Why: CouchDB updates slightly out-of-date views on the next read. A view or index that is newer than its database triggers a full index rebuild, which can be costly and slow disaster recovery.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/backups page (Database Backups): replication, copying .couch files, snapshots with fsfreeze, indexes in data/.shards before databases in data/shards, full rebuild when an index is newer than its database. Nothing removed.

Method: documentation only; no commands were run.
