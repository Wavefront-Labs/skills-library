---
id: computing-software.database-administration.couchdb.shards-q-n-and-quorum
name: shards-q-n-and-quorum
category: computing-software
field: database-administration
product: couchdb
tags: [sharding, q-n, quorum, cluster, replicas]
level: practitioner
status: docs-checked
description: "How the q (shards) and n (replicas) settings, per-database overrides, and r/w read and write quorum work in a CouchDB cluster."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`q` is the number of shards, `n` the number of copies of each shard. Defaults: `n=3`, `q=2`, giving 6 shard replicas per database. Keep the node count a multiple of `n` for even distribution.

Defaults live in `[cluster]` (`q=2`, `n=3`); override in `etc/local.ini`. `[couch_peruser] q` applies to per-user databases (default 1). Per database:

```
curl -X PUT "$COUCH_URL:5984/database-name?q=4&n=2"
```

**Quorum.** Any node can coordinate a request and proxies to the nodes holding the data, replying once a quorum answers. Default `r = w = ((n div 2) + 1)`, which is 2 when `n` is 3. Override per request:

```
curl "$COUCH_URL:5984/{db}/{doc}?r=2"
curl -X PUT "$COUCH_URL:5984/{db}/{doc}?w=2" -d '{...}'
```

- `_view`, `_find` and `_search` read only one copy, whatever the quorum.
- `r` or `w` equal to `n` waits for all relevant nodes (or timeouts) and does not guarantee ACID consistency.
- `r` or `w` of 1 replies after one node.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page (Introduction and Quorum sections): defaults n=3 and q=2, 6 shard replicas, multiple-of-n advice, [cluster] and [couch_peruser] q (default 1), per-database q and n query parameters, quorum formula, r and w parameters, _view/_find/_search single-copy reads, r or w equal to n or 1. Nothing removed.

Method: documentation only; no commands were run.
