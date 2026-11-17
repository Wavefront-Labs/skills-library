---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.composable-index-templates
name: composable-index-templates
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, composable-index-templates, es-index-templates]
level: practitioner
status: docs-checked
description: "Create composable index templates with index_patterns, priority and a template body so new indices get consistent settings and mappings."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/templates
  - https://www.elastic.co/docs/manage-data/data-store/templates/simulate-multi-component-templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composable index templates

**Goal:** every new index matching a pattern gets the same settings, mappings and aliases.
```
PUT _index_template/logs-tpl
{"index_patterns":["logs-*"],"priority":501,"template":{"settings":{"number_of_shards":1},"mappings":{"properties":{"@timestamp":{"type":"date"}}}}}
```
- A template is applied when an index (or data stream backing index) is created; mappings, settings and aliases in the template are inherited by each created index.
- If a new index matches more than one template, the one with the highest `priority` is used.
- Built-in Elasticsearch templates have priority `100` and Fleet/Agent integrations use up to `200`, with overlapping patterns such as `logs-*`. Avoid collisions: use a non-overlapping pattern, or for an overlapping pattern use a priority above `500` (the page's example uses `501` for `logs-*`).
- Settings in a create-index request take precedence over the template and its component templates; settings in the index template itself take precedence over its component templates.
- Preview the result: `POST /_index_template/_simulate_index/<index-name>` shows the settings that would apply to that index name; `POST /_index_template/_simulate/<template>` simulates an existing template.

## Verify
- [ ] Simulate shows the merged settings, then create an index and compare `GET <index>/_settings`.

## Scope
The Elasticsearch documentation was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch docs pages Templates and Simulate multi-component templates. Confirmed: all statements above. Removed: "equal priority with overlapping patterns is rejected" and the `illegal_argument_exception` failure mode (not stated), "existing indices are not changed" (only the creation-time application is documented), and the OpenSearch source root. Changed: the example priority from `200` to `501` because the page warns about collisions with built-in `logs-*` templates.

Method: documentation only; no commands were run.
