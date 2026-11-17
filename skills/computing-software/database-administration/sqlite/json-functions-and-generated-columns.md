---
id: computing-software.database-administration.sqlite.json-functions-and-generated-columns
name: json-functions-and-generated-columns
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-query-planner, sqlite-json, json-extract, json-each, jsonb, generated-columns, indexed-expressions, virtual-columns]
level: practitioner
status: verified
description: "Store and query JSON in SQLite with json_extract/->>, json_each, JSONB (3.45+), and make JSON fields fast with generated columns or expression indexes."
sources:
  - https://www.sqlite.org/json1.html
  - https://www.sqlite.org/gencol.html
  - https://www.sqlite.org/expridx.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON functions and generated columns

**Goal:** keep flexible JSON payloads in SQLite while filtering on fields at index speed.

## Query JSON
```sql
CREATE TABLE events (id INTEGER PRIMARY KEY, body TEXT NOT NULL CHECK (json_valid(body)));
SELECT body ->> '$.user.id' AS uid,            -- SQL value (3.38+); -> returns JSON text
       json_extract(body, '$.tags[0]')
FROM events WHERE body ->> '$.type' = 'login';
-- arrays to rows
SELECT e.id, t.value FROM events e, json_each(e.body, '$.tags') t WHERE t.value = 'mobile';
-- modify
UPDATE events SET body = json_set(body, '$.processed', json('true')) WHERE id = 7;
SELECT json_group_array(id), json_group_object(id, body ->> '$.type') FROM events;
```
3.45+: `jsonb(...)` returns a binary form (a BLOB; faster to parse, use `jsonb_*` functions, keep the column as BLOB). `json_valid(x)` is 0 for a JSONB value; add flags: `json_valid(jsonb(...), 8)` and `, 6` were both 1 in a test, `json_valid('{a:1}')` is 0 (JSON5) but `json_valid('{a:1}', 2)` is 1.

## Index a JSON field: two ways
1. Expression index (the expression in the query must match exactly):
```sql
CREATE INDEX idx_events_type ON events (body ->> '$.type');
```
2. Generated column + index (cleaner, typed, reusable in queries):
```sql
ALTER TABLE events ADD COLUMN type TEXT GENERATED ALWAYS AS (body ->> '$.type') VIRTUAL;
CREATE INDEX idx_events_type2 ON events(type);
SELECT * FROM events WHERE type = 'login';
```
`VIRTUAL` computes on read (only VIRTUAL can be added with ALTER TABLE); `STORED` stores it (must be declared in CREATE TABLE).

## Gotchas
- `->>` vs `->`: `->` returns JSON text (`'"login"'` with quotes), comparisons fail silently (`WHERE body -> '$.type' = 'login'` matched 0 rows). Use `->>` for scalar comparisons.
- `json_extract` and `->>` return SQL types: numbers compare as numbers, but JSON `true` is the integer 1.
- An expression index is used only for the same expression: with an index on `body ->> '$.type'`, the query `WHERE json_extract(body,'$.type') = 'login'` showed `SCAN events` (tested), `->>` showed `SEARCH ... USING INDEX idx_events_type (<expr>=?)`.
- `ALTER TABLE ... ADD COLUMN ... STORED` fails with `cannot add a STORED column`.
- Generated columns cannot be PRIMARY KEY or reference other tables; expressions must be deterministic.
- Old SQLite (< 3.38) lacks `->`/`->>`; the JSON functions are built in by default since 3.38.0 (json1.html).

## Verify
`EXPLAIN QUERY PLAN SELECT * FROM events WHERE type = 'login'` shows `SEARCH events USING INDEX idx_events_type2 (type=?)`.
