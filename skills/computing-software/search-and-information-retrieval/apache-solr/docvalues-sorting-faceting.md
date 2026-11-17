---
id: computing-software.search-and-information-retrieval.apache-solr.docvalues-sorting-faceting
name: docvalues-sorting-faceting
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [docvalues, use-docvalues-as-stored, sorted-set, uninverted, export-fields]
level: practitioner
status: docs-checked
description: "Understand Solr DocValues: column-oriented per-field data used for sorting, faceting, grouping and export; defaults, ordering caveats, docValuesFormat and the reindex requirement."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/docvalues.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docvalues-sorting-faceting

DocValues are a document-to-value mapping built at index time, replacing in-memory un-inversion for sorting, faceting, grouping and function queries. Solr uses them automatically for those features when `docValues="true"`.

Defaults: enabled for most supporting types (numeric except DenseVectorField, boolean, string, date, UUID, enum) when `schemaVersion` is 1.7 or higher. With 1.6 or lower, enable it explicitly. Turn it off with `docValues="false"`.

Retrieval behaviour:
- Non-stored docValues fields are returned for `fl=*` when `useDocValuesAsStored` is true (the implicit default for schema 1.6+). If false, request them by name.
- Values come back in sorted order, not insertion order, and SORTED_SET types (strings, UUID, booleans) drop duplicates: inserting 4, 5, 2, 4, 1 returns 1, 2, 4, 5. Keep the field stored if insertion order matters.

`docValuesFormat="Direct"` keeps everything in memory but is not back-compatible across upgrades. Changing docValues on existing data requires a full reindex.

## Checked

2026-11-04. Confirmed against the DocValues page: defaults by `schemaVersion`, `useDocValuesAsStored`, ordering and duplicate caveats, `docValuesFormat="Direct"`, reindex requirement. Nothing removed.

Method: documentation only; no commands were run.
