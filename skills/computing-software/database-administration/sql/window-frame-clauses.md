---
id: computing-software.database-administration.sql.window-frame-clauses
name: window-frame-clauses
category: computing-software
field: database-administration
product: sql
tags: [sql, window-frame-clauses]
level: advanced
status: docs-checked
description: "Define window frames precisely with ROWS, RANGE, GROUPS and EXCLUDE."
sources: ["https://www.postgresql.org/docs/current/sql-expressions.html", "https://www.sqlite.org/windowfunctions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Window frames ROWS RANGE and GROUPS

- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` counts individual rows. `RANGE` looks at ORDER BY values within a band of the current row, and peers (rows the ORDER BY sorts as equivalent) share a frame. `GROUPS` counts peer groups before or after the current row's group, and needs an ORDER BY in the window definition (PostgreSQL).
- In RANGE and GROUPS mode a `CURRENT ROW` start means the first peer and a `CURRENT ROW` end means the last peer. In ROWS mode it is just the current row.
- If `frame_end` is omitted, the end defaults to CURRENT ROW.
- The default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. With ORDER BY that runs from the partition start through the current row's last peer, so ties get the same running total; without ORDER BY every row of the partition is a peer, so the frame is the whole partition.
- `EXCLUDE CURRENT ROW | GROUP | TIES | NO OTHERS` trims the frame. NO OTHERS is the default. GROUP removes the current row and its peers; TIES keeps the current row but removes its peers. In SQLite, peers for EXCLUDE are rows with the same ORDER BY values even in ROWS mode.
- SQLite: window functions arrived in 3.25.0 (2018-09-15); EXCLUDE, GROUPS frames and `<expr> PRECEDING/FOLLOWING` in RANGE frames arrived in 3.28.0 (2019-04-16).
- Self-check: use duplicate ORDER BY values and compare ROWS versus RANGE results.

## Checked

2026-11-08. Confirmed against PostgreSQL Window Function Calls (in the Value Expressions chapter) and the SQLite Window Functions page: frame modes, peer semantics, CURRENT ROW meaning, default frame, EXCLUDE options, GROUPS ORDER BY requirement and the SQLite version dates. Removed the "PostgreSQL 11+" GROUPS claim, which the current page does not state.

Method: documentation only; no commands were run.
