---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.profile-api-slow-queries
name: profile-api-slow-queries
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, profile-api-slow-queries]
level: advanced
status: docs-checked
description: "Add profile:true to a search to see time spent by query component, collector and aggregation per shard."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/search-profile
  - https://docs.opensearch.org/latest/api-reference/search-apis/profile/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profile a slow query

**Goal:** find which clause costs the time.
- `GET my-index/_search {"profile":true,"query":{...}}` returns, per shard, a `searches` list whose `query` entries carry `time_in_nanos`, a `breakdown` (OpenSearch's example shows `next_doc`, `advance`, `score`, `build_scorer` and matching `_count` fields) and nested `children`. A query's `time_in_nanos` includes the time of all its children, so compare siblings rather than adding parents and children. Collectors appear in a `collector` list.
- Aggregations have their own profile section: send an aggregation request with `profile` set to true.
- The Profile API is a debugging tool and adds significant overhead to search execution (Elasticsearch); OpenSearch likewise calls it resource-consuming. Do not leave it on for production traffic.
- It does not measure network latency, time spent in queues, or time merging shard responses on the coordinating node, so a slow request may be slow outside what the profile shows.
- Work from the biggest child time downwards, then try a cheaper rewrite of that clause and profile again.
- Failure mode: treating the profile as the whole request latency.

## Verify
- [ ] After a rewrite, the profiled time of the offending clause drops.

## Checked

2026-11-08. Confirmed against the Elasticsearch Profile API page (overhead, what is not measured, inclusive child times) and the OpenSearch Profile API page (overhead, breakdown fields, collector, aggregation profiling). Removed the list of expensive clause types (wildcards, scripts, large terms lists) and the cold versus warm cache explanation as unsupported by those pages, and the "unconfirmed" notes.
Method: documentation only; no commands were run.
