---
id: computing-software.database-administration.couchdb.examine-database-shards
name: examine-database-shards
category: computing-software
field: database-administration
product: couchdb
tags: [sharding, shards, shard-map, cluster, diagnostics]
level: practitioner
status: docs-checked
description: "Inspect how a CouchDB database is sharded with the cluster block of GET /{db}, GET /{db}/_shards and GET /{db}/_shards/{docid}."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three endpoints show a database's sharding.

1. `GET /{db}` includes a `cluster` object with `q`, `n`, `w` and `r`. For example `q` 8 and `n` 3 means 24 shard replicas across the nodes.
2. `GET /{db}/_shards` returns `shards`, mapping each hash range (such as `00000000-1fffffff`) to the list of node names holding a replica.
3. `GET /{db}/_shards/{docid}` returns the `range` and `nodes` for the shard that stores that document.

```
curl -s $COUCH_URL:5984/mydb/_shards | jq .
curl -s $COUCH_URL:5984/mydb/_shards/joan | jq .
```

Use these to confirm shards are spread evenly across nodes, or to find which shard holds a document.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page (Examining database shards): the cluster block, _shards and _shards/{docid} outputs. Removed a mention of data/shards files that the section does not tie to these endpoints.

Method: documentation only; no commands were run.
