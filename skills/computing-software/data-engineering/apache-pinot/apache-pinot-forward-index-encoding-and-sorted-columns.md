---
id: computing-software.data-engineering.apache-pinot.apache-pinot-forward-index-encoding-and-sorted-columns
name: apache-pinot-forward-index-encoding-and-sorted-columns
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, forward-index, dictionary-encoding, sorted-column, sortedcolumn, run-length-encoding, tableindexconfig, metadata-properties]
level: practitioner
status: docs-checked
description: "Pinot forward index basics: dictionary encoding, sorted columns with run-length encoding, and sortedColumn for realtime but not offline."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/forward-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forward index encoding and sorted columns

The forward index is enabled by default for every column. By default a column is dictionary encoded: the index stores bit-compressed dictionary IDs, which is space efficient when unique values are far fewer than rows. The alternative is `RAW` encoding, which stores actual values and avoids dictionary lookups, suited to columns with many unique values.

A **sorted** forward index uses run-length encoding built on dictionary encoding: for each unique value it stores start and end docIds, and it can also serve as an inverted index. It is active only when the segment is sorted by that column and the dictionary is enabled. Sorting must hold within each segment; sorting across segments is not needed.

How to get a sorted segment:
- Realtime: set `tableIndexConfig.sortedColumn` to exactly one column (the property is a JSON array, but more than one column does not sort by all of them); Pinot sorts the segment on commit.
- Offline: `sortedColumn` is ignored. The input data must already be sorted by the column before ingestion.

```
"tableIndexConfig": { "sortedColumn": ["customerId"] }
```

Pinot actually decides sortedness by scanning each column when the segment is built: if a column's values are all ascending it is treated as sorted, whatever `sortedColumn` says. So two segments of one table can differ in their sorted columns.

Check it in a segment's `metadata.properties` (`column.<name>.isSorted = true`), or through the controller segment metadata endpoint, which returns a `sorted` flag for offline segments and committed realtime segments.

Since 1.3.0 a raw (no-dictionary) column can be configured as sorted without forcing an inverted index.

## Checked

2026-11-09. Read the encoding comparison, dictionary-encoded, sorted forward index, checking-sort-status and raw sections of the Pinot docs page `forward-index.md`. Confirmed all of the above. Removed: advice to pick a "high-selectivity key" and that a sorted column makes a separate inverted index "unnecessary" (the page says only that it can act as one).
Method: documentation only; no commands were run.
