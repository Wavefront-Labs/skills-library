---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.bulk-indexing-tuning
name: bulk-indexing-tuning
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, bulk-indexing-tuning, es-perf-indexing]
level: advanced
status: docs-checked
description: "Raise indexing speed with larger bulks, parallel clients, less replicas during load and no per-document refresh."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-stats.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tune bulk indexing throughput

**Goal:** faster ingestion.
- Size bulk requests by benchmark on one node with one shard: start at 100 documents, then double (200, 400, ...) until speed plateaus, erring towards fewer documents; stay under a couple of tens of MB per request.
- Send from several workers and raise the count until I/O or CPU saturates; on `429` (`TOO_MANY_REQUESTS`) pause and retry with randomized exponential backoff.
- Initial load: `index.number_of_replicas` 0 (data must live elsewhere so the load can be retried) and `index.refresh_interval` `-1`; restore both afterwards, and consider a force merge (expensive).
- Use auto-generated ids when you do not need your own: an explicit id forces a per-shard existence check.
- Disable swapping and prefer SSDs; give at least half of system memory to the filesystem cache.
- `indices.memory.index_buffer_size` defaults to 10% of heap; beyond about 512 MB per heavily indexing shard it rarely helps.
- Failure mode: changing settings and forgetting to restore them.

## Verify
- [ ] Indexing rate in `GET _nodes/stats/indices/indexing` rises while write rejections stay at zero.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited page is the Elasticsearch guide; OpenSearch defaults may differ.

## Checked
2026-11-08. Read the Elasticsearch "Tune for indexing speed" page in full and checked every tuning claim above against it; the `_nodes/stats` indexing metric against the nodes stats API page. Removed the unsupported "a few MB" bulk size.
Method: documentation only; no commands were run.
