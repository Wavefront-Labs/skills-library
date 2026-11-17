---
id: computing-software.database-administration.sql.tsvector-tsquery-ranking
name: tsvector-tsquery-ranking
category: computing-software
field: database-administration
product: sql
tags: [sql, tsvector-tsquery-ranking]
level: advanced
status: docs-checked
description: "Search text in PostgreSQL with tsvector, tsquery and ts_rank."
sources: ["https://www.postgresql.org/docs/current/textsearch-controls.html", "https://www.postgresql.org/docs/current/textsearch-tables.html", "https://www.postgresql.org/docs/current/textsearch-indexes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tsvector tsquery and ranking

- Basic search: `SELECT title FROM docs WHERE to_tsvector('english', body) @@ websearch_to_tsquery('english', 'quick fox');`
- Rank matches with `ts_rank(vector, query [, normalization])` (term frequency) or `ts_rank_cd` (cover density, also uses proximity and needs lexeme positions). Order by the rank descending and add `LIMIT`. Ranking must read the tsvector of every matching row, so it can be I/O bound.
- Weights: label parts of a document with `setweight(to_tsvector(coalesce(title,'')), 'A')` (A to D) and concatenate with `||`. Default rank weights are {0.1, 0.2, 0.4, 1.0} for D, C, B, A. Use `coalesce` because `to_tsvector(NULL)` returns NULL.
- Normalization is a bit mask (0 default ignores length, 1 and 2 divide by log length or length, 32 gives rank/(rank+1)); 4 is only implemented by `ts_rank_cd`.
- Query parsers: `to_tsquery` needs tsquery syntax (`&`, `|`, `!`, `<->`) and raises a syntax error on bad input; `plainto_tsquery` ANDs the words; `phraseto_tsquery` uses `<->`; `websearch_to_tsquery` accepts quoted phrases, `or` and `-` and never raises syntax errors, so it suits raw user input. The last three ignore operators, weights and prefix labels in the input.
- Indexing: a GIN index is the preferred type. Either index an expression with the two-argument form, `CREATE INDEX ON docs USING gin (to_tsvector('english', body));` (queries must use the same two-argument call to use it), or add a stored generated `tsvector` column built with `to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,''))` and index that column with GIN. The column form avoids repeating the configuration in queries and avoids recomputing `to_tsvector` for rechecks; the expression form uses less disk.
- The configuration (`english`) controls stemming and stop words.
- `ts_headline` builds excerpts from the original document, can be slow, and its output is not safe for direct HTML inclusion with untrusted input.
- Self-check: `EXPLAIN` should show the GIN index used; if not, compare the configuration argument in the query with the index definition.

## Checked

2026-11-08. Confirmed against the PostgreSQL manual sections Controlling Text Search (parsing, ranking, weights, normalization, ts_headline), Tables and Indexes, and Preferred Index Types for Text Search. Removed the specific claim that the plan shows a Bitmap Index Scan, which no fetched page states.
Method: documentation only; no commands were run.
