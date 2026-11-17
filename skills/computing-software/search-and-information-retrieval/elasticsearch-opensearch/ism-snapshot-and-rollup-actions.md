---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.ism-snapshot-and-rollup-actions
name: ism-snapshot-and-rollup-actions
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, ism-snapshot-and-rollup-actions]
level: advanced
status: docs-checked
description: "Combine OpenSearch ISM snapshot and rollup actions with transform jobs to retain summarised data."
sources:
  - https://docs.opensearch.org/latest/im-plugin/ism/policies-operations/
  - https://docs.opensearch.org/latest/im-plugin/index-rollups/index/
  - https://docs.opensearch.org/latest/im-plugin/index-transforms/index/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ISM snapshot, rollup and transform

**Goal:** keep old data cheaply.
- ISM `snapshot` action: `repository` (required, must already be registered with the native snapshot API) and `snapshot` (required name; Mustache `{{ctx.index}}` and `{{ctx.indexUuid}}` allowed; invalid variables fall back to the index name).
- ISM `rollup` action defines the job in an `ism_rollup` object and can only be non-continuous. Transform is not in the ISM operations list; run transforms as their own jobs.
- Rollups (`PUT _plugins/_rollup/jobs/<id>`) compress old time-series into a coarser target index: a `date_histogram` dimension (optionally `terms`, `histogram`) and numeric metrics (avg, sum, max, min, value_count, cardinality). Source and target cannot change after creation; the target is created on the first run (`_explain` with null `rollup_metadata` means it has not run).
- Queries on the rollup index must fit its dimensions and metrics or return 400; mixing rolled-up and live data in one query can double-count the overlap.
- Transforms (`PUT _plugins/_transform/<id>`) write a differently organised summary: `groups` (histogram, date_histogram, terms) plus aggregations (sum, avg, max, min, value_count, percentiles, scripted_metric), optional source filter, continuous or one-shot. Groups and aggregations cannot change afterwards; check with `_explain`.
- `convert_index_to_remote` restores an index from a snapshot made by the snapshot action to a remote repository; `delete_original_index: true` removes the original once accepted.
- Order: rollup first, then delete the raw index only after verification.
- Failure mode: deleting raw data before checking the rollup target.

## Verify
- [ ] Aggregations on the rollup index match the same aggregation on the raw data for a sample window.

## Checked
Date: 2026-11-08
Method: Read the OpenSearch ISM operations page (snapshot, rollup sections), index rollups page and index transforms page in their body chunks; part of the rollups page past 200000 characters was not read. Elasticsearch was not checked.
