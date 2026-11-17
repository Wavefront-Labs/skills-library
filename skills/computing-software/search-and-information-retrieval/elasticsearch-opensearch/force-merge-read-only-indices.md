---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.force-merge-read-only-indices
name: force-merge-read-only-indices
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, force-merge-read-only-indices]
level: advanced
status: docs-checked
description: "Use _forcemerge with max_num_segments on indices no longer written to; avoid it on active indices."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge
  - https://www.elastic.co/docs/reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Force merge read-only indices

**Goal:** fewer segments for read-heavy cold data.
- `POST my-index/_forcemerge?max_num_segments=1` only after the index no longer receives writes (for example `index.blocks.write: true`, or rolled over). Needs the `maintenance` index privilege.
- It is resource-intensive; run off-peak. By default the call blocks until done; `wait_for_completion=false` returns a task id (that task cannot be cancelled).
- With `max_num_segments=1` a shard may temporarily need up to three times its size in free disk.
- Lucene only auto-merges segments up to 5 GB; a force merge can create larger segments that regular merges will not reprocess, so soft-deleted documents accumulate and hurt disk use and search. On indices still being written, snapshots also become costlier.
- Each shard merges on the `force_merge` threadpool (size `max(1, allocatedProcessors / 8)`); raise `thread_pool.force_merge.size` gradually if merges back up.
- `only_expunge_deletes=true` removes deleted documents only; `flush` defaults to true.
- ILM runs it as the `forcemerge` action in the hot (only with `rollover`) or warm phase; `max_num_segments` is required. `index_codec: best_compression` makes ILM close and reopen the index around the merge.
- Applying a forcemerge policy to many existing indices at once can strain the cluster; raise `min_age` or set `index.lifecycle.origination_date`.
- Failure mode: force merging an index still receiving writes.

## Verify
- [ ] `GET _cat/segments/my-index?v` shows the segment count reduced.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch force merge API reference and ILM forcemerge action pages in full; OpenSearch was not checked.
