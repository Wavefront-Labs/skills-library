---
id: computing-software.data-engineering.apache-pinot.apache-pinot-star-tree-index-configuration
name: apache-pinot-star-tree-index-configuration
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, star-tree-index, startreeindexconfigs, dimensionssplitorder, skipstarnodecreationfordimensions, functioncolumnpairs, aggregationconfigs, maxleafrecords, enabledefaultstartree]
level: advanced
status: docs-checked
description: "Configuring a Pinot star-tree index: dimensionsSplitOrder, functionColumnPairs vs aggregationConfigs, maxLeafRecords and the default tree."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/star-tree-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Star-tree index configuration

A star-tree pre-aggregates data across dimension combinations, giving a configurable space/time trade-off and a hard upper bound on query latency for a given use case.
```
"tableIndexConfig": { "starTreeIndexConfigs": [{
  "dimensionsSplitOrder": ["Country", "Browser", "Locale"],
  "skipStarNodeCreationForDimensions": [],
  "functionColumnPairs": ["SUM__Impressions", "COUNT__*"],
  "maxLeafRecords": 10000
}]}
```
Several configs in the list generate several star-trees.

Keys:
- `dimensionsSplitOrder`: ordered dimension list; nodes split level by level in this order and only these dimensions are kept. **Every filter and group-by column of a query must be in this list** for the tree to be used. The dimension can also be a time, date-time or metric column. Each must have dictionary values: a dictionary-encoded forward index, or a RAW forward index plus an explicit shared dictionary in `fieldConfigList` (not via legacy `noDictionaryColumns`).
- `skipStarNodeCreationForDimensions`: optional, default empty; dimensions that get no star node.
- `functionColumnPairs`: `FUNCTION__column` pairs split by a double underscore, for example `SUM__Impressions` or `COUNT__*`.
- `aggregationConfigs`: interchangeable with `functionColumnPairs` and preferable because it takes more parameters. Each entry has `columnName` and `aggregationFunction` (required), plus optional `compressionCodec` (default `PASS_THROUGH`, e.g. `LZ4` for big BYTES sketches) and `functionParameters` (e.g. `{"log2m": 16}` for `DISTINCTCOUNTHLL`; the index is used only by queries with the same parameter value).
- `maxLeafRecords`: optional, default **10000**; the threshold T deciding whether a node is split further.
- `nullHandlingEnabled`: optional, default `false`; builds a null-aware star-tree, used only by queries that enable null handling.
- All aggregations in a query must be covered by the pairs or configs, or the tree is not used.

Default tree: `"enableDefaultStarTree": true` under `tableIndexConfig` builds one automatically. It uses dictionary-encoded single-value dimensions with cardinality up to 10000 (highest cardinality first), then time columns, `COUNT(*)` and `SUM` for numeric metrics, and `maxLeafRecords` 10000.

Gotchas: `REGEXP_LIKE` filters are unsupported by the star-tree, and star-trees cannot be used on upsert tables.

## Checked

2026-11-09. Read the Pinot docs page `star-tree-index.md` (index generation configuration, AggregationConfigs, default configuration, predicates and limitations sections). Confirmed every key, default and the default-tree rules above. Removed: advice to order split dimensions by cardinality, the claim that lower maxLeafRecords gives faster queries, and the "reload and EXPLAIN PLAN" step, none of which the page states.
Method: documentation only; no commands were run.
