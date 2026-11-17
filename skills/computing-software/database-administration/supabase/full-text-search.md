---
id: computing-software.database-administration.supabase.full-text-search
name: full-text-search
category: computing-software
field: database-administration
product: supabase
tags: [full-text-search, tsvector, tsquery, websearch, ranking]
level: practitioner
status: docs-checked
description: "Use Postgres full text search in Supabase with to_tsvector, tsquery operators, prefix matching, websearch queries and A-D weights."
sources:
  - https://supabase.com/docs/guides/database/full-text-search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: search text columns with Postgres built-ins.

Functions:
- `to_tsvector()` converts data into searchable tokens.
- `to_tsquery()` converts a query string and needs manual operators.
- `plainto_tsquery()` makes an AND query from plain text.
- `phraseto_tsquery()` makes phrase queries.
- `websearch_to_tsquery()` supports quotes, "or" and negation.
- `@@` matches a tsvector against a tsquery.

```sql
select to_tsvector('green eggs and ham');
select * from books where to_tsvector(description) @@ to_tsquery('big');
select * from books where to_tsvector(description) @@ to_tsquery('little | big');
select title from books where to_tsvector(title) @@ to_tsquery('Lit:*');
select * from books where to_tsvector(description) @@ websearch_to_tsquery('english', 'animal -rabbit');
```

Operators in `to_tsquery`:
- `&` AND, `|` OR, `!` NOT.
- `<->` terms immediately adjacent; `<2>` (the page's example `'year <2> school'`, described as "within 2 words of each other").
- `:*` prefix match.
- `+` can stand in for a space in a search term, as in `search_books_by_title_prefix('Little+Puppy')`.

Ranking: the page says ranking functions need to be computed server-side, so use RPC functions and generated columns (`ts_rank` over a stored `tsvector` column with a GIN index). Weight labels order matches: A highest (1.0), then B (0.4), C (0.2), D (0.1); `setweight(to_tsvector(...), 'A')` assigns them, and `ts_rank` also accepts a custom weight array ordered {D, C, B, A}. The page also shows searches wrapped in Postgres functions, such as `search_books_weighted('Harry')` and `search_books_fts('little & big')`. Searching several columns from the JavaScript or Dart client has no direct way; use a computed column.

## Checked

2026-11-04: Read the Full Text Search guide in full. Confirmed the functions, operators, example queries, the `+` placeholder, ranking approach and weight values. Tightened the `<2>` wording to the page's example and added the generated-column and custom-weight-array details.
Method: documentation only; no commands were run.
