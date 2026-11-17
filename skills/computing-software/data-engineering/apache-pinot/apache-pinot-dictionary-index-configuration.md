---
id: computing-software.data-engineering.apache-pinot.apache-pinot-dictionary-index-configuration
name: apache-pinot-dictionary-index-configuration
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, dictionary-index, indexes-dictionary, optimizedictionary, optimizedictionaryformetrics, nodictionarysizeratiothreshold, usevarlengthdictionary, onheap, nodictionarycolumns, intern]
level: advanced
status: docs-checked
description: "Dictionary index options: disabling, standalone dictionaries over RAW columns, optimizeDictionary heuristics, onHeap, var-length, intern."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/dictionary-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dictionary index configuration

Dictionary encoding is on by default, assuming unique values are far fewer than rows. It suits low to medium cardinality; for high-cardinality columns (UUIDs, free text) disabling it and using RAW may save space. Supported on all data types.

Turn it off per column, either way (but define a column's index in one place only, Pinot rejects the same column and index defined in different locations):
```
{ "name": "col1", "indexes": { "dictionary": { "disabled": true } } }
{ "name": "col1", "encodingType": "RAW" }
```

A RAW forward index can still get a **standalone dictionary** when another index needs dictionary IDs or values (bitmap inverted, FST/IFST). Declare it explicitly:
```
{ "name": "myColumn", "encodingType": "RAW", "indexes": { "dictionary": {}, "inverted": {} } }
```
Legacy `tableIndexConfig.noDictionaryColumns` and `noDictionaryConfig` still disable the dictionary and cause such configs to be rejected; remove the column from them. Effects on other indexes: JSON and text indexes disable the dictionary when `optimizeDictionary` is on; H3 is incompatible with a dictionary.

Heuristic (in the table's `indexingConfig`, applies to all columns of the table):
- `optimizeDictionary` (default false): enables the heuristic for all columns and some extra rules. Takes precedence over `optimizeDictionaryForMetrics`.
- `optimizeDictionaryForMetrics` (default false): the heuristic for metric columns only.
- `noDictionarySizeRatioThreshold` (default **0.85**): the saving ratio. Pinot computes raw-size over dictionary-encoded size for candidate columns; below the ratio the dictionary is not created.
- `optimizeDictionaryType` (default false): for variable-width columns, uses fixed-width dictionaries when all values in a segment have the same length. It does not disable dictionaries.
- Candidates: dictionary-encoded, single-valued, fixed-size types (int, long, double, timestamp); variable-size types and columns with text or JSON indexes are never considered.

Dictionary options in `indexes.dictionary`:
- `onHeap` (default false): dictionary data is always off-heap; copying it on heap avoids per-access deserialization for strings or bytes but not recommended, as it raises heap use and GC time and costs memory per concurrently accessed segment.
- `useVarLengthDictionary` (default false): by default Pinot sizes all values to the largest value in the segment; set true if you have a few very large values and many small ones, at an extra 4 bytes of offset per entry.
- `intern.capacity` (default null): on-heap only; caches dictionary values across segments of the same table and column. Only string and byte columns can be interned; other types ignore it.

## Checked

2026-11-08. Read the whole pinot-docs dictionary-index page. Confirmed the disable forms, standalone dictionary, legacy conflict, heuristic parameters and defaults, candidate rules and dictionary options. Corrected the heuristic location (`indexingConfig`, not `tableIndexConfig`), optimizeDictionaryType (fixed-width versus variable-width storage, not "pick the dictionary type") and the threshold meaning.

Method: documentation only; no commands were run.
