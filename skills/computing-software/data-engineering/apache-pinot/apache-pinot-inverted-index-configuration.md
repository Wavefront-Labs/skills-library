---
id: computing-software.data-engineering.apache-pinot.apache-pinot-inverted-index-configuration
name: apache-pinot-inverted-index-configuration
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, inverted-index, indexes-inverted, invertedindexcolumns, createinvertedindexduringsegmentgeneration, sorted-inverted-index, fieldconfiglist]
level: practitioner
status: docs-checked
description: "Enabling inverted indexes with indexes.inverted, RAW plus dictionary form, legacy invertedIndexColumns, sorted inverted index."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/inverted-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inverted index configuration

An inverted index maps values to the set of document IDs that contain them. Add one to columns that appear frequently in WHERE filters, especially equality and membership predicates; it is a good starting point for performance tuning.

Recommended config, in `fieldConfigList`:
```
{ "name": "playerName", "indexes": { "inverted": {} } }
```

Bitmap inverted indexes need dictionary IDs. To keep the forward index RAW, declare a standalone dictionary alongside:
```
{ "name": "playerName", "encodingType": "RAW", "indexes": { "dictionary": {}, "inverted": {} } }
```
Do not leave the column in legacy `tableIndexConfig.noDictionaryColumns` or `noDictionaryConfig`; those still disable the dictionary and Pinot rejects the table config.

Supported types: all except MAP (INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL, BOOLEAN, TIMESTAMP, STRING, JSON, BYTES), single-value and multi-value.

Creation time: inverted indexes are always built during segment generation when configured. The legacy `indexingConfig.createInvertedIndexDuringSegmentGeneration` flag (which defaulted to false) is no longer honored, per the page's note about Apache Pinot PR 17951.

Legacy config: `tableIndexConfig.invertedIndexColumns` (list of column names).

Sorted inverted index:
- A column that is both sorted and dictionary-encoded uses a sorted forward index with run-length encoding that doubles as an inverted index. It is automatic, needs no config, and gives `O(log n)` lookup with data locality (binary search for the matching document range).
- It only works on columns physically sorted within each segment, and performs better than a bitmap inverted index.
- From Pinot 1.3.0 a raw (no-dictionary) column can be a sorted column without forcing a dictionary or inverted index.

## Checked

2026-11-08. Read the whole pinot-docs inverted-index page. Confirmed supported types, fieldConfigList forms, the noDictionary conflict, the ignored createInvertedIndexDuringSegmentGeneration flag, sorted inverted index behaviour and the 1.3.0 raw sorted columns note. Removed the unsourced "builds on reload without re-ingesting" and the low-cardinality guidance; corrected "requires a dictionary-encoded column" (a standalone dictionary with a RAW forward index also works).

Method: documentation only; no commands were run.
