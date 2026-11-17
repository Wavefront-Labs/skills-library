---
id: computing-software.database-administration.couchdb.rexi-rpc-tuning
name: rexi-rpc-tuning
category: computing-software
field: database-administration
product: couchdb
tags: [rexi, rpc, buffer-count, stream-limit, cluster-performance]
level: sme
status: docs-checked
description: "Tune CouchDB internal cluster RPC with the [rexi] buffer_count and stream_limit settings, and why a high stream_limit can lower throughput."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/cluster.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CouchDB nodes talk over distributed Erlang; the `rexi` library provides an optimised RPC layer on it. The defaults generally work well.

- `buffer_count`: the local RPC server buffers messages when a remote node is unavailable. This sets how many are buffered before messages start being dropped. Default `2000`.
- `stream_limit` (added 3.0): during streaming operations such as views and changes feeds, how many messages a remote worker may send to the coordinator without waiting for an acknowledgement. If too large the coordinator can be overwhelmed and deliver lower overall throughput to the client. It was hard-coded to `10` in 2.x; in 3.x it is configurable and defaults to `5`. Databases with a high `q` are especially sensitive.

```ini
[rexi]
buffer_count = 2000
stream_limit = 5
```

## Checked

2026-11-04. Confirmed against the CouchDB config/cluster page ([rexi]): buffer_count default 2000, stream_limit added in 3.0, hard-coded 10 in 2.x and default 5 in 3.x, throughput warning and sensitivity of high q. Nothing removed.

Method: documentation only; no commands were run.
