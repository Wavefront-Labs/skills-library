---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.reload-search-analyzers-and-synonym-sets
name: reload-search-analyzers-and-synonym-sets
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, reload-search-analyzers, synonyms-api]
level: advanced
status: docs-checked
description: "Refresh synonym changes in Elasticsearch with the reload search analyzers API for updateable file-based filters, or with managed synonym sets."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-reload-search-analyzers
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-synonyms-put-synonym
  - https://www.elastic.co/docs/reference/text-analysis/analysis-synonym-graph-tokenfilter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update synonyms without downtime (Elasticsearch)

**Goal:** apply synonym edits live.
- File-based: mark the `synonym` or `synonym_graph` filter `"updateable": true` (default false) and use it only in search analyzers.
- Edit the synonym file on every data node, including nodes that hold no replica of the index (shards can relocate later), then `POST my-index/_reload_search_analyzers`. Needs the `manage` index privilege; works for data streams via backing indices.
- The reload runs once per node holding shards, so the `_shards` total can differ from the shard count. The response has `reload_details` with `index`, `reloaded_analyzers` and `reloaded_node_ids`.
- After reloading, clear the request cache so it holds no responses from the old analyzer.
- Managed synonym sets (Elasticsearch 8.10.0 and later): `PUT _synonyms/my-set` with `synonyms_set` rules in Solr format (each with optional `id`); reference it from the filter as `"synonyms_set": "my-set"` with `"updateable": true`. Updating a set reloads dependent search analyzers automatically for all indices (query `refresh` defaults to true). `append` (default false) appends instead of replacing the whole set. Needs the `manage_search_synonyms` cluster privilege.
- Limits: 100,000 rules per set by default (`synonyms.max_synonym_rules`); up to 100 sets per filter.
- The synonym set must exist before an index references it, otherwise the index is left partially created and inoperable.
- Failure mode: the file differs between nodes, so results vary by node.
- OpenSearch: not covered; its refresh-search-analyzer page could not be read.

## Verify
- [ ] Add a rule, call the reload API (or update the set), confirm `_analyze` on the search analyzer shows the new expansion.
- [ ] The same query returns the new synonym hit.

## Checked
Checked 2026-11-08 against the Elasticsearch "Reload search analyzers" and "Create or update a synonym set" API pages and the "Synonym graph token filter" page. Only Elasticsearch was checked. Removed: the claim that an `updateable` filter in an index-time analyzer is rejected (the pages say only that it must be used in search analyzers), the "existing tokens unaffected" statement, and the OpenSearch equivalence guess.
Method: documentation only; no commands were run.
