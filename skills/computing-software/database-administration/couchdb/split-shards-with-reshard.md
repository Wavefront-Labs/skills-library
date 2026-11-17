---
id: computing-software.database-administration.couchdb.split-shards-with-reshard
name: split-shards-with-reshard
category: computing-software
field: database-administration
product: couchdb
tags: [sharding, resharding, shard-splitting, reshard-api, q-value]
level: advanced
status: docs-checked
description: "Split CouchDB shards online with the _reshard API: check cluster state, clear completed jobs, post split jobs by db, node and range, and track progress."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `_reshard` API currently supports only splitting. This is how `q` is raised after creation.

1. `GET /_reshard` for a summary: `state` (normally `running`), `state_reason`, and job counts. Watch `total`: there is a maximum number of jobs per node (`max_jobs` in the reshard config), and exceeding it errors.
2. Remove completed jobs: list with `GET /_reshard/jobs` and `DELETE /_reshard/jobs/{jobid}` for those with `job_state` `completed`.
3. Look at the shard map with `GET /{db}/_shards`.
4. Post a job. Parameters `db`, `node` and `range` allow splitting all ranges everywhere, all ranges on one node, or one range on one node:

```
curl -s -H "Content-type: application/json" -XPOST $COUCH_URL:5984/_reshard/jobs \
  -d '{"type": "split", "db":"db1", "range":"00000000-7fffffff"}'
```

The response has one job per shard copy (`ok`, `id`, `node`, `shard`).

5. Track with `GET /_reshard/jobs` or `GET /_reshard/jobs/{jobid}`. When done, the range appears as two halves in `_shards`.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page (Splitting Shards): split-only API, GET /_reshard state and total, max_jobs per node and error when exceeded, removing completed jobs, GET /{db}/_shards, job parameters db, node and range, the POST example and one job per copy, progress endpoints, q increased later by splitting. Nothing removed.

Method: documentation only; no commands were run.
