---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.composite-aggregation-pagination
name: composite-aggregation-pagination
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, composite-aggregation-pagination]
level: advanced
status: docs-checked
description: "Page through all buckets with composite sources and after_key, for exports and exact distinct enumeration."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-composite-aggregation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite aggregation paging

**Goal:** iterate through every bucket.
- `{"aggs":{"c":{"composite":{"size":1000,"sources":[{"day":{"date_histogram":{"field":"@timestamp","calendar_interval":"1d"}}},{"brand":{"terms":{"field":"brand"}}}]}}}}`.
- `size` is exactly the number of composite buckets returned (default 10); to retrieve everything, use a small size (100 or 1000) and page.
- Resend the same aggregation with `"after"` set to the `after_key` from the response to get the next page. Always use the returned `after_key` rather than deriving it from the last bucket.
- The order of `sources` controls the order of the keys returned; source names must be unique.
- Failure mode: not passing the full `after_key` repeats or skips buckets.

## Verify
- [ ] Sum of pages' doc counts equals the total hit count.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited page is the Elasticsearch composite aggregation page; OpenSearch was not checked here.

## Checked
2026-11-08. Read the Elasticsearch composite aggregation page (value sources, `size` default 10, Pagination section, `after_key` note). Replaced "the supported way to page aggregations" (not stated) with the documented pagination guidance.
Method: documentation only; no commands were run.
