---
id: computing-software.search-and-information-retrieval.apache-solr.pagination-start-rows
name: pagination-start-rows
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [pagination, start-rows, queryresultcache, queryresultwindowsize, paging]
level: intro
status: docs-checked
description: "Page through Solr results with start and rows, understand queryResultCache and queryResultWindowSize, and know when deep paging with start becomes costly."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/pagination-of-results.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pagination-start-rows

Basic pagination uses `rows` (page size) and `start` (zero-based offset). Compute `start = page_number * rows_per_page` with the first page numbered 0.

The guide says performance of this common pattern can be tuned with the `queryResultCache` and by adjusting the `queryResultWindowSize` setting to your expected page sizes.

Limits: deep offsets make every request sort and discard all earlier results, and on a sharded collection each shard must return `start + rows` entries. For stable and cheap deep paging use `cursorMark` instead (see the cursor skill). `start` and `cursorMark` are mutually exclusive.

When results can change between requests (updates, merges) pages may overlap or skip; cursors with a total sort order avoid that.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Pagination of Results page: `start = page_number * rows_per_page` with page 0 first, the `queryResultCache` and `queryResultWindowSize` tuning sentence, overlap and skipped documents after index changes, deep paging cost per shard, and cursor mutual exclusion with `start`. The claim that Solr caches a window of document ids was not stated on that page and was left as the general tuning note only.

Method: documentation only; no commands were run.
