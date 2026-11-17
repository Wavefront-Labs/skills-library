---
id: computing-software.data-engineering.apache-pinot.apache-pinot-json-index-configuration
name: apache-pinot-json-index-configuration
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, json-index, json-match, json-extract-index, indexes-json, maxlevels, excludearray, includepaths, excludepaths, maxbytessize, skipinvalidjson]
level: advanced
status: docs-checked
description: "JSON index options (maxLevels, excludeArray, include and exclude paths, size limits), JSON_MATCH query syntax, and the cross-array unnest limit of 100000 combinations."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/json-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON index configuration

The JSON index flattens a JSON value so `JSON_MATCH` filters are indexed. It supports STRING and MAP columns (single-valued only) and is typically used with `noDictionaryColumns`, since JSON columns tend to have high cardinality.
```
{ "name": "attrs", "encodingType": "RAW", "indexes": { "json": {
   "maxLevels": 2, "excludeArray": false, "disableCrossArrayUnnest": true } } }
```

Keys under `indexes.json` (defaults in brackets):
- `maxLevels` [-1, unlimited]: levels to flatten; an array counts as one level.
- `excludeArray` [false].
- `disableCrossArrayUnnest` [false]: with unnesting on, two arrays of M and N elements produce M*N documents, and when the combinations reach 100k Pinot throws a "Got too many combinations" error. Set true to avoid it; then one JSON_MATCH call that queries more than one array returns an empty result (split it into separate JSON_MATCH calls joined with AND).
- `includePaths` / `excludePaths` [null]: sets such as `"$.a.b"`; mutually exclusive; paths under a listed path are included or excluded too.
- `excludeFields` [null]: exclude fields such as `"b"` even under included paths.
- `indexPaths` [null, same as **]: patterns such as `*.*` or `a.**`.
- `maxValueLength` [0, disabled]: a node value longer than this is replaced with `$SKIPPED$` before indexing.
- `maxBytesSize` [null, no limit]: approximate on-heap byte budget for the mutable JSON index in real-time ingestion; growth stops at the limit (posting lists are excluded, so it is a guardrail, not an exact cap).
- `skipInvalidJson` [false]: replace ill-formed JSON with an empty key/path and `$SKIPPED$` value instead of throwing.

Query:
```
SELECT * FROM t WHERE JSON_MATCH(attrs, '"$.user.id" = 42')
```
The docs also show IN, !=, NOT IN, REGEXP_LIKE, range, BETWEEN, IS NULL / IS NOT NULL, and array index forms such as `"$.addresses[0].number"`.

`JSON_EXTRACT_INDEX(<column>, '<jsonPath>', ['resultsType'], ['filter'])` extracts values using the index; the path must be covered by `includePaths` or `indexPaths` if you restrict them. Setting the query option `useIndexBasedDistinctOperator=true` lets SELECT DISTINCT on a JSON path use the index; `jsonIndexDistinctSkipMissingPath=true` additionally drops missing-path rows. The feature is off by default.

## Checked

Confirmed against the Pinot docs page "JSON index": supported column types, every key and default in the config table, the 100k combinations error, JSON_MATCH and JSON_EXTRACT_INDEX forms, and the DISTINCT query options. Corrected "exceeding 100000" to "reach 100k" and dropped the unsourced advice that includePaths is preferred for size, and the `maxValueLength: 100` example value.

Method: docs-only read of cited pages, 2026-11-08
