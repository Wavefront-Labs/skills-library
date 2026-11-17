---
id: computing-software.database-administration.couchdb.database-placement-rules
name: database-placement-rules
category: computing-software
field: database-administration
product: couchdb
tags: [sharding, placement, zones, couchdb-zone, cluster]
level: advanced
status: docs-checked
description: "Control where new CouchDB shard replicas land with node zone attributes and the [cluster] placement setting or ?placement= query parameter."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Placement rules set at database creation which nodes host replicas. Warning: `placement` overrides `n`, both in the ini file and in a URL.

1. Label each node with a zone by editing its document in the `_nodes` database at `/_node/_local/_nodes/{node-name}` and adding `"zone": "{zone-name}"`. Or set the `COUCHDB_ZONE` environment variable on each node and CouchDB writes the document on startup.
2. Define a consistent cluster-wide setting in each node's `local.ini`:

```ini
[cluster]
placement = {zone-name-1}:2,{zone-name-2}:1
```

This puts two replicas of each shard on nodes in zone 1 and one in zone 2.

Per database, use the same syntax as a query parameter:

```
curl -X PUT $COUCH_URL:5984/{db}?placement={zone}
```

To keep certain nodes from hosting replicas of new databases, give them a zone that does not appear in the `[cluster]` placement string.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page (Specifying database placement): placement overrides n, the zone attribute in the node document under /_node/_local/_nodes, COUCHDB_ZONE, the [cluster] placement syntax and meaning, the per-database query parameter, excluding nodes via an unlisted zone. Nothing removed.

Method: documentation only; no commands were run.
