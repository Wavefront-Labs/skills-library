---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.optimistic-concurrency-control
name: optimistic-concurrency-control
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, optimistic-concurrency-control]
level: advanced
status: docs-checked
description: "Use if_seq_no and if_primary_term (or external versioning) to prevent lost updates on concurrent writes."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/optimistic-concurrency-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimistic concurrency control

**Goal:** safe read-modify-write.
- Every operation on a document gets a sequence number from the primary shard, increasing with each operation. Document responses (index and GET) include `_seq_no` and `_primary_term`; the Search API can return them per hit with the `seq_no_primary_term` parameter.
- Conditional write: `PUT my-index/_doc/1?if_seq_no=5&if_primary_term=1` changes the document only if no other change was made since you read those values. The `if_seq_no` and `if_primary_term` parameters work on the index, update and delete APIs.
- They are rejected on indices that disable sequence numbers with `index.disable_sequence_numbers`.
- Failure mode: blind overwrites by two workers lose changes.

## Verify
- [ ] Two parallel conditional writes with the same `_seq_no`: only one succeeds.

## Scope
The Elasticsearch reference page was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference page Optimistic concurrency control. Confirmed: `_seq_no` and `_primary_term`, `if_seq_no` and `if_primary_term`, the `index.disable_sequence_numbers` warning. Removed: the HTTP 409 and `version_conflict_engine_exception` wording, `retry_on_conflict` and external versioning with `version_type=external` (none appear in the docs source read), and the OpenSearch source root.

Method: documentation only; no commands were run.
