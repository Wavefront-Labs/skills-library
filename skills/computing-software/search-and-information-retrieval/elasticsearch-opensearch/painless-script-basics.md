---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.painless-script-basics
name: painless-script-basics
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, painless-script-basics, es-painless-scripting]
level: advanced
status: docs-checked
description: "Write Painless scripts with params, test them with the execute API and know the script cache, size limit and search-speed cost."
sources:
  - https://www.elastic.co/docs/explore-analyze/scripting/modules-scripting-using
  - https://www.elastic.co/docs/explore-analyze/scripting/scripts-search-speed
  - https://docs.opensearch.org/latest/api-reference/script-apis/exec-script/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Painless script basics and safety

**Goal:** fast, cached scripts.
- Script shape wherever scripting is supported (Elasticsearch): `"script": {"lang": "painless", "source" | "id": "...", "params": {...}}`. `lang` defaults to `painless`; `source` is an inline script and `id` a stored one. Pass values through `params` instead of hard-coding them to decrease compile time.
- Compiled scripts are cached so repeated requests skip compilation. Size the cache (`script.cache.max_size`) to hold the scripts used concurrently; many cache evictions plus rising compilations in node stats suggest it is too small. Scripts have no time-based expiry by default (`script.cache.expire` changes that).
- Script size is limited to 65,535 bytes; `script.max_size_in_bytes` raises the soft limit (Elasticsearch).
- In a script query or sort, read field values through `doc['field'].value` (the OpenSearch filter-context example does this).
- Scripts cannot use index structures or related optimisations, so searching with one can be slower. If you often transform indexed data in scripts, compute it at ingest instead (for example an ingest `script` processor writing `ctx.total_score`, then sort on that field), at the cost of slower indexing.
- Test with `POST _scripts/painless/_execute` (OpenSearch also accepts GET). It runs an inline script only (no stored `id`); the default `painless_test` context exposes only `params` and returns the result as a string; the `filter` context takes a test document and an index name (a single index, no wildcards) in `context_setup` and exposes `doc`.
- Do not build script text from user input; pass user values as `params`.

## Verify
- [ ] `_scripts/painless/_execute` returns the expected value for a sample context.

## Checked

2026-11-08. Confirmed against the Elasticsearch pages How to write Painless scripts and Scripts, caching, and search speed, and the OpenSearch Execute Inline Script API page. Removed `script.max_compilations_rate` and its circuit-breaker error text, the claim that `params._source` is slower, and the missing-doc-values claim for text fields, none of which those pages state.
Method: documentation only; no commands were run.
