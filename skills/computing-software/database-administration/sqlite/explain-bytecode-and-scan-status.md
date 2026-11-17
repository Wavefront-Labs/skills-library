---
id: computing-software.database-administration.sqlite.explain-bytecode-and-scan-status
name: explain-bytecode-and-scan-status
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-explain-bytecode, explain, vdbe, sqlite-query-planner, scanstatus]
level: practitioner
status: verified
description: "Read SQLite EXPLAIN bytecode (VDBE opcodes) to confirm exactly how a statement executes, when EXPLAIN QUERY PLAN is not detailed enough, and pair it with scan status."
sources:
  - https://sqlite.org/opcode.html
  - https://sqlite.org/eqp.html
  - https://sqlite.org/c3ref/stmt_scanstatus.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EXPLAIN bytecode and scan status

**Goal:** prove which index, loops, sorters and subroutines a statement uses. `EXPLAIN QUERY PLAN` summarises; `EXPLAIN` shows the program the virtual machine (VDBE) runs.

## Run
```text
.mode box
EXPLAIN SELECT name FROM users WHERE email = 'a@x.io';
```
Columns: `addr`, `opcode`, `p1..p5`, `comment` (comments present when built with `SQLITE_ENABLE_EXPLAIN_COMMENTS`, as the 3.54.1 shell is). The shell indents loop bodies to make structure visible.

## Opcodes worth recognising
| Opcode | Meaning |
|---|---|
| `OpenRead` p2 = root page | Opens a table or index B-tree (find which via `sqlite_schema.rootpage`) |
| `Rewind` / `Next` | Full scan loop |
| `SeekGE` / `SeekLE` / `IdxGT` | Index range seek and end check |
| `SeekRowid` (`WHERE id=5` on 3.54.1) / `NotExists` (rowid existence check, seen in an INSERT's uniqueness test) | Rowid lookup |
| `DeferredSeek` / `IdxRowid` | Index → table lookup (not covering) |
| `SorterOpen` / `SorterSort` | Temp B-tree sort (ORDER BY/GROUP BY not satisfied by index) |
| `OpenAutoindex` | Automatic transient index built for this query |
| `BeginSubrtn` / `Return` (older versions `Gosub`) | Subroutine, e.g. a correlated subquery (3.54.1 emitted `BeginSubrtn` ... `Return` for a scalar correlated subquery) |
| `Function` / `PureFunc` | Function call per row (3.54.1 showed `Function` for `abs(age)` and `lower(name)`) |
| `Halt` | End |

Map root pages:
```sql
SELECT name, rootpage FROM sqlite_schema;
```

## Typical findings
- `OpenAutoindex` every run: create a permanent index on that join column.
- `SorterOpen` for ORDER BY: add an index matching the order or accept the sort.
- `DeferredSeek` per row: a covering index could avoid table lookups.
- Correlated subquery executed per row (`Gosub` in the loop): rewrite as a join.

## Scan status
With `SQLITE_ENABLE_STMT_SCANSTATUS` (present in the 3.54.1 shell's `PRAGMA compile_options`; the Python 3.14 build tested, 3.50.4, did not list it), `sqlite3_stmt_scanstatus_v2()` (C) or the shell's `.scanstats on|off|est` reports per plan element after execution. In 3.54.1 `.scanstats on` printed a table with `Cycles`, `Loops` and `Rows` columns (e.g. `SCAN users 601 56% 1 1000`); `.scanstats est` adds the estimates.

## Gotchas
- Bytecode is not a stable interface and changes between versions; use it for diagnosis, not automated assertions.

## Verify
Confirm the presence (or absence) of the opcode you expected, e.g. `SeekGE` on the index's root page after adding the index.
