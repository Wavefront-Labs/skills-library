---
id: computing-software.database-administration.couchdb.force-shard-sync
name: force-shard-sync
category: computing-software
field: database-administration
product: couchdb
tags: [sharding, sync-shards, internal-replication, mem3, monitoring]
level: advanced
status: docs-checked
description: "Force synchronization of all shard replicas with POST /{db}/_sync_shards and watch internal_replication_jobs on /_system until it settles."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Whether or not you pre-copied files to a new node, you can force synchronization of every replica of every shard in a database (added in 2.4.0):

```
curl -X POST $COUCH_URL:5984/{db}/_sync_shards
{"ok":true}
```

This adds load to the cluster and may affect performance. For one shard only, write to a document stored in that shard. For the duration of the sync, admins may want to raise `[mem3] sync_concurrency`.

**Monitor.** Query `/_node/{node-name}/_system` and watch the `internal_replication_jobs` metric. When it returns to its baseline from before the sync, or is 0, the shard replica is ready to serve data and the node can leave maintenance mode.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page: _sync_shards (added in 2.4.0), load warning, per-shard sync by writing a document, sync_concurrency note, internal_replication_jobs on /_system. Nothing removed.

Method: documentation only; no commands were run.
