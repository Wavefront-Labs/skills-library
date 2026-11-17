---
id: computing-software.database-administration.sql.keyset-vs-offset-tradeoffs
name: keyset-vs-offset-tradeoffs
category: computing-software
field: database-administration
product: sql
tags: [sql, keyset-vs-offset-tradeoffs]
level: practitioner
status: docs-checked
description: "Switch deep pagination from OFFSET to keyset with a composite tiebreaker."
sources: ["https://www.postgresql.org/docs/current/queries-limit.html", "https://www.postgresql.org/docs/current/functions-comparisons.html", "https://www.postgresql.org/docs/current/indexes-ordering.html", "https://www.sqlite.org/rowvalue.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyset versus offset pagination trade-offs

- OFFSET: rows skipped by `OFFSET` still have to be computed inside the server, so a large `OFFSET` can be slow. Also give `ORDER BY` a unique order or pages overlap or skip.
- Keyset, page 1: `ORDER BY ts DESC, id DESC LIMIT 50`. Next page: `WHERE (ts, id) < ($last_ts, $last_id) ORDER BY ts DESC, id DESC LIMIT 50`. `id` is the tiebreaker that makes the order unique.
- The row comparison is lexicographic: columns are compared left to right and the first unequal pair decides. If a NULL is reached first the result is NULL, so keep the key columns `NOT NULL`.
- SQLite supports row values from 3.15.0; earlier versions give a syntax error. Its docs describe the keyset form as much more efficient than OFFSET given an appropriate index.
- PostgreSQL: a plain `(ts, id)` B-tree index can be scanned backward to satisfy `ORDER BY ts DESC, id DESC`. A mixed order such as `ts DESC, id ASC` needs an index declared with that mix.
- Cannot jump to page N; pass an opaque cursor holding the last key.
- Offset is acceptable for small, static lists.
- Self-check: insert rows between page fetches and confirm no duplicates or skips.

## Checked

2026-11-08. Confirmed: PostgreSQL LIMIT/OFFSET page (skipped rows still computed, unique ORDER BY needed); PostgreSQL row constructor comparison (left-to-right, NULL gives unknown); PostgreSQL index ordering page (backward scan, mixed-direction indexes); SQLite row values page (3.15.0, keyset example, efficiency remark). Removed the claim that the index must be declared `(ts DESC, id DESC)`, which the PostgreSQL page contradicts.
Method: documentation only; no commands were run.
