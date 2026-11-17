---
id: computing-software.database-administration.couchdb.merge-shards-by-regeneration
name: merge-shards-by-regeneration
category: computing-software
field: database-administration
product: couchdb
tags: [sharding, merge-shards, decrease-q, replication, downtime]
level: advanced
status: docs-checked
description: "Decrease a CouchDB database's shard count q by regenerating it through a temporary database and replication, with the ordered steps."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`q` can be raised by splitting shards, but lowering it (merging) requires regenerating the database. Steps:

1. Stop any running shard splitting jobs via the `_reshard/state` API.
2. Create a temporary database with the desired shard settings (`q` query parameter on the PUT).
3. Stop clients accessing the database.
4. Replicate the primary into the temporary database. Repeat if the primary is still in active use.
5. Delete the primary database. Make sure nobody is using it.
6. Recreate the primary with the desired shard settings.
7. Clients can access the database again.
8. Replicate the temporary database back to the primary.
9. Delete the temporary database.

The cluster creates and distributes the new shards according to placement rules automatically.

Downtime can be avoided if client applications can be pointed at the new database, with a cut-over during a very brief outage window.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page (Merging Shards): all nine steps, placement-rule note, downtime-avoidance note. Nothing removed.

Method: documentation only; no commands were run.
