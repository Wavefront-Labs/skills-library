---
id: computing-software.data-engineering.trino.trino-join-reordering-and-distribution
name: trino-join-reordering-and-distribution
category: computing-software
field: data-engineering
product: trino
tags: [join-reordering-strategy, join-distribution-type, broadcast-join, partitioned-join, cost-based-optimizer]
level: advanced
status: docs-checked
description: "How the Trino cost-based optimizer picks join order and broadcast versus partitioned distribution, and how to cap replicated table size."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/optimizer/cost-based-optimizations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino join reordering and distribution

Join order matters because early joins that produce lots of data force later stages to process and ship more. With cost-based join enumeration Trino uses connector-supplied statistics to estimate costs and picks the cheapest order.

`join_reordering_strategy` (default from `optimizer.join-reordering-strategy`):
- `AUTOMATIC` (default): full automatic enumeration.
- `ELIMINATE_CROSS_JOINS`: remove unnecessary cross joins only.
- `NONE`: purely syntactic order.
If statistics are missing or a cost cannot be computed, `AUTOMATIC` falls back to `ELIMINATE_CROSS_JOINS`.

Trino uses hash joins: one input is the build side (hash table), the other the probe side. Distribution types:
- Partitioned: each node builds a hash table from a fraction of the data; both tables are redistributed by join-key hash. Slower but supports much larger joins, needing only distributed memory.
- Broadcast: every node builds a table from all the build data. Faster when the build side is much smaller, but the filtered build table must fit in memory on each node.

`join_distribution_type` (default from `join-distribution-type`) accepts `AUTOMATIC` (default), `BROADCAST` or `PARTITIONED`. Cost-based selection chooses partitioned versus broadcast; cost-based enumeration chooses which side is build and probe.

Cap replicated size with `join-max-broadcast-table-size` or session `join_max_broadcast_table_size` (default 100MB). It applies when either setting is `AUTOMATIC` and protects concurrency and plans when the optimizer misestimates sizes. The connector must provide statistics for any of this to work.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
