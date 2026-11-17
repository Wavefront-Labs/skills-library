---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.explicit-mapping-creation
name: explicit-mapping-creation
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, explicit-mapping-creation, es-mappings]
level: practitioner
status: docs-checked
description: "Create an Elasticsearch or OpenSearch index with an explicit mapping instead of relying on dynamic guesses, and evolve it safely."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/mapping/explicit-mapping
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/number
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create an index with an explicit mapping

**Goal:** fix field types before data arrives, because you generally cannot change an existing field's type.
```
PUT my-index
{"mappings":{"properties":{"title":{"type":"text"},"sku":{"type":"keyword"},"price":{"type":"scaled_float","scaling_factor":100},"created":{"type":"date"}}}}
```
- `scaled_float` stores a long scaled by a fixed double; `scaling_factor` is required, a higher factor is more accurate but uses more storage.
- Add a field later: `PUT my-index/_mapping` with new `properties`.
- Change an existing field type: generally not possible, because it could invalidate indexed data (supported mapping parameters are the exception); create a new index with the right mapping and reindex (see the reindex skills).
- Rename: do not rename a field (existing data is indexed under the old name); add an `alias` field instead.
- Read back: `GET my-index/_mapping` for the full mapping, `GET my-index/_mapping/field/title` for specific fields (useful on large indices).
- Keep the mapping in version control next to an index template.

## Verify
- [ ] `GET my-index/_mapping` matches the file in version control.
- [ ] A test document with a wrong-typed value is rejected as expected.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch explicit mapping and numeric field type pages in full; OpenSearch was not checked.
