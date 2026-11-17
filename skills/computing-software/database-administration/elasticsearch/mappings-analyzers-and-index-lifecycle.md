---
id: computing-software.database-administration.elasticsearch.mappings-analyzers-and-index-lifecycle
name: mappings-analyzers-and-index-lifecycle
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, elastic-stack, mapping, explicit-mapping, dynamic-mapping, mapping-explosion, keyword, text, multi-fields, analyzer, tokenizer, token-filter, analyze-api, index-template, component-template, ilm, index-lifecycle-management, ism, index-state-management, rollover, data-streams, shard-sizing, hot-warm-cold, reindex, aliases, full-text-search]
level: practitioner
status: docs-checked
description: "Design explicit Elasticsearch/OpenSearch mappings and analyzers, test with _analyze, size shards at 10-50GB, and automate rollover/retention with ILM or OpenSearch ISM."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/size-your-shards.html
  - https://opensearch.org/docs/latest/im-plugin/ism/index/
  - https://github.com/elastic/elasticsearch/tree/main/docs/reference/elasticsearch/mapping-reference
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Mappings, analyzers and index lifecycle — Elasticsearch and OpenSearch

**Goal:** indices whose field types and analysis are chosen on purpose, shards in a
healthy size range, and old data rolled over, shrunk and deleted automatically.

## 1. Explicit mappings in index templates
Dynamic mapping guesses field types from the first value seen, and arbitrary JSON keys cause
**mapping explosion** (cap it with `index.mapping.total_fields.limit`). Map
deliberately:
```json
PUT _index_template/logs-app
{
  "index_patterns": ["logs-app-*"],
  "data_stream": {},
  "template": {
    "settings": { "number_of_shards": 1, "number_of_replicas": 1,
                  "index.lifecycle.name": "logs-30d" },
    "mappings": {
      "dynamic": "strict",
      "properties": {
        "@timestamp": { "type": "date" },
        "service":    { "type": "keyword" },
        "status":     { "type": "short" },
        "message":    { "type": "text", "fields": { "raw": { "type": "keyword", "ignore_above": 512 } } },
        "attrs":      { "type": "flattened" }
      }
    }
  }
}
```
- `keyword` for exact match, aggregations, sorting (IDs, enums, hostnames);
  `text` for full-text search. Need both? multi-fields.
- Numbers you never range-query (IDs, ZIP codes) are better as `keyword`.
- `dynamic: strict` rejects unknown fields; `false` ignores new fields (not indexed or
  searchable, still in `_source`); `flattened` maps a whole object as one field of keywords.
- You cannot change an existing field's type. Create a new index and `_reindex`, behind
  an alias so clients don't change.
- Split templates into `component_template`s (settings, mappings) and compose them.

## 2. Analyzers: test before you index
```json
PUT products
{ "settings": { "analysis": {
    "filter":   { "en_stem": { "type": "stemmer", "language": "light_english" } },
    "analyzer": { "en_text": { "tokenizer": "standard",
                   "filter": ["lowercase", "asciifolding", "en_stem"] } } } },
  "mappings": { "properties": { "title": { "type": "text", "analyzer": "en_text" } } } }

POST products/_analyze
{ "analyzer": "en_text", "text": "Crème Brûlée Recipes" }
```
Check the emitted tokens. Changing an analyzer on existing data needs a reindex.
Synonyms belong in a search analyzer (`synonym_graph` filter with `"updateable": true`,
which allows reloading search analyzers to pick up synonym file changes). Autocomplete:
`search_as_you_type`, or the `edge_ngram` tokenizer at index time only, with a plain
search analyzer, and configure its gram lengths (the defaults are almost useless).

## 3. Shard sizing
- Aim for **10–50 GB per shard** (Elastic: "typically work well for many use cases") and
  under 200 million documents per shard. With ILM, set the rollover action's
  `max_primary_shard_size` to `50gb` and `min_primary_shard_size` to `10gb`.
- Each shard has management and search overhead. Elastic's rule of thumb for master-eligible
  nodes is fewer than 3000 indices per GB of heap. If retention allows, Elastic advises
  rolling over on `max_primary_shard_size` rather than `max_age`, to avoid empty or many small indices.
- Shard size is fixed once created: fix an oversized shard by copying the index with
  corrected settings (for example `_reindex`), then point an alias at it.

## 4. Time-based data: ILM (Elasticsearch)
```json
PUT _ilm/policy/logs-30d
{ "policy": { "phases": {
  "hot":    { "actions": { "rollover": { "max_primary_shard_size": "50gb", "max_age": "1d" } } },
  "warm":   { "min_age": "7d",  "actions": { "shrink": { "number_of_shards": 1 },
                                              "forcemerge": { "max_num_segments": 1 } } },
  "delete": { "min_age": "30d", "actions": { "delete": {} } } } } }
```
Use **data streams** for append-only time-series; rollover then needs no alias setup.

## 5. OpenSearch differences (ISM)
OpenSearch replaced ILM with **Index State Management**: a policy is a state machine
(`states` with `actions` and `transitions` conditions such as a minimum age or document
count), attached to new indices by an `ism_template` object in the policy. ISM runs a job
every 5 minutes by default, so transitions are not instant. ILM JSON does not port
directly; rewrite it.

## Verify
- [ ] Every index pattern has a template with explicit mappings; `GET <index>/_mapping` shows no surprise fields.
- [ ] `_analyze` output matches expectations for real sample text.
- [ ] Primary shard sizes sit in 10–50 GB; no swarm of sub-1 GB shards.
- [ ] ILM/ISM explain shows indices progressing through phases without errors.
- [ ] Cluster health is green and field count is well under the limit.

## Checked
2026-11-09. Confirmed in Elastic docs (size your shards, mapping limit, dynamic, flattened, edge_ngram, synonym_graph, search_as_you_type, stemmer light_english) and ILM action pages: 10GB-50GB shard size and 200 million docs, rollover thresholds min/max_primary_shard_size, 3000 indices per GB heap, total_fields limit, dynamic false/strict, flattened, edge_ngram index-time only, synonym updateable, shrink/forcemerge fields. Confirmed in OpenSearch ISM docs: states/transitions, ism_template, job every 5 minutes by default. Removed: string to text+keyword and 42 to long mapping guesses, OpenSearch flat_object, synonym reload without qualification, the _cat/shards command and the _ilm/explain tip (not checked).
Method: documentation only; no commands were run.
