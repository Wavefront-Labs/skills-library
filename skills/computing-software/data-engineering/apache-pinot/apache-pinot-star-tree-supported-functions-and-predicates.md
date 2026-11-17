---
id: computing-software.data-engineering.apache-pinot.apache-pinot-star-tree-supported-functions-and-predicates
name: apache-pinot-star-tree-supported-functions-and-predicates
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, star-tree-index, distinctcounthll, tdigest, thetasketch, log2m, compressionfactor, nominalentries, predicate-support]
level: advanced
status: docs-checked
description: "What a star-tree can answer: supported aggregate functions and their parameters (HLL log2m, TDigest compressionFactor, theta nominalEntries), unsupported ones, predicate limits."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/star-tree-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Star-tree supported functions and predicates

Any aggregation function with a bounded-size intermediate result is supported. The docs list: COUNT, COUNTMV, MIN, MAX, SUM, SUMMV, ARRAYAGG (distinct aggregation over a single-value column only), SUM_PRECISION, AVG, AVGMV, MIN_MAX_RANGE, PERCENTILE_EST, PERCENTILE_RAW_EST, PERCENTILE_TDIGEST, PERCENTILE_RAW_TDIGEST, DISTINCT_COUNT_BITMAP (its RoaringBitmap is not bounded, so use carefully on high-cardinality columns), the HLL, HLL_PLUS, Theta, Tuple, CPC and ULL distinct-count families, and their RAW variants.

Parameters go in `aggregationConfigs[].functionParameters`:
- HyperLogLog: `log2m`, default **8** (larger means better accuracy and more memory).
- TDigest: `compressionFactor`, default **100** (values below 10 act as 10).
- HLL plus: `p` default 14 and `sp` default 0; for star-tree `sp` must be 0.
- Theta and Tuple sketches: `nominalEntries`, default **16384**. The nominalEntries used at query time must be less than or equal to the one used to build the tree.
- CPC sketch: `lgK`, default 12. ULL: `p`, default 12.
- SUM_PRECISION: `precision`.
The index is only used by queries with the same parameter value (for example log2m) as the tree.

Not supported (unbounded intermediate results): exact `DISTINCT_COUNT`, `SEGMENT_PARTITIONED_DISTINCT_COUNT` and exact `PERCENTILE`.

Predicate support:
- Supported: `=`, `!=`, `IN`, `NOT IN`, range comparisons (>, >=, <, <=, BETWEEN) and `AND`.
- Not supported: `REGEXP_LIKE` (would scan the whole dictionary) and `IS NULL` / `IS NOT NULL` (null info is not stored; the docs suggest comparing with the default value instead).
- `OR` only across predicates on the same dimension (otherwise double counting).
- `NOT` (since 1.2.0) only over a simple predicate, not on top of AND/OR.
- Transforms on a group-by column in the split order are fine; a transform on a predicate column prevents use of the tree.

A query benefits only when its filter columns, group-by columns and all aggregations match a star-tree config, so design trees around known query patterns. Every filtered or grouped column must be in `dimensionsSplitOrder`, and star-tree dimensions need dictionary values (a dictionary-encoded forward index, or a RAW one with an explicit shared dictionary).

## Checked

Confirmed against the Pinot docs page "Star-tree index": supported and unsupported function lists, parameter names and defaults, predicate support and limitations. Replaced the vague "and similar sketches" with the page's actual list and added the != / NOT IN / NOT support the page states. Reworded the reason for unsupported functions to "unbounded intermediate result".

Method: docs-only read of cited pages, 2026-11-08
