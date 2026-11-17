---
id: computing-software.systems-network-administration.paperless-ngx.api-custom-field-query
name: api-custom-field-query
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, custom-field-query, api-search, autocomplete, more-like-id, search-hit]
level: advanced
status: docs-checked
description: "Search the documents API with text, title_search, query and more_like_id, and filter by custom fields with custom_field_query."
sources:
  - "https://docs.paperless-ngx.com/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API search and custom field queries

## Search parameters on /api/documents/
- `text`: title and content, substring style.
- `title_search`: title only.
- `query`: full-text query syntax.
- `more_like_id=1234`: documents similar to ID 1234.

Pagination is unchanged. Each result gains `__search_hit__` with `score`, `highlights` (matches wrapped in `<span>`) and `rank` (0 for the first).

## Autocomplete
`/api/search/autocomplete/?term=inv&limit=10` returns words ordered by how many of your visible documents contain them. Limit defaults to 10.

## custom_field_query
```
?custom_field_query=["due", "range", ["2024-08-01", "2024-09-01"]]
?custom_field_query=["customer", "exact", "bob"]
?custom_field_query=["favorite animal", "in", ["cat", "dog"]]
?custom_field_query=["foo", "exists", false]
?custom_field_query=["references", "contains", [3, 7]]
?custom_field_query=["OR", [["address", "isnull", true], ["address", "exact", ""]]]
```
Operators:
- All types: `exact`, `in`, `isnull`, `exists`.
- Strings, URLs, monetary: `icontains`, `istartswith`, `iendswith`.
- Numbers and dates: `gt`, `gte`, `lt`, `lte`, `range`.
- Document links: `contains`, meaning superset.

Dates accept dateparser expressions like `today` or `in 30 days`, resolved each run using `PAPERLESS_TIME_ZONE` and `PAPERLESS_DATE_PARSER_LANGUAGES`.

## Checked
2026-11-04. Compared line by line with the Searching for documents section of the API page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: text, title_search, query and more_like_id parameters, the `__search_hit__` fields, autocomplete behaviour and default limit, all custom_field_query recipes, the operator groups by field type, dateparser expressions and the two settings used to resolve them. Nothing removed.

Method: documentation only; no commands were run.
