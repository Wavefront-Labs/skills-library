---
id: computing-software.data-engineering.apache-pinot.apache-pinot-bloom-filter-index
name: apache-pinot-bloom-filter-index
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, bloom-filter, indexes-bloom, fpp, maxsizeinbytes, loadonheap, bloomfiltercolumns, bloomfilterconfigs, segment-pruning]
level: practitioner
status: docs-checked
description: "Bloom filter index to prune segments on equality: fpp, maxSizeInBytes, loadOnHeap, supported predicates and unsupported types."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/bloom-filter.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bloom filter index

Pinot creates one Bloom filter per segment for each configured column. A server skips a whole segment when the filter shows the value is certainly absent (a Bloom filter gives false positives, never false negatives). Bloom filters are off by default; a column is indexed only when configured in the table config.

In `fieldConfigList`:
```
{ "name": "memberId", "encodingType": "RAW", "indexes": { "bloom": { "fpp": 0.05, "maxSizeInBytes": 0, "loadOnHeap": false } } }
```
`"bloom": {}` enables it with defaults.

Parameters (all optional):
- `fpp`: false positive probability, 0 to 1, default **0.05**. Lower is more accurate but makes the index larger.
- `maxSizeInBytes`: default **0** (unlimited). It takes precedence over `fpp`: if the size computed from `fpp` exceeds a non-zero cap, Pinot raises the effective `fpp` to stay within the cap.
- `loadOnHeap`: default **false** (off-heap memory); true uses heap memory.
- The special parameter `disabled: true` explicitly deactivates the index.

The size of a Bloom filter depends on the number of unique values expected per segment.

Supported predicates: equality and `IN`; `IN` support is limited to **10 or fewer** values so pruning overhead stays minimal. It does not accelerate range queries, `LIKE` or other filters. No special query syntax is needed.

Column types: all types except `BOOLEAN` and `MAP`.

Older config: `tableIndexConfig.bloomFilterColumns` (list of columns, default settings) and `tableIndexConfig.bloomFilterConfigs` (map of column to `fpp` / `maxSizeInBytes` / `loadOnHeap`).

Best for lookup columns (IDs) on tables with many segments, where most segments do not contain the searched key.

## Checked

2026-11-08. Read the whole pinot-docs bloom-filter page. Confirmed the defaults (fpp 0.05, maxSizeInBytes 0 unlimited, loadOnHeap false), maxSizeInBytes precedence over fpp, the 10-value IN limit, the unsupported BOOLEAN and MAP types, the `disabled` parameter and the legacy keys. Removed the unsourced remark about low-cardinality columns and replaced "memory mapped" with the documented off-heap wording.

Method: documentation only; no commands were run.
