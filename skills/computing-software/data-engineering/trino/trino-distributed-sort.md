---
id: computing-software.data-engineering.trino.trino-distributed-sort
name: trino-distributed-sort
category: computing-software
field: data-engineering
product: trino
tags: [distributed-sort, sort, query-max-memory-per-node, retry-policy]
level: practitioner
status: docs-checked
description: "Sort data sets larger than one node's memory with Trino distributed sort, and know why the TASK retry policy switches it off."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/dist-sort.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino distributed sort

Distributed sort lets Trino sort data that exceeds `query.max-memory-per-node`. It is on by default, controlled by the `distributed_sort` session property or the `distributed-sort` property in the coordinator's `etc/config.properties`.

How it works: the sort operator runs in parallel on several nodes. Each worker produces partially sorted data, which is streamed to a single worker for a final merge. Memory across many workers is used for the sort, so data sets that would not fit on one node can be sorted.

Performance expectations from the docs: an improvement can be expected, but it does not scale linearly with node count, because the final merge happens on one node.

Interaction with fault-tolerant execution: distributed sort is used with the `NONE` and `QUERY` retry policies. It is automatically disabled with the `TASK` retry policy, because distributed sort needs all stages of a query to run concurrently, and task-level retries do not guarantee that.

The page only states that it is enabled via the session property or the coordinator config property; it gives no explicit steps for turning it off.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. Removed the unsupported how-to-disable steps; other claims unchanged.
