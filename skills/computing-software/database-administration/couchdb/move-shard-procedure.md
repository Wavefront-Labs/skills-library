---
id: computing-software.database-administration.couchdb.move-shard-procedure
name: move-shard-procedure
category: computing-software
field: database-administration
product: couchdb
tags: [sharding, shard-move, rebalancing, shard-files, secondary-indexes]
level: sme
status: docs-checked
description: "The full ordered procedure for moving a CouchDB shard replica to another node, and how to copy shard and index files (views before databases)."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Adding a node does not redistribute existing shards; they must be moved manually. Stop resharding jobs first. Steps:

0. Target node has joined the cluster.
1. Copy the shard and index shard files to the target.
2. Put the target node in maintenance mode.
3. Update cluster metadata to add the target shard.
4. Monitor internal replication until up to date.
5. Clear maintenance mode.
6. Update metadata to remove the source shard.
7. Delete the shard and index files on the source.

**Copying (optional but faster than internal replication).** Database shards live in `data/shards/{range}/`; view and Mango index shards in `data/.shards/{range}/`. Copy with `cp`, `rsync` or `scp`:

```
scp {couch-dir}/data/.shards/{range}/{database}.{datecode}* {node}:{couch-dir}/data/.shards/{range}/
scp {couch-dir}/data/shards/{range}/{database}.{datecode}.couch {node}:{couch-dir}/data/shards/{range}/
```

Move view files before database files: a view ahead of its database is rebuilt from scratch.

**Final cleanup:**

```
rm {couch-dir}/data/shards/{range}/{db}.{datecode}.couch
rm -r {couch-dir}/data/.shards/{range}/{db}.{datecode}*
```

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page (Moving a shard): no automatic redistribution, the steps 0-7, shard and index locations, copy tools, views before databases, cleanup commands. Nothing removed.

Method: documentation only; no commands were run.
