---
id: computing-software.database-administration.sql.lag-lead-first-last-value
name: lag-lead-first-last-value
category: computing-software
field: database-administration
product: sql
tags: [sql, lag-lead-first-last-value]
level: practitioner
status: docs-checked
description: "Access neighbouring rows with LAG and LEAD and frame-edge rows with FIRST_VALUE."
sources: ["https://www.postgresql.org/docs/current/functions-window.html", "https://www.sqlite.org/windowfunctions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LAG LEAD FIRST_VALUE LAST_VALUE NTH_VALUE

- `lag(v, 1, 0) OVER (PARTITION BY k ORDER BY ts)` returns v from the row `offset` rows before within the partition, and the default (here 0) when there is no such row. Offset defaults to 1 and default to NULL. `lead` looks forward.
- Delta: `v - lag(v) OVER (...)`.
- `first_value`, `last_value` and `nth_value` consider only the window frame. The default frame runs from the start of the partition through the last peer of the current row, so `last_value` usually returns the current row (or its last peer), not the partition end. Add `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` to fix this.
- `nth_value(v, 3)` returns the 3rd row of the frame (counting from 1), or NULL if there is none.
- `lag` and `lead` ignore the frame specification; they depend on the `ORDER BY` of the window.
- SQLite supports window functions from 3.25.0 with the same names and the same default frame (`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`).
- Self-check: the first row of each partition has NULL lag unless a default is supplied.

## Checked

2026-11-08. Confirmed on the PostgreSQL window functions page: signatures and defaults of `lag`/`lead`, definitions of `first_value`, `last_value`, `nth_value`, and the default-frame warning. Confirmed on the SQLite window functions page: NULL or supplied default, frame handling, default frame and 3.25.0. Corrected "returns the current row" to include peers. The statement that lag and lead ignore the frame is from the SQLite page ("most built-in window functions ignore the frame-spec, the exceptions being first_value(), last_value() and nth_value()").
Method: documentation only; no commands were run.
