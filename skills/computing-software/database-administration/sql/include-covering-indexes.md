---
id: computing-software.database-administration.sql.include-covering-indexes
name: include-covering-indexes
category: computing-software
field: database-administration
product: sql
tags: [sql, include-covering-indexes]
level: advanced
status: docs-checked
description: "Enable index-only scans with INCLUDE payload columns."
sources: ["https://www.postgresql.org/docs/current/sql-createindex.html", "https://www.postgresql.org/docs/current/indexes-index-only-scans.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Covering indexes and INCLUDE columns

- PostgreSQL: `CREATE INDEX ON t (cid) INCLUDE (total, status);` the INCLUDE columns are stored in the index as non-key columns so index-only scans can return them.
- An index-only scan checks the visibility map for each candidate index entry.
- Self-check: EXPLAIN (ANALYZE) shows an index-only scan for the query.

## Checked

2026-11-02. Confirmed: the INCLUDE clause makes non-key columns (CREATE INDEX page) and its use for index-only scans, with the visibility map check (index-only scans page). Removed: PostgreSQL 11 attribution, SQL Server and SQLite claims, the Heap Fetches figure.
Method: documentation only; no commands were run.
