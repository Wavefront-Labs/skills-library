---
id: computing-software.search-and-information-retrieval.apache-solr.field-properties-indexed-stored
name: field-properties-indexed-stored
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [field-properties, indexed-stored, multivalued, fieldtype, omitnorms, schema]
level: intro
status: docs-checked
description: "Choose Solr field and field type properties: indexed, stored, docValues, multiValued, required, omitNorms, omitTermFreqAndPositions, uninvertible, useDocValuesAsStored and large."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/field-type-definitions-and-properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# field-properties-indexed-stored

A field type needs a `name` and a `class` (`solr` is shorthand for the schema package, so `solr.TextField` works). Analysis chains go on `solr.TextField` types. Properties set on the type are inherited by fields of that type.

Key properties:
- `indexed`: value usable in queries to retrieve matching documents.
- `stored`: value can be retrieved by queries.
- `docValues`: column-oriented structure, true for most fields.
- `multiValued`: a document may hold several values. Default false.
- `uninvertible`: lets an indexed field without docValues be un-inverted at query time into a large in-memory structure. Default false.
- `omitNorms`: disables length normalization and saves memory. Defaults to true for primitive (non-analyzed) types.
- `omitTermFreqAndPositions`: drops frequency, positions and payloads; saves space.
- `required`: reject documents lacking the field. Default false.
- `useDocValuesAsStored`: return a docValues field for `fl=*` even when stored is false. Default true.
- `large`: always lazily loaded; needs `stored=true` and `multiValued=false`.

Changing a property that affects indexing requires reindexing.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Field Type Definitions and Properties page: `solr` class shorthand, inherited type properties, and the property table entries for `docValues`, `multiValued`, `uninvertible`, `omitNorms`, `omitTermFreqAndPositions`, `required`, `useDocValuesAsStored` and `large` with their defaults; and the Reindexing page for the reindex rule. Nothing removed.

Method: documentation only; no commands were run.
