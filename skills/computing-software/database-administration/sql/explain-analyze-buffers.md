---
id: computing-software.database-administration.sql.explain-analyze-buffers
name: explain-analyze-buffers
category: computing-software
field: database-administration
product: sql
tags: [sql, explain-analyze-buffers]
level: practitioner
status: docs-checked
description: "Read actual versus estimated rows and buffer use in PostgreSQL plans."
sources: ["https://www.postgresql.org/docs/current/sql-explain.html", "https://www.postgresql.org/docs/current/using-explain.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EXPLAIN ANALYZE and BUFFERS

- `EXPLAIN (ANALYZE, BUFFERS) SELECT ...;` ANALYZE actually executes the statement. EXPLAIN discards a SELECT's output, but other side effects happen, so for INSERT, UPDATE, DELETE, MERGE, CREATE TABLE AS or EXECUTE use `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`. `ANALYZE` defaults to FALSE; the current docs say buffer information is included automatically when ANALYZE is used.
- Compare the `rows=` estimate against the actual rows. The page says to look for estimates reasonably close to reality; when a table has changed substantially, the planner statistics may need a manual `ANALYZE` instead of waiting for autovacuum.
- Plan indentation reflects the plan structure: child nodes feed their parent. `actual time` and `rows` are per-execution averages; `loops` is the number of executions, so multiply by `loops` for the node total.
- `Buffers: shared hit=N read=M`: a hit means a read was avoided because the block was already in cache; `read` counts blocks read in. The count for an upper node includes its child nodes. Shared blocks hold regular tables and indexes, local blocks temporary tables, temp blocks sort/hash working data.
- Self-check: after `ANALYZE t`, re-run and compare estimates with actuals (ANALYZE samples randomly, so estimates can change from run to run).

## Checked

Date: 2026-11-07. Read the BUFFERS, ANALYZE and notes passages of the PostgreSQL EXPLAIN reference (sql-explain; synopsis, parameters and the statistics note, rest of the page located by search) and section 14.1.2 EXPLAIN ANALYZE of Using EXPLAIN (using-explain, read; the earlier plan examples were searched, not read in full). Confirmed: ANALYZE executes the statement, the BEGIN/ROLLBACK recipe, loops averaging and multiplication, hit/read/shared/local/temp definitions, upper-node block counts including children. Removed: the "10x+" gap threshold, the "or correlation" cause, "read inside-out" and the claim that estimates will move closer after ANALYZE (none is on the pages; the page says estimates may change after a fresh ANALYZE run).
Method: documentation only; no commands were run.
