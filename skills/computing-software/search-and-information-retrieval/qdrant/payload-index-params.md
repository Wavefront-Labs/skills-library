---
id: computing-software.search-and-information-retrieval.qdrant.payload-index-params
name: payload-index-params
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [integer-index, lookup, range, keyword-prefix, idx-params]
level: advanced
status: docs-checked
description: "Tune Qdrant payload indexes with parameterized integer indexes (lookup, range), keyword prefix matching and the memory tier."
sources:
  - https://qdrant.tech/documentation/manage-data/indexing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Some payload indexes take parameters.

Integer index with explicit capabilities:

```json
{ "field_name": "price",
  "field_schema": { "type": "integer", "lookup": true, "range": true } }
```

`lookup` enables direct lookup with Match filters and `range` enables Range filters. Both default to true. Setting one to false can reduce memory use in large collections; the docs encourage testing whether it helps, and say to use the regular integer index if you see no improvement or are unsure which filters you use. Setting `range: false` and still using a range filter (or `lookup: false` and using Match) can cause significant performance problems.

Keyword prefix matching:

```json
{ "field_name": "path",
  "field_schema": { "type": "keyword", "prefix": true } }
```

By default a keyword index supports exact matching only. `prefix: true` also enables the Prefix Match condition (and speeds up Substring Match). It suits identifier-like values such as URLs, paths and SKUs. Matching is byte-wise (character-wise for valid UTF-8) and case-sensitive. It is unrelated to the full-text prefix tokenizer. Enabling `prefix` on an existing keyword index triggers a full rebuild of that index. With strict mode `unindexed_filtering_retrieve` or `unindexed_filtering_update` set to false, a prefix condition on a field without a prefix-enabled keyword index is rejected.

Memory tier: payload indexes are always persisted to disk and by default loaded into the pinned memory tier (kept on the heap, no disk I/O during search). Set `memory` in the schema, for example:

```json
{ "field_name": "city", "field_schema": { "type": "keyword", "memory": "cold" } }
```

Other parameters: `is_tenant` and `is_principal` (separate skills), and `nested` for per-element indexes of arrays of objects (see the nested index skill).

## Checked

2026-11-08. Confirmed against the Indexing page: integer `lookup`/`range` and defaults, keyword `prefix` behaviour, rebuild on enabling prefix, strict-mode interaction, the `memory` parameter and its default tier. Page read by section (payload index parameters); full-text and sparse sections skipped. Corrected: `memory` values other than `cold` are not listed for payload indexes in the part read, so only the example is kept. Removed: the uuid 16-byte note (kept in the payload types skill) and the unsourced "extra capabilities cost memory for every point" advice.
Method: documentation only; no commands were run.
