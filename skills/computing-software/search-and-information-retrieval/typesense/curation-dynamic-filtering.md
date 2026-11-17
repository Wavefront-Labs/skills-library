---
id: computing-software.search-and-information-retrieval.typesense.curation-dynamic-filtering
name: curation-dynamic-filtering
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [dynamic-filter, remove-matched-tokens, query-placeholder, typesense]
level: advanced
status: docs-checked
description: "Rewrite queries in Typesense curation with a placeholder rule such as {brand} phone, apply filter_by brand:={brand}, and drop matched tokens with remove_matched_tokens."
sources: ["https://typesense.org/docs/30.2/api/curation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic filtering in curation

Put a placeholder in the rule query and reuse it in `filter_by`:

```json
{"id": "brand-filter",
 "rule": {"query": "{brand} phone", "match": "contains"},
 "filter_by": "brand:={brand}",
 "remove_matched_tokens": true}
```

Any query containing a brand value is then filtered on that brand automatically. The brand is also removed from the query tokens, so the text search runs on what remains: `sony ericsson phone` becomes the query `phone` with a `sony ericsson` brand filter.

## remove_matched_tokens

Default `true`. Set `false` to keep the matched tokens in the search text.

## Requirement

Fields used for dynamic filtering should have `facet: true` in the schema.

## Related actions

A rule can also carry `replace_query` (swap the whole query for a fixed string), `metadata` (a custom JSON object returned in the search response when the rule fires, e.g. a promotion banner), and `sort_by` for dynamic sorting.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Curation page (https://typesense.org/docs/30.2/api/curation.html) and its source markdown in typesense-website (placeholder rules, sort_by and filter_by examples), plus the API Keys page for curation_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
