---
id: computing-software.data-engineering.apache-pinot.apache-pinot-forward-index-disable-and-regenerate
name: apache-pinot-forward-index-disable-and-regenerate
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, forward-index, disabled, indexes-forward-disabled, range-index-v2, inverted-index, storage-saving]
level: advanced
status: docs-checked
description: "Disabling the Pinot forward index on offline columns: prerequisites, blocked query shapes, range index v2 need and regeneration on reload."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/forward-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disabling and regenerating the forward index

For columns only ever used as filters in `WHERE`, the forward index can be dropped to save storage. In the table config under `fieldConfigList`:
```
{ "name": "columnA",
  "indexes": { "forward": { "disabled": true } } }
```
(The older `"properties": { "forwardIndexDisabled": "true" }` still works but is not recommended.) A table reload is needed for the change to take effect.

Limitations:
- Supported only for immutable (offline) segments.
- If the column has a range index, the column must be single-value and use range index version 2. Range filters (`>`, `<`, `>=`, `<=`) on single-value columns need a version 2 range index or the query fails.
- To be able to regenerate the forward index later on reload, the dictionary **and** inverted index must be enabled on that column. Otherwise the only way back is regenerating and re-pushing segments from your offline jobs.
- Multi-value columns lose duplicated entries within a row, and may change in-row ordering, on regeneration; backfill if that matters.
- A sorted column allows the setting but it is treated as a no-op, because the sorted index acts as both forward and inverted index.

Queries that fail on a forward-index-disabled column: the column in `SELECT` (even with a filter), `GROUP BY`, `ORDER BY`, `HAVING`, and `SELECT DISTINCT`. Some aggregations still work (`MIN`, `MAX`, `DISTINCTCOUNT`, `DISTINCTCOUNTHLL` and more) while others do not (`SUM`, `AVG`, and expressions like `MAX(ADD(columnA, columnB))`).

Re-enable by turning the index back on (remove `disabled`) and reloading the segments; the forward index is regenerated from the dictionary and inverted index.

## Checked

2026-11-09. Read the "Disabling the forward index" section and the sorted-index section of the Pinot docs page `forward-index.md`. Confirmed limitations, config syntax, blocked query shapes and regeneration rule. Removed: the exact reload REST path, the literal `"encodingType": "DICTIONARY"` example and the claim that EQ/IN filters are specifically supported, none of which that section states. Not read: the RAW-encoding and compression codec sections in full.
Method: documentation only; no commands were run.
