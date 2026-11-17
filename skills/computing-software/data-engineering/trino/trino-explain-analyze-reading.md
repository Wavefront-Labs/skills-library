---
id: computing-software.data-engineering.trino.trino-explain-analyze-reading
name: trino-explain-analyze-reading
category: computing-software
field: data-engineering
product: trino
tags: [explain-analyze, query-plan, fragments, skew, verbose]
level: advanced
status: docs-checked
description: "Read Trino EXPLAIN ANALYZE output: per-fragment CPU and blocked time, relative plan node cost by wall time, input statistics for spotting skew, and VERBOSE metrics."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/sql/explain-analyze.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino explain analyze reading

`EXPLAIN ANALYZE [VERBOSE] statement` executes the statement and prints the distributed plan with the cost of each operation. Because it runs the query, treat it like the query itself (it reads data and costs resources).

What the output shows:
- A header line with queued, analysis, planning and execution time.
- Per fragment (for example `Fragment 1 [HASH]`, `Fragment 2 [SOURCE]`): CPU, scheduled and blocked time (split into input and output blocking), input rows and bytes, per-task average and standard deviation, and output rows.
- Per plan node: layout, estimates, CPU, scheduled and blocked time with percentages, output rows and size, and `Input avg.` with `Input std.dev.`.

The percentage cost of plan nodes is based on wall time, which may or may not correlate with CPU time. The input average and standard deviation per node instance are the tool for detecting data anomalies such as skew: a very large `Input std.dev.` (the docs example shows 793.73% on a local exchange) means work is unevenly spread. A scan node also reports `Filtered:` percentage and `Physical Input`, which shows how selective the filter was against the bytes actually read.

`VERBOSE` adds low-level operator statistics, for example the window operator prints metric distributions for CPU time, input rows and scheduled time (count, percentiles, min, max), active drivers, index size and partition size. The docs note that interpreting these may need knowledge of Trino internals.

Caveat from the docs: the stats may not be entirely accurate, especially for queries that complete quickly. The page's only cross-reference is to the plain `EXPLAIN` statement.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. Removed an unsupported suggestion; rest matches the page.
