---
id: computing-software.data-engineering.trino.trino-syntactic-join-order
name: trino-syntactic-join-order
category: computing-software
field: data-engineering
product: trino
tags: [syntactic-join-order, hash-join, build-side, probe-side, join-ordering]
level: advanced
status: docs-checked
description: "Order joins largest to smallest when Trino cost-based optimization is off, and why the docs warn this is an implementation artifact."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/optimizer/cost-based-optimizations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino syntactic join order

Without cost-based optimization (strategy `NONE` or no statistics), Trino follows the syntactic join order. There is no formal tuning, but the in-memory hash join implementation can be exploited.

How it executes: Trino loads the right-most table of a join into memory as the build side and streams the next right-most table as the probe side. With several joins, the result of the first join stays in memory as the build side and the third right-most table becomes the probe, and so on. With parentheses forcing particular join pairings, Trino may run several lower-level joins at once, but each step follows the same rule, as does the final join of those results.

Consequence from the docs: write joins from the largest table to the smallest, which minimises memory use. Example with left joins:

```sql
SELECT *
FROM large_table l
  LEFT JOIN medium_table m ON l.user_id = m.user_id
  LEFT JOIN small_table s ON s.user_id = l.user_id
```

Warning: this is not a Trino feature. It is an artifact of how joins are implemented, and the behaviour may change without notice. The cost-based strategies instead need the connector to provide statistics.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. Removed an unsupported recommendation; other claims match the page.
