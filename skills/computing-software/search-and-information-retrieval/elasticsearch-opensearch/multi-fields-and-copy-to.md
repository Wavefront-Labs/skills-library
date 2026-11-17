---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.multi-fields-and-copy-to
name: multi-fields-and-copy-to
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, multi-fields-and-copy-to]
level: practitioner
status: docs-checked
description: "Index one value several ways with fields (text plus keyword sub-field) and combine fields into one searchable group field with copy_to; know the limits."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/multi-fields
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/copy-to
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-fields and copy_to

**Goal:** search and sort/aggregate the same value without duplicating source data.
```
"city":{"type":"text","fields":{"raw":{"type":"keyword"}}}
```
- Query `city` for full text; use `city.raw` for sorting and `terms` aggregations (Elasticsearch docs example).
- A multi-field mapping is completely separate from the parent's: it inherits no mapping options, and multi-fields do not change `_source`.
- Multi-fields are also used to analyze the same text differently, for example `text` (standard analyzer) plus `text.english` (english analyzer, stems `foxes` to `fox`), queried together with `multi_match` of `"type":"most_fields"`.
- You can add multi-fields to an existing field with the update mapping API. Documents already in the index get no value for the new multi-field; populate it with the update by query API.
- `copy_to` copies the field value (not the analyzed terms) into a group field: `"first_name":{"type":"text","copy_to":"full_name"}`. Query `full_name` with `match` and `"operator":"and"` to match both names. `_source` is not modified.
- One value can go to several fields with `"copy_to":["field_1","field_2"]`. Copying is not recursive: `field_1` copied to `field_2` which is copied to `field_3` does not reach `field_3`; list both targets on the source field.
- `copy_to` is not supported for field types whose values are objects, for example `date_range`.
- With dynamic mapping: a missing target is created when `dynamic` is `true`, not created and not copied when `false`, and an error when `strict`. A target inside an object must use its full path (`description.notes_raw`), otherwise `strict_dynamic_mapping_exception`.
- Searching fewer fields through `copy_to` can improve search speed (Elasticsearch docs tip).

## Verify
- [ ] A `match` on `city` for `york` finds both stored values; sorting on `city.raw` works.
- [ ] A `match` on `full_name` with operator `and` for `John Smith` finds the document, while `_source` still shows only the original fields.

## Checked
2026-11-08. Confirmed against the Elasticsearch multi-fields (`fields`) and `copy_to` mapping parameter pages: example mappings, independence of multi-field mappings, `_source` unchanged, add-to-existing plus update by query, the multiple-analyzers example, copy_to value-not-terms, list targets, non-recursion, object-type exclusion, dynamic behaviours.
Removed: the claim that sorting on `text` errors because fielddata is disabled (not on the pages read), the OpenSearch root source, and unconfirmed-cluster boilerplate.
Method: documentation only; no commands were run.
