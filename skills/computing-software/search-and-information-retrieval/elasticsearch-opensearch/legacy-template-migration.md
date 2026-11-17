---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.legacy-template-migration
name: legacy-template-migration
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, legacy-template-migration]
level: advanced
status: docs-checked
description: "Move legacy _template definitions to _index_template and resolve precedence between the two kinds."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/templates
  - https://www.elastic.co/docs/manage-data/data-store/templates/simulate-multi-component-templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate legacy templates to composable

**Goal:** stop relying on legacy templates without changing what new indices look like.
- Composable index templates take precedence over legacy templates (deprecated in Elasticsearch 7.8). If no composable template matches an index, a legacy template might still match and be applied.
- So a leftover legacy template keeps applying to indices that no composable template matches; remove it only after a composable template covers the same index names.
- Before deleting a legacy template, run `POST /_index_template/_simulate_index/<index-name>` and compare the settings with an index created from the legacy template. The simulate output covers composable templates only.
- Legacy template API details (`GET _template`, the `order` field and the conversion to a `template` object with `priority`) are not covered by the pages read; see the legacy templates reference for your version.

## Verify
- [ ] After deletion, a newly created test index has the same `_settings` and `_mapping` as before.

## Scope
The Elasticsearch documentation was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch docs pages Templates and Simulate multi-component templates. Confirmed: precedence, the legacy fallback and deprecation version, simulate API. Removed: the `GET _template` / `GET _index_template` listing commands and the field conversion recipe (not stated on the pages read), and the OpenSearch source root.

Method: documentation only; no commands were run.
