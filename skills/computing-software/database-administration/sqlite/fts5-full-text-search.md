---
id: computing-software.database-administration.sqlite.fts5-full-text-search
name: fts5-full-text-search
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-query-planner, fts5, full-text-search, external-content-table, bm25, trigram-tokenizer, porter-tokenizer, match-query]
level: practitioner
status: verified
description: "Add full-text search to SQLite with FTS5: external-content tables kept in sync by triggers, tokenizers, MATCH syntax, bm25 ranking, snippets and optimize."
sources:
  - https://www.sqlite.org/fts5.html
  - https://www.sqlite.org/fts5.html#external_content_tables
  - https://www.sqlite.org/fts5.html#the_bm25_function
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full-text search with FTS5

**Goal:** fast relevance-ranked search over text columns of an existing table, without duplicating the data.

## External-content table
```sql
CREATE VIRTUAL TABLE notes_fts USING fts5(
  title, body,
  content='notes', content_rowid='id',
  tokenize='porter unicode61 remove_diacritics 2'
);
-- keep in sync
CREATE TRIGGER notes_ai AFTER INSERT ON notes BEGIN
  INSERT INTO notes_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;
CREATE TRIGGER notes_ad AFTER DELETE ON notes BEGIN
  INSERT INTO notes_fts(notes_fts, rowid, title, body) VALUES ('delete', old.id, old.title, old.body);
END;
CREATE TRIGGER notes_au AFTER UPDATE ON notes BEGIN
  INSERT INTO notes_fts(notes_fts, rowid, title, body) VALUES ('delete', old.id, old.title, old.body);
  INSERT INTO notes_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;
INSERT INTO notes_fts(notes_fts) VALUES ('rebuild');   -- initial build / repair
```
The `'delete'` command must receive the OLD values exactly, or the index is corrupted (fix with `rebuild`).
Tested on 3.50.4: a `'delete'` with wrong values went unnoticed by the plain
`INSERT INTO notes_fts(notes_fts) VALUES ('integrity-check')` but `... (notes_fts, rank) VALUES ('integrity-check', 1)`
(the form that also compares an external-content index with its table) failed with `database disk image is malformed`.

## Query
```sql
SELECT n.id, n.title, snippet(notes_fts, 1, '[', ']', '…', 12) AS snip
FROM notes_fts JOIN notes n ON n.id = notes_fts.rowid
WHERE notes_fts MATCH 'title:replica AND (lag OR delay) NOT arbiter'
ORDER BY bm25(notes_fts, 5.0, 1.0)      -- lower = better; weights per column
LIMIT 20;
```
Syntax: `"exact phrase"`, `prefix*`, `NEAR(a b, 5)`, `col:term`, `^start`. `ORDER BY rank` uses the default bm25.

## Tokenizers
| Tokenizer | Use |
|---|---|
| `unicode61` (default) | Word split, case folding; `remove_diacritics 2` |
| `porter unicode61` | English stemming (run/running) |
| `trigram` (3.34+) | Substring search; `LIKE '%lo wo%'` showed `SCAN t VIRTUAL TABLE INDEX 0:L0` (index-assisted) on 3.50.4; bigger index |
| `ascii` | ASCII only |

## Maintenance
```sql
INSERT INTO notes_fts(notes_fts) VALUES ('optimize');        -- merge b-trees after bulk loads
INSERT INTO notes_fts(notes_fts, rank) VALUES ('automerge', 8);
INSERT INTO notes_fts(notes_fts, rank) VALUES ('integrity-check', 1);   -- 1 also checks against the external content table
```

## Gotchas
- User input in MATCH can be a syntax error (`"`, `-`, `:`): quote each term as a phrase or catch errors.
- `contentless` (`content=''`) tables save space but return NULL for column values and reject a plain `DELETE` (`cannot DELETE from contentless fts5 table`); add `contentless_delete=1` (3.43.0+) to allow DELETE and UPDATE.
- FTS5 must be compiled in (it was in the Python 3.14 build tested and the 3.54.1 sqlite.org shell); check `PRAGMA compile_options` for `ENABLE_FTS5`.

## Verify
`EXPLAIN QUERY PLAN` shows `SCAN notes_fts VIRTUAL TABLE INDEX 0:M2` (the `MATCH` plan; `ORDER BY bm25(...)` adds `USE TEMP B-TREE FOR ORDER BY`); after updating a note, searching for the new word finds it and the old word does not.
