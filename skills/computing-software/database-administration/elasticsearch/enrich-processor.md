---
id: computing-software.database-administration.elasticsearch.enrich-processor
name: enrich-processor
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, ingest-pipeline, enrich-processor, enrich-policy, match-policy, geo-match, range-policy, lookup-at-ingest, execute-policy]
level: advanced
status: docs-checked
description: "Add lookup data (customer tier, asset owner, IP range metadata) to documents at ingest with Elasticsearch enrich policies and the enrich processor, and keep the lookup fresh."
sources:
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/ingest-processor/enrich-processor.md
  - https://github.com/elastic/docs-content/blob/main/manage-data/ingest/transform-enrich/data-enrichment.md
  - https://github.com/elastic/docs-content/blob/main/manage-data/ingest/transform-enrich/example-enrich-data-based-on-exact-values.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enrich processor

**Goal:** documents arrive with joined reference data, since Elasticsearch has no
query-time joins worth using at scale.

## 1. Source index with reference data
```json
PUT customers/_doc/c-42 { "customer_id": "c-42", "tier": "gold", "region": "eu-west", "account_manager": "Ana" }
```

## 2. Enrich policy
```json
PUT _enrich/policy/customer-lookup
{ "match": { "indices": "customers", "match_field": "customer_id",
             "enrich_fields": ["tier", "region", "account_manager"] } }
POST _enrich/policy/customer-lookup/_execute
```
Policy types: `match`, `range` and `geo_match`. Executing the policy builds an enrich index: a read-only, force-merged system index whose name starts with `.enrich-`, used by the enrich processor for fast lookups.

## 3. Use in a pipeline
```json
PUT _ingest/pipeline/orders-enrich
{ "processors": [
  { "enrich": { "policy_name": "customer-lookup", "field": "customer.id",
                "target_field": "customer.info", "max_matches": 1, "ignore_missing": true } } ] }
```

## Keeping it fresh
The enrich index is built from the source indices when the policy is executed, so later updates to
`customers` are not seen until you re-run `_execute`. Schedule it (cron, Watcher,
or an external job) at the freshness the use case needs.

## Gotchas
- Processor options: `max_matches` defaults to 1 (a larger value turns `target_field` into an array), `ignore_missing` defaults to false, `override` defaults to true, and `shape_relation` (default `INTERSECTS`) applies to `geo_match` policies only.
- Already-indexed documents are not re-enriched; reprocess them through the pipeline (for example `_update_by_query` with `?pipeline=`) if needed.

## Verify
`POST _ingest/pipeline/orders-enrich/_simulate` with a known customer id shows
`customer.info.tier`; `GET _enrich/policy/customer-lookup` lists the policy and its last execution.

## Checked

Checked 2026-10-25 against elastic/elasticsearch and elastic/docs-content `main` (Stack 9.x docs). Confirmed: policy types, that a policy must be executed before use, enrich index properties (`.enrich-*`, read-only, system index, force merged), processor parameters and defaults. Removed unconfirmed claims: replication of the enrich index to every node, index swapping on re-execution, heap cost guidance, in-place policy update rules and `_enrich/_stats` fields.

Method: documentation only; no commands were run.
