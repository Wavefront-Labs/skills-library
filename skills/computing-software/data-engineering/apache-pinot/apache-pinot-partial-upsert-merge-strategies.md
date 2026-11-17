---
id: computing-software.data-engineering.apache-pinot.apache-pinot-partial-upsert-merge-strategies
name: apache-pinot-partial-upsert-merge-strategies
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, partial-upsert, partialupsertstrategies, defaultpartialupsertstrategy, partialupsertmergerclass, postpartialupserttransformconfigs, overwrite, increment, append, union, ignore, force-overwrite, nullhandlingenabled]
level: advanced
status: docs-checked
description: "Partial upsert merge strategies (OVERWRITE, INCREMENT, APPEND, UNION, IGNORE, MAX, MIN, FORCE_OVERWRITE), per-column and default strategy, custom merger, null handling."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/upsert-and-dedup/upsert.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial upsert merge strategies

Partial upsert (mode `PARTIAL`; the default mode is `FULL`) updates only chosen columns of the existing row. Per the docs' table-type matrix, PARTIAL upsert is supported on REALTIME tables only (OFFLINE and HYBRID support FULL only). Null handling must be enabled.
```
"upsertConfig": {
  "mode": "PARTIAL",
  "defaultPartialUpsertStrategy": "OVERWRITE",
  "partialUpsertStrategies": { "rsvp_count": "INCREMENT", "group_name": "IGNORE" }
},
"tableIndexConfig": { "nullHandlingEnabled": true }
```
Since release 0.10.0, columns without a strategy use OVERWRITE, and `defaultPartialUpsertStrategy` changes that default.

| Strategy | Effect |
|---|---|
| OVERWRITE | overwrite the column of the last record |
| INCREMENT | add the new value to the existing value |
| APPEND | add the new item to the Pinot unordered set |
| UNION | add the new item to the unordered set if not present |
| IGNORE | keep the existing value (0.10.0+) |
| MAX / MIN | keep the larger / smaller of existing and new (0.12.0+) |
| FORCE_OVERWRITE | always replace, including with null (1.4.0+) |

For strategies other than FORCE_OVERWRITE, if either the existing or incoming value is null Pinot ignores the strategy and keeps the non-null value. Use FORCE_OVERWRITE when an incoming null should clear the stored value.

Related keys:
- `partialUpsertMergerClass`: custom row merger on the server classpath with a constructor `(List<String> primaryKeyColumns, List<String> comparisonColumns, UpsertConfig upsertConfig)`. It is mutually exclusive with `partialUpsertStrategies`; Pinot rejects both together.
- `postPartialUpsertTransformConfigs`: list of `{columnName, transformFunction}` entries (for example `plus(score,bonus)`) that recompute derived columns after the merge. PARTIAL tables only; the destination column must exist in the schema and cannot be a primary key, comparison column, deleteRecordColumn or outOfOrderRecordColumn, and cannot appear twice or be referenced by its own function.
- Partial upsert tables skip out-of-order events (a record with a smaller comparison value arriving later is not indexed).

## Checked

Confirmed against the Pinot docs page "Stream ingestion with upsert": strategy table and version tags, null rules, default strategy, merger class constraints, post-merge transform validation, null-handling requirement. Corrected the old "realtime tables only" wording to the page's per-mode table-type matrix, and removed the unsourced claim that primary key and comparison columns are never merged.

Method: docs-only read of cited pages, 2026-11-08
