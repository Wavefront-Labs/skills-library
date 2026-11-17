---
id: computing-software.database-administration.sql.seq-scan-vs-index-scan
name: seq-scan-vs-index-scan
category: computing-software
field: database-administration
product: sql
tags: [sql, seq-scan-vs-index-scan]
level: practitioner
status: docs-checked
description: "Understand why the planner picks scans and what to change."
sources: ["https://www.postgresql.org/docs/current/using-explain.html", "https://www.postgresql.org/docs/current/runtime-config-query.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seq scan versus index scan decisions

- A seq scan is correct when the query must read most of the table, when no index exists, or when the table fits in about one disk page (you will nearly always get a seq scan there). Its estimated cost is pages read times `seq_page_cost` plus rows scanned times `cpu_tuple_cost`.
- Index Scan fetches rows in index order and is typical for queries returning very few rows (the manual's example: `unique1 = 42` on a 10000-row table). Bitmap Index Scan plus Bitmap Heap Scan finds matching row locations first, sorts them into physical order, then fetches, which beats a seq scan when only some pages are needed (about 1% of rows in the manual's example; about 70% gave a seq scan). Index Only Scan reports `Heap Fetches` in EXPLAIN ANALYZE.
- Diagnosis: compare estimated and actual row counts in `EXPLAIN ANALYZE`; ANALYZE statistics come from a random sample, so estimates can shift between runs. `SET enable_seqscan = off` only discourages seq scans (they cannot be suppressed entirely) and shows `Disabled: true` in the plan; use it to test alternatives, not in production.
- Other checks worth making, though outside these pages: whether the predicate matches the index expression and column type, and how stale statistics are.
- `random_page_cost` defaults to 4.0 against `seq_page_cost` 1.0; lowering it makes index scans look cheaper, raising it makes them dearer. The manual says to lower it when data is mostly cached and raise it for storage with costly random reads such as magnetic disks, and cautions against tuning from a few experiments.
- Self-check: re-run EXPLAIN after the change and confirm the node type.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages using-explain.html and runtime-config-query.html; the draft's "about 1.1 on SSD" figure is not on those pages and was replaced with the manual's own guidance.
