---
id: computing-software.data-engineering.apache-pinot.apache-pinot-timestamp-index
name: apache-pinot-timestamp-index
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, timestamp-index, timestampconfig, granularities, datetrunc, derived-column, time-bucketing]
level: practitioner
status: docs-checked
description: "Timestamp index: timestampConfig.granularities generates $ts$ derived columns and rewrites dateTrunc calls to use them, from MILLISECOND up to YEAR."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/timestamp-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timestamp index

A timestamp index pre-computes time values at coarser granularities so range filters and group-bys on `TIMESTAMP` columns avoid per-row conversion. Requires Pinot 0.11 or later.

Configured per column in `fieldConfigList`; `timestampConfig.granularities` must be an array with at least one value:
```
{ "name": "ts", "timestampConfig": { "granularities": ["DAY", "WEEK", "MONTH"] } }
```

Allowed granularities: MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR.

Supported column types: `TIMESTAMP`, or `LONG` columns holding millisecond epoch values.

What happens:
1. Pinot pre-generates one extra column per granularity, with a forward index and a range index. The name is `$<column>$<granularity>`: column `ts` with DAY and MONTH gives `$ts$DAY` and `$ts$MONTH`.
2. Query rewrite: `dateTrunc('DAY', ts)` in a GROUP BY or selection reads `$ts$DAY`; for predicates the range index is built on each granularity column.

Limitations:
- Each granularity adds a column and storage, so list only the granularities you query.
- The auto-rewrite applies only to `dateTrunc` calls in predicates and group-by clauses; other time functions are not rewritten.

## Checked

2026-11-08. Read the whole pinot-docs timestamp-index page. Confirmed 0.11+, the nine granularities, column types, the `$ts$GRANULARITY` naming, the dateTrunc rewrite and limitations. Corrected the derived column description (forward plus range index, not "its own dictionary and inverted index") and removed the `indexTypes`/`encodingType` snippet and the reload remark, none of which the page shows.

Method: documentation only; no commands were run.
