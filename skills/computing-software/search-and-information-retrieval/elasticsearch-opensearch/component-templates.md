---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.component-templates
name: component-templates
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, component-templates]
level: practitioner
status: docs-checked
description: "Split shared mappings and settings into component templates and compose them with composed_of in an index template."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/templates
  - https://www.elastic.co/docs/manage-data/data-store/templates/simulate-multi-component-templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Component templates

**Goal:** reuse blocks (timestamps, ECS-like fields, shard settings) across templates.
- A component template is a reusable building block defining settings, mappings and aliases; it is not applied directly and must be referenced by index templates.
- Create: `PUT _component_template/ts-mappings {"template":{"mappings":{...}}}`.
- Use: `"composed_of":["ts-mappings","shard-settings"]` in the index template. Component templates are merged in the order listed, so later ones override earlier ones; settings and mappings in the index template itself override the component templates.
- Preview the merged result with `POST /_index_template/_simulate_index/<index-name>` or `POST /_index_template/_simulate/<template>`.

## Verify
- [ ] `_simulate_index` shows fields from every component in the order expected.

## Scope
The Elasticsearch documentation was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch docs pages Templates and Simulate multi-component templates. Confirmed: all statements above. Removed: `GET _component_template/ts-*`, "updating a component template affects only later indices", "deleting a referenced component template is refused", the version-control advice, and the OpenSearch source root (none stated on the pages read).

Method: documentation only; no commands were run.
