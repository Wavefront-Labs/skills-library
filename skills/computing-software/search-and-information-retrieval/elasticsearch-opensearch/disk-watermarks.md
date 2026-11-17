---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.disk-watermarks
name: disk-watermarks
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, disk-watermarks]
level: advanced
status: docs-checked
description: "Understand low, high and flood-stage watermarks and recover from the read-only-allow-delete block."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk watermarks and read-only indices

**Goal:** keep nodes from filling disk.
- Settings (dynamic): `cluster.routing.allocation.disk.watermark.low` (default 85%), `.high` (default 90%) and `.flood_stage` (default 95%). Each can be a percentage, a ratio such as 0.9, or an absolute free-space value such as `500mb`.
- Low: Elasticsearch will not allocate shards to a node over the threshold; it has no effect on primaries of newly created indices but blocks their replicas. High: Elasticsearch tries to relocate shards away from the node, and the setting affects all shards. Flood stage: a last resort that enforces `index.blocks.read_only_allow_delete` on every index with a shard on a node that has a disk over the threshold.
- The flood stage block is released automatically when disk usage falls below the high watermark, so free space first (delete or move indices).
- `.max_headroom` settings cap the free space required when a watermark is a percentage (defaults 200GB low, 150GB high, and a flood stage cap); they have defaults only if the matching watermark is not set explicitly.
- Setting `cluster.routing.allocation.disk.threshold_enabled` to false disables the disk decider and removes existing `read_only_allow_delete` blocks; treat it as a last resort.
- Failure mode: raising watermarks without adding capacity just delays the incident.

## Verify
- [ ] Disk use on every data node is below the low watermark and writes succeed.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited page is Elasticsearch; OpenSearch was not checked here.

## Checked
2026-11-08. Read the Elasticsearch cluster-level shard allocation settings page (watermark defaults, ratio and absolute forms, low/high/flood behaviour, automatic block release, max headroom). Removed the manual `PUT my-index/_settings` block removal and the `_cat/allocation` command, which were not on the page read.
Method: documentation only; no commands were run.
