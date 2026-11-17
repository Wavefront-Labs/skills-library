---
id: computing-software.database-administration.sql.generate-series-sequences
name: generate-series-sequences
category: computing-software
field: database-administration
product: sql
tags: [sql, generate-series-sequences]
level: intro
status: docs-checked
description: "Generate number, date and timestamp sequences and synthetic rows."
sources: ["https://www.postgresql.org/docs/current/functions-srf.html", "https://www.sqlite.org/series.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# generate_series for numbers and test data

- `SELECT g FROM generate_series(1, 10) g;` takes a step: `generate_series(0, 100, 10)`; timestamp series take an interval step.
- SQLite: the `generate_series(START,STOP,STEP)` table-valued function is a loadable extension in the SQLite source tree, compiled into the command-line shell; otherwise use a recursive CTE.
- Self-check: `count(*)` equals the expected rows.

## Checked

2026-11-02. Confirmed: generate_series with optional step and timestamp/interval forms (PostgreSQL set-returning functions page); SQLite generate_series extension (series page). Removed: the md5 test-data example and the random() volatility claim.
Method: documentation only; no commands were run.
