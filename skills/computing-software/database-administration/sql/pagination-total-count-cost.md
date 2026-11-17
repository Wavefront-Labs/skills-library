---
id: computing-software.database-administration.sql.pagination-total-count-cost
name: pagination-total-count-cost
category: computing-software
field: database-administration
product: sql
tags: [sql, pagination-total-count-cost]
level: practitioner
status: docs-checked
description: "Avoid expensive exact counts when paginating."
sources: ["https://www.postgresql.org/docs/current/queries-limit.html", "https://www.postgresql.org/docs/current/catalog-pg-class.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Counting totals for pagination

- Options to avoid an exact `count(*)` over a large filtered set: cap the count with `SELECT count(*) FROM (SELECT 1 FROM t WHERE ... LIMIT 1001) x` and display "1000+", or show a rough size from the planner estimate `pg_class.reltuples` (PostgreSQL), which is only an estimate, is refreshed by VACUUM, ANALYZE and a few DDL commands such as CREATE INDEX, and is -1 if the table has never been vacuumed or analyzed. It covers the whole table, not a filtered set.
- Fetch `limit + 1` rows to learn whether a next page exists without counting.
- Always use an `ORDER BY` that gives a unique order with `LIMIT`/`OFFSET`, or pages can overlap or skip rows. Rows skipped by `OFFSET` are still computed, so deep pages get slower.
- Self-check: EXPLAIN the count and compare timing at production scale.

## Checked

2026-11-08. Confirmed against the PostgreSQL LIMIT and OFFSET page and the pg_class catalog page (reltuples). Removed the MVCC explanation for why exact counts are costly and the advice to cache totals, which no fetched page states.
Method: documentation only; no commands were run.
