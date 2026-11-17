---
id: computing-software.database-administration.sql.fts5-query-syntax-bm25
name: fts5-query-syntax-bm25
category: computing-software
field: database-administration
product: sql
tags: [sql, fts5-query-syntax-bm25]
level: advanced
status: docs-checked
description: "Query SQLite FTS5 with MATCH operators, bm25 ranking and highlight()."
sources: ["https://www.sqlite.org/fts5.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FTS5 query syntax and bm25

- `CREATE VIRTUAL TABLE docs USING fts5(title, body);` then `SELECT * FROM docs WHERE docs MATCH 'quick + fox' ORDER BY bm25(docs);`
- Syntax: phrase `"a b"` (or `a + b`), prefix `qui*`, `AND` / `OR` / `NOT` (must be upper case; `NOT` binds tighter than `AND`, which binds tighter than `OR`; use parentheses), column filter `title : fox` (or `{title body} : fox`; a `-` before the filter excludes columns).
- Proximity is the function form `NEAR(quick fox, 5)`: the keyword `NEAR` is case sensitive and followed by an open parenthesis, two or more phrases, and an optional `, N` that defaults to 10. The infix form `quick NEAR fox` is not in the FTS5 grammar.
- `bm25(docs)` returns numerically smaller values for better matches, so `ORDER BY bm25(docs)` lists best first; extra real arguments weight columns (`bm25(docs, 10.0, 5.0)`). The hidden `rank` column defaults to the same value and `ORDER BY rank` is faster than `bm25()`.
- `highlight(docs, 1, '<b>', '</b>')` takes exactly three arguments after the table name: a column index counted from zero (1 = `body` here), the text before and the text after each match. `snippet()` takes five parameters after the table name and returns a short fragment of a column instead.
- Gotcha: a string containing characters other than non-ASCII characters, letters, digits and underscore must be double-quoted (embedded `"` doubled), otherwise MATCH raises a syntax error; quote or escape user input.
- Self-check: a user query containing a quote does not crash.

## Checked

Date: 2026-11-07. Read SQLite FTS5 sections 3.1 to 3.7 (query syntax, strings, phrases, prefix, NEAR, column filters, boolean operators), 5.1 to 5.1.3 (auxiliary functions bm25, highlight, snippet start) and the rank column text of the one cited page (fts5.html); the rest of the page (tokenizers, options, extension API) was searched, not read. Confirmed all items above. Corrected: `'quick NEAR fox'` is not valid FTS5 syntax (NEAR is `NEAR(phrase phrase, N)`), replaced by a phrase query and the NEAR function form; the column filter now matches the page's `colname : ...` spelling; "lower bm25 is better" now cites the page ("numerically smaller"); added rank, AND/OR/NOT case rule and highlight argument meaning from the page.
Method: documentation only; no commands were run.
