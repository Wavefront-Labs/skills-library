---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.boosting-query-demotion
name: boosting-query-demotion
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, boosting-query-demotion]
level: advanced
status: docs-checked
description: "Use the boosting query with positive, negative and negative_boost to demote rather than exclude documents."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-boosting-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# boosting query to demote results

**Goal:** push down (not remove) unwanted results.
```
{"query":{"boosting":{"positive":{"match":{"title":"apple"}},"negative":{"term":{"category":"fruit-juice"}},"negative_boost":0.3}}}
```
- `positive` and `negative` and `negative_boost` are all required. Returned documents must match `positive`; a document that also matches `negative` has its `positive` score multiplied by `negative_boost`.
- `negative_boost` is a float between `0` and `1.0`.
- Differs from `must_not`, which excludes matching documents; `boosting` demotes them without excluding them.

## Verify
- [ ] The demoted documents appear lower but are still returned.

## Scope
The Elasticsearch reference page was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference Boosting query page. Confirmed: required parameters, the score multiplication, the `0` to `1.0` range, demote-not-exclude. Removed: the claim that a `negative_boost` of 1 or more "does not demote" (the page only documents `0` to `1.0`) and the OpenSearch source root.

Method: documentation only; no commands were run.
