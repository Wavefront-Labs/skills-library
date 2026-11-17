---
id: computing-software.database-administration.couchdb.compaction-overview
name: compaction-overview
category: computing-software
field: database-administration
product: couchdb
tags: [compaction, disk-space, smoosh, maintenance]
level: intro
status: docs-checked
description: "What CouchDB compaction does, the disk space it needs, and how the smoosh automatic compaction daemon and manual compaction relate."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/compaction.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Compaction reduces disk usage by removing unused and old data from database or view index files, much like `vacuum` in other database systems.

How it works:

- CouchDB re-creates the database or view in a new file with the `.compact` extension.
- This needs roughly twice the disk storage, so CouchDB checks available disk space first.
- When all live data has been copied, the compacted file is swapped into service transparently and the old file is removed.

Automatic vs manual:

- Since CouchDB 2.1.1 automatic compaction is enabled by default. The daemon is internally called "smoosh".
- Manual compaction is still possible per database (`POST /{db}/_compact`) and per design document (`POST /{db}/_compact/{ddoc}`).

During database compaction, old document revisions are replaced by a small piece of metadata called a tombstone, used for conflict resolution during replication. The number of stored revisions is set with the `/{db}/_revs_limit` endpoint.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/compaction page: purpose, .compact file, roughly twice the disk space, file swap, automatic compaction by default since 2.1.1, smoosh name, manual endpoints, tombstones and _revs_limit. Nothing removed.

Method: documentation only; no commands were run.
