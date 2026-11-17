---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.custom-analyzer-definition
name: custom-analyzer-definition
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, custom-analyzer-definition, es-analysis]
level: practitioner
status: docs-checked
description: "Build a custom analyzer from char_filter, tokenizer and token filters in index settings and assign it to fields."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer-anatomy.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-update-settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Define a custom analyzer

**Goal:** control exactly how text is split and normalised at index time.
```
PUT my-index
{"settings":{"analysis":{"analyzer":{"my_an":{"type":"custom","tokenizer":"standard","filter":["lowercase","asciifolding"]}}}},
 "mappings":{"properties":{"body":{"type":"text","analyzer":"my_an"}}}}
```
- An analyzer is zero or more character filters (applied in order), exactly one tokenizer, and zero or more token filters (applied in order). For `type: custom` (or omitted) `tokenizer` is required; `char_filter` and `filter` are optional arrays; `position_increment_gap` defaults to 100.
- New analyzers can only be defined on a closed index (`POST my-index/_close`, `PUT my-index/_settings`, `POST my-index/_open`). To change the analyzer on a data stream's existing backing indices, create a new data stream and reindex; for future backing indices update the index template and roll over.
- Failure mode: changing the analyzer on a populated field makes old and new tokens disagree; reindex.

## Verify
- [ ] `POST my-index/_analyze {"analyzer":"my_an","text":"Café Society"}` returns `cafe`, `society`.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited pages are Elasticsearch; OpenSearch was not checked here.

## Checked
2026-11-08. Read the Elasticsearch Create a custom analyzer, Anatomy of an analyzer and Update index settings pages: component order and counts, parameters, `position_increment_gap` default, closed-index requirement and the data stream guidance. Removed the `illegal_argument_exception` error name (not on the pages). The `_analyze` expected output in Verify is derived reasoning, not quoted from a page.
Method: documentation only; no commands were run.
