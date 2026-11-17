---
id: computing-software.data-engineering.trino.trino-dynamic-filtering-thresholds
name: trino-dynamic-filtering-thresholds
category: computing-software
field: data-engineering
product: trino
tags: [dynamic-filtering-thresholds, max-distinct-values-per-driver, min-max-filter, build-side, dimension-tables]
level: sme
status: docs-checked
description: "Tune Trino dynamic filter collection limits, understand distinct-values versus min-max filters, and the type limitations that block them."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/dynamic-filtering.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino dynamic filtering thresholds

For dynamic filtering to help, the smaller table must be the join build side. The cost-based optimizer chooses this from connector statistics, so keep table statistics current.

Collecting build-side values costs CPU, so Trino caps filter size. Six properties set the limits:
- `dynamic-filtering.max-distinct-values-per-driver`, `dynamic-filtering.max-size-per-driver`, `dynamic-filtering.range-row-limit-per-driver`
- the same three prefixed `dynamic-filtering.partitioned.`

The unprefixed limits apply when filters are collected before the build side is partitioned on join keys, which is the case for broadcast joins and when fault-tolerant execution is on. The `partitioned` limits apply after partitioning, when a partitioned join is chosen and fault-tolerant execution is off.

The distinct-values and size limits cap the distinct-values structure. Past those, Trino switches to a min and max per column, which is much coarser but can still filter well when the build side selects a range. The `range-row-limit` properties bound that min-max collection.

Layout advice: filtering works best where dimension keys correlate with columns, for example a date key that rises with the date, or a composite key like `US-NY-10001-1234`; the docs say this lets dynamic filtering succeed even with a large number of selected dimension rows.

Limitations:
- Min-max collection is unsupported for `DOUBLE`, `REAL` and unorderable types.
- `IS NOT DISTINCT FROM` filtering is unsupported for `DOUBLE` and `REAL`.
- A cast from build key type to probe key type is supported; an implicit cast from probe to build only in limited cases, such as a `DOUBLE` build key with `REAL` or `INTEGER` probe key.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. One inferred claim reworded to the page's wording; rest unchanged.
