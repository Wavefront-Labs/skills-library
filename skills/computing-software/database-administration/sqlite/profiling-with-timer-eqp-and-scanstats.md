---
id: computing-software.database-administration.sqlite.profiling-with-timer-eqp-and-scanstats
name: profiling-with-timer-eqp-and-scanstats
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-timer, sqlite-eqp, scanstats, sqlite-performance, sqlite3-shell]
level: practitioner
status: verified
description: "Profile SQLite queries in the shell with .timer, .eqp on/full/trigger and .scanstats to compare plans and actual loop counts before adding indexes."
sources:
  - https://sqlite.org/cli.html#special_commands_to_sqlite3_dot_commands_
  - https://sqlite.org/eqp.html
  - https://sqlite.org/c3ref/stmt_scanstatus.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling with .timer / .eqp / .scanstats

## Timing
```text
.timer on
SELECT count(*) FROM orders WHERE customer_id = 42;
Run Time: real 0.183 user 0.170 sys 0.012
```
Run twice: the first run includes cold page cache reads. `real` much greater than `user+sys` means waiting on I/O or locks.

## Show plans automatically
```text
.eqp on        -- EXPLAIN QUERY PLAN before each statement's output
.eqp full      -- also full EXPLAIN bytecode
.eqp trigger   -- like full, but also shows the bytecode of triggers fired (`.help eqp`; an INSERT with a trigger printed a `-- TRIGGER tr` program)
.eqp off
```
Output like:
```text
QUERY PLAN
`--SCAN orders
```
vs after an index:
```text
`--SEARCH o USING COVERING INDEX idx_o_c (customer_id=?)
```
(run on 3.54.1: `SCAN o` became `SEARCH o USING COVERING INDEX idx_o_c (customer_id=?)` after `CREATE INDEX idx_o_c ON o(customer_id)`).

## Actual row counts (.scanstats; requires SQLITE_ENABLE_STMT_SCANSTATUS, enabled in the sqlite.org 3.54.1 shell build)
```text
.scanstats on
SELECT count(*) FROM o JOIN c ON c.id=o.customer_id WHERE o.v>100;
                                                  Cycles      Loops  Rows
                                                  ----------  -----  -----
QUERY PLAN                                        27.7K 100%
|--SCAN o                                         12.9K  47%     1   20.0K
`--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)   5121   19%  19.9K  19.9K
```
(Real output of 3.54.1 on a 20,000-row test; older shells printed a different layout.) `loops` and `rows` show where work happens; `.scanstats est` adds `(est)` columns for loops and rows (it printed 983K estimated rows against 20.0K actual before `ANALYZE`), revealing bad statistics (run `ANALYZE`). The release log credits `.scanstats est` to 3.41.0.

## Workflow
1. `.timer on` and `.eqp on`, run the slow query.
2. Look for `SCAN` on large tables, `USE TEMP B-TREE FOR ORDER BY`, and `AUTOMATIC` indexes (3.54.1 printed `SEARCH a USING AUTOMATIC PARTIAL COVERING INDEX (v=?)` with a `BLOOM FILTER`).
3. Try an index or rewrite; compare `Run Time` and plan.
4. `.expert` (shell) suggests indexes for a query.

## Gotchas
- The shell's numbers are for one connection on one machine; production with concurrent writers may block on locks, which `.timer` will not show.
- `.scanstats` needs a build with `SQLITE_ENABLE_STMT_SCANSTATUS`: the sqlite.org 3.54.1 shell listed it in `PRAGMA compile_options`, the Python 3.14 module (SQLite 3.50.4) did not.

## Verify
After the fix the plan changes from `SCAN` to `SEARCH ... USING INDEX` and real time drops on warm cache runs.
