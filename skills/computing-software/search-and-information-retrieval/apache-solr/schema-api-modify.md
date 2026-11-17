---
id: computing-software.search-and-information-retrieval.apache-solr.schema-api-modify
name: schema-api-modify
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [schema-api, solr, schema, managed-schema-xml, replace-field, delete-field]
level: practitioner
status: docs-checked
description: "Change a Solr collection schema at runtime with the Schema API: add-field, replace-field, add-dynamic-field, add-field-type, copy field commands, and why to reindex."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/schema-api.html
  - https://solr.apache.org/guide/solr/latest/indexing-guide/reindexing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# schema-api-modify

Send a POST to the collection `/schema` endpoint with JSON commands. Supported commands: `add-field`, `delete-field`, `replace-field`, `add-dynamic-field`, `delete-dynamic-field`, `replace-dynamic-field`, `add-field-type`, `delete-field-type`, `replace-field-type`, plus copy field add and delete commands.

The Schema API uses `ManagedIndexSchemaFactory`, the default schema factory. A core reload happens automatically after each modification so the change applies to documents indexed afterward.

Rules that matter:
- The change never touches documents already indexed. If existing data uses a field or type you changed, reindex, or you may lose access to documents or fail to interpret them (for example after replacing a field type).
- Hand editing `managed-schema.xml` is discouraged. Edits can be lost if the Schema API is used later, unless you reload the collection or restart Solr between the manual edit and the API call.
- Read access works for all schema elements and can return JSON or XML.

## Checked

2026-11-04. Confirmed against the Schema API and Reindexing pages: supported commands, `ManagedIndexSchemaFactory`, automatic reload, existing documents untouched, hand-editing caveat, read access formats. Removed an unsourced version claim and a generic closing tip.

Method: documentation only; no commands were run.
