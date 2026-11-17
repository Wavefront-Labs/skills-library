---
id: computing-software.database-administration.couchdb.edit-shard-map-in-dbs
name: edit-shard-map-in-dbs
category: computing-software
field: database-administration
product: couchdb
tags: [sharding, shard-map, dbs-database, changelog, by-node, by-range]
level: sme
status: docs-checked
description: "Manually edit a database's shard map document in the internal _dbs database: changelog, by_node and by_range must agree or the cluster can corrupt."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Shard placement metadata lives in the internal `_dbs` database, reachable only at `/_node/_local/_dbs/{name}`. It is replicated between nodes. Warning from the docs: mistakes can irreparably corrupt the cluster, and this must be done manually.

Fetch the document:

```
curl http://adm:pass@localhost:5984/_node/_local/_dbs/{name}
```

Fields: `_id` (database name), `_rev`, `shard_suffix` (creation timestamp as ASCII codepoints), `changelog`, `by_node` (shards on each node), `by_range` (nodes per shard).

To add a replica, make all three edits:

1. Append `["add", "{range}", "{node-name}"]` to `changelog`. Use `remove` to drop one. The node name must match `GET /_membership`.
2. Add the range to that node's `by_node` list.
3. Add the node to the range's `by_range` list.

The changelog entries and the two maps must match, or the database may be corrupted. Then `PUT` the full document back to the same URL with `-d '{...}'` (include `_rev`).

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page (Moving a shard, updating cluster metadata): _dbs reachable only via /_node/_local/_dbs, automatic replication, document anatomy, the three-step edit, add and remove changelog entries, node name matching _membership, consistency warning, PUT of the new metadata. Nothing removed.

Method: documentation only; no commands were run.
