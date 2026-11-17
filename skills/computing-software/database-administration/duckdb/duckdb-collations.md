---
id: computing-software.database-administration.duckdb.duckdb-collations
name: duckdb-collations
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, collation, nocase, noaccent, icu, sorting, default-collation]
level: practitioner
status: docs-checked
description: "Compare and sort DuckDB text with COLLATE: built-in NOCASE/NOACCENT/NFC, chaining, default_collation, per-column collations and ICU language collations."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/expressions/collations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: language-aware or case/accent-insensitive string comparison and ordering.

Default is `BINARY` (aliases `C`, `POSIX`): compares binary UTF-8 content. It is the fastest and recommended unless you need otherwise. Collation support has known limitations.

Built-in collations in the stand-alone install: `NOCASE`, `NOACCENT`, `NFC` (NFC-normalised comparison).

```sql
SELECT 'hello' COLLATE NOCASE = 'hElLO';          -- true  (plain = is false)
SELECT 'hello' COLLATE NOACCENT = 'hëllo';        -- true
SELECT 'hello' COLLATE NOCASE.NOACCENT = 'hElLÖ'; -- true; each alone gives false
```
Chain with the dot operator. NOCASE combines with most others; most other collations cannot be combined.

Defaults:
```sql
SET default_collation = NOCASE;                   -- global
CREATE TABLE names (name VARCHAR COLLATE NOACCENT);  -- per column
```
Gotcha: different collations cannot be mixed. `WHERE name = 'hannes' COLLATE NOCASE` on a NOACCENT column, or joining a NOACCENT column to a NOCASE column, fails with `Cannot combine types with different collation!`. Override both sides: `names.name COLLATE NOACCENT.NOCASE = other_names.name COLLATE NOACCENT.NOCASE`.

ICU collations: `LOAD icu;` (see the ICU extension) adds language and region collations such as `de`, `fr_ca`, `lt`, `tr`, `zh_cn`, `icu_noaccent`. List them with `PRAGMA collations;` or `SELECT list(collname) FROM pragma_collations();`. They combine with NOCASE.

```sql
CREATE TABLE strings (s VARCHAR COLLATE DE);
INSERT INTO strings VALUES ('Gabel'), ('Göbel'), ('Goethe'), ('Goldmann'), ('Göthe'), ('Götz');
SELECT * FROM strings ORDER BY s;                 -- Gabel, Göbel, Goethe, Goldmann, Göthe, Götz
```

## Checked

2026-11-07. Read the Collations page in full and confirmed the BINARY default and its aliases `C` and `POSIX`, the three stand-alone collations, chaining with the dot operator, `default_collation`, per-column collations, the `Cannot combine types with different collation!` error and the manual override, ICU loading, `PRAGMA collations` and `pragma_collations()`, and the German ordering example. Removed an unsupported per-query `ORDER BY ... COLLATE DE` comment (the page only shows per-column use) and the Verify step.

Method: documentation only; no commands were run.
