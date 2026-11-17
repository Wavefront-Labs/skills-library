---
id: computing-software.search-and-information-retrieval.meilisearch.filter-expression-syntax
name: filter-expression-syntax
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [filter-expression, filterable-attributes, filter-operators, meilisearch]
level: practitioner
status: docs-checked
description: "Write Meilisearch filter expressions: comparison, TO, EXISTS, IS EMPTY, IS NULL, IN, STARTS WITH, NOT, AND/OR grouping, array syntax and _foreign()."
sources: ["https://www.meilisearch.com/docs/capabilities/filtering_sorting_faceting/advanced/filter_expression_syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filter expression syntax

The `filter` search parameter takes a string, an array, or a mix. A condition is `attribute OPERATOR value`. Values with whitespace need quotes: `director = 'Jordan Peele'`. Filters handle numbers and strings; do not rely on NaN or infinities (pass them as strings, except in `_geo`). Keep field types homogeneous because the engine may coerce values.

## Operators

- `=` and `!=`: case-insensitive on strings; on arrays match if any element matches. `=` returns nothing for null or empty arrays.
- `>`, `>=`, `<`, `<=`: numbers and strings (lexicographic), e.g. `release_date > 2004-01-01`.
- `TO`: range, `rating.users 80 TO 89`.
- `EXISTS`: field present (null or empty still counts); negate with `NOT EXISTS`. `_vectors EXISTS` and `_vectors.<embedder> EXISTS` filter on embeddings and work only with EXISTS.
- `IS EMPTY` matches `""`, `[]`, `{}`; `IS NULL` matches null; both negate with NOT.
- `IN`: `genres IN [horror, comedy]` equals the OR form.
- `STARTS WITH`; `CONTAINS` is experimental and needs the experimental features endpoint enabled.
- `NOT` binds tighter than AND, and AND tighter than OR.
- `_foreign(fieldName, condition)` filters via a joined index; it errors if the related filter matches over 1000 documents.

## Grouping

Strings read left to right, so use parentheses: `(genres = horror OR genres = comedy) AND release_date > 795484800`. Quote fields or values named like operators (`title = "NOT"`).

Arrays: outer elements are ANDed, inner arrays ORed, maximum depth two. `[["genres = horror", "genres = comedy"], "director = 'Jordan Peele'"]`.

## Checked

2026-11-03. Confirmed claim by claim against the Filter expression syntax page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: the unsupported word 'inclusive' for TO.

Method: documentation only; no commands were run.
