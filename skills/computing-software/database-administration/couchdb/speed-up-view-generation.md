---
id: computing-software.database-administration.couchdb.speed-up-view-generation
name: speed-up-view-generation
category: computing-software
field: database-administration
product: couchdb
tags: [performance, views, stale, stable, builtin-reduce, couchjs]
level: advanced
status: docs-checked
description: "Speed up CouchDB view builds and reads: built-in _sum and _count reduces, and stable=false with update=false or lazy instead of stale in a cluster."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/performance.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JavaScript views are very slow to generate over many documents: the latency between CouchDB and the separate `couchjs` query server dominates, and a single CPU is not even saturated. The page cites a 10 million document database taking about 10 minutes to load but about 4 hours for view generation. View data is not replicated; it is rebuilt on each database, so you cannot generate views on a separate server.

**Built-in reduces.** For a plain sum or count, write `_sum` or `_count` instead of a JavaScript function. This runs native Erlang and cuts I/O with the query server:

```json
"reduce": "_sum"
```

**Stale reads in a cluster.** `stale` requests are served by a fixed set of shards for consistent results, trading away availability. If you do not need that, use `stable=false&update=false` instead of `stale=ok`, or `stable=false&update=lazy` instead of `stale=update_after`, so any available replica answers.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/performance page (Views): couchjs latency, the 10 million document timing, views not replicated, _sum and _count built-ins, stable=false with update=false or lazy. Nothing removed.

Method: documentation only; no commands were run.
