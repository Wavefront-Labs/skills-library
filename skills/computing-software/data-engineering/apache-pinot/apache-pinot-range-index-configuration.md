---
id: computing-software.data-engineering.apache-pinot.apache-pinot-range-index-configuration
name: apache-pinot-range-index-configuration
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, range-index, indexes-range, rangeindexcolumns, range-index-v2, bit-sliced, raw-index]
level: practitioner
status: docs-checked
description: "Range index setup: indexes.range with version 2 (the default), supported column types, RAW plus dictionary rule, legacy list."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/range-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Range index configuration

A range index speeds up range predicates (`>`, `<`, `>=`, `<=`, `BETWEEN`). It maps ranges of values to document IDs, as a variant of an inverted index. It is especially useful on metric columns with very many unique values, where an inverted index would be large and inefficient.

Recommended config, in `fieldConfigList`:
```
{ "name": "hits", "indexes": { "range": {} } }
```
The version defaults to `2`; set it explicitly with `"range": { "version": 2 }`.

Supported columns:
- Dictionary-enabled columns of any type except MAP (INT, LONG, FLOAT, DOUBLE, STRING, BIG_DECIMAL, BYTES, BOOLEAN, TIMESTAMP). The dictionary can sit with a dictionary-encoded forward index or with a RAW forward index plus a standalone dictionary.
- Raw (no-dictionary) columns of numeric types only: INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL.
- A dictionary-encoded time column stored as STRING also works, since Pinot only supports lexicographically ordered datetime formats.

RAW forward index with a dictionary-backed range index needs the dictionary declared explicitly and version 2:
```
{ "name": "eventDate", "encodingType": "RAW", "indexes": { "dictionary": {}, "range": { "version": 2 } } }
```
Version 1 is rejected for RAW forward index plus dictionary; version 2 is the BitSliced range index and is required there.

Limitations:
- MAP columns are not supported.
- With the forward index disabled, the column must be single-valued and use range index version 2 for range queries to work.
- Non-numeric RAW columns need a dictionary.
- For no-dictionary ingestion-aggregated metric columns, version 2 is supported on committed segments. Adding the index to an older segment without min/max metadata for a raw INT or LONG column needs an extra scan of its forward index.

Older config: `tableIndexConfig.rangeIndexColumns` (list of column names).

## Checked

2026-11-08. Read the whole pinot-docs range-index page. Confirmed version default 2, BitSliced version 2, supported types, RAW plus dictionary rule, the forward-index-disabled limitation and the legacy list. Removed unsourced claims (time column as sortedColumn needs no range index, build-time comparison with inverted, reload after adding) and corrected "applies to RAW columns" to numeric RAW only.

Method: documentation only; no commands were run.
