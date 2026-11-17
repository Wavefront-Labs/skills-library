---
id: computing-software.search-and-information-retrieval.apache-solr.dynamic-fields-wildcards
name: dynamic-fields-wildcards
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [dynamic-fields, wildcard-field, dynamicfield, schema]
level: intro
status: docs-checked
description: "Use Solr dynamicField rules such as *_i to index fields you did not declare, taking type and analysis from the matching wildcard rule."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/dynamic-fields.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dynamic-fields-wildcards

A dynamic field is a field definition whose name contains a wildcard. When a document carries a field that matches no explicitly defined field, Solr tries the dynamic field patterns and the field takes that rule's type and options.

Example from the guide: with `<dynamicField name="*_i" type="int" indexed="true" stored="true"/>` in the schema, indexing a `cost_i` value works even though no `cost_i` field is defined; it gets the type and analysis of `*_i`.

Like regular fields, dynamic fields have a name, a field type and options. The guide recommends including basic dynamic field mappings in your schema, since they make the schema less brittle when a field was forgotten.

Add or remove rules with `add-dynamic-field` and `delete-dynamic-field` in the Schema API. Reindex after changing a rule that existing data used.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Dynamic Fields and Schema API pages: the `*_i` and `cost_i` example, the recommendation about brittle schemas, `add-dynamic-field`, `delete-dynamic-field`, and reindexing after schema changes. Removed the claim that the first matching pattern wins, which the pages do not state.

Method: documentation only; no commands were run.
