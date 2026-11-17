---
id: computing-software.database-administration.postgresql.pg-trgm-fuzzy-and-like-search
name: pg-trgm-fuzzy-and-like-search
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-extensions, create-extension, pg-trgm, trigram, like-search, ilike, fuzzy-search, similarity, gin-trgm-ops]
level: practitioner
status: verified
description: "Make LIKE '%term%', ILIKE and regex searches index-backed in PostgreSQL with pg_trgm GIN/GiST indexes, and do typo-tolerant similarity search."
sources:
  - https://www.postgresql.org/docs/current/pgtrgm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_trgm for substring and fuzzy search

**Goal:** `WHERE name ILIKE '%smith%'` stops scanning the whole table, and
"Jonh Smiht" still finds "John Smith".

## Setup
```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX customers_name_trgm ON customers USING gin (name gin_trgm_ops);
```
GIN: faster lookup, slower updates. GiST (`gist_trgm_ops`): supports
`ORDER BY name <-> 'term'` (nearest by similarity). Do not assume GiST is smaller: on 100,000 random 37-character names the GIN index was 10.2 MB and the GiST index 21 MB.

## Queries that use it
```sql
SELECT * FROM customers WHERE name ILIKE '%smith%';
SELECT * FROM customers WHERE name ~* 'sm(i|y)th';
SELECT name, similarity(name, 'Jon Smith') AS sim
FROM customers WHERE name % 'Jon Smith'           -- % uses pg_trgm.similarity_threshold (0.3)
ORDER BY sim DESC LIMIT 10;
SELECT * FROM customers WHERE 'smith' <% name;    -- word_similarity: term within longer text
```
Tune: `SET pg_trgm.similarity_threshold = 0.2;` (lower finds more, slower). Typos cost a lot: `similarity('John Smith', 'Jonh Smiht')` is only 0.294, so `name % 'Jonh Smiht'` does **not** match "John Smith" at the default 0.3 (it does at 0.2); `word_similarity('Jonh Smiht', 'John Smith')` is 0.357 and `<%` has its own `pg_trgm.word_similarity_threshold` (default 0.6).

## Limits
- Search strings shorter than 3 characters produce no usable trigrams: the
  index cannot help `ILIKE '%ab%'` or `'%sm%'` (both planned as a seq scan here).
- Very common trigrams make GIN posting lists huge; performance degrades for
  terms like `%the%`.
- The index is large: the GIN trigram index above was 1.4x the table (10.2 MB vs 7.5 MB) and 2.7x the raw column bytes; measure on your data.
- For language-aware word search (stemming, ranking), use full-text search
  (tsvector + GIN) instead; trigram is for substrings, names, codes, typos.

## Verify
`EXPLAIN ANALYZE SELECT * FROM customers WHERE name ILIKE '%smith%';` shows
`Bitmap Index Scan on customers_name_trgm`. `SELECT show_trgm('smith');` shows
the trigrams being indexed (`{"  s"," sm",ith,mit,smi,"th "}`).

## Checked
PostgreSQL 17.6 with pg_trgm and 100,002 rows: `ILIKE '%smith%'`, `~* 'sm(i|y)th'` and `name % '...'` use the GIN index (`Bitmap Index Scan`), `'smith' <% name` uses it as `name %> 'smith'`, `ORDER BY name <-> '...' LIMIT 3` uses the GiST index (`Order By:`), `%ab%` and `%sm%` seq scan; defaults `pg_trgm.similarity_threshold` 0.3 and `word_similarity_threshold` 0.6; similarity values and sizes quoted above were computed here; `show_trgm('smith')` output as shown.
