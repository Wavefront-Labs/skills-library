---
id: computing-software.database-administration.postgresql.auto-explain-slow-plan-logging
name: auto-explain-slow-plan-logging
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-monitoring, auto-explain, log-min-duration, slow-query, execution-plan, log-analyze, session-preload-libraries, plan-regression]
level: practitioner
status: verified
description: "Log the execution plan of slow PostgreSQL queries automatically with auto_explain: safe settings, sampling, and per-session loading for diagnosis."
sources:
  - https://www.postgresql.org/docs/current/auto-explain.html
  - https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-SESSION-PRELOAD-LIBRARIES
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging slow plans with auto_explain

**Goal:** capture the plan a slow query actually ran with, in production, without re-running it.

## Enable server-wide
```ini
# postgresql.conf
session_preload_libraries = 'auto_explain'   # new sessions pick it up after reload; shared_preload_libraries needs restart
auto_explain.log_min_duration = '500ms'
auto_explain.log_analyze = on        # actual rows/time; adds timing overhead
auto_explain.log_timing = off        # keep row counts, drop per-node clock calls (cheap)
auto_explain.log_buffers = on
auto_explain.log_format = 'json'     # or text; json parses into tools like explain.dalibo.com
auto_explain.log_nested_statements = on   # include statements inside functions
auto_explain.sample_rate = 0.1       # explain 10% of statements per session (nested statements: all or none)
```
`SELECT pg_reload_conf();` then open a new session.

## One session only (diagnosis)
```sql
LOAD 'auto_explain';                       -- superuser, or library in $libdir/plugins
SET auto_explain.log_min_duration = 0;
SET auto_explain.log_analyze = on;
-- run the app code path / statement
```

## Overhead
- `log_analyze = on` instruments every statement (it cannot know a query will be slow beforehand); the docs describe the per-node timing cost as potentially "extremely negative" for performance (not benchmarked here). Use `log_timing = off` and `sample_rate`.
- `log_min_duration` without `log_analyze` is nearly free: it logs the estimated plan only.

## Reading the output
Look for estimated vs actual rows off by 10x+ (stale stats or correlation), `Rows Removed by Filter` large (missing index), `Buffers: shared read` large (cold cache), sort/hash `Disk:` (raise `work_mem` for that query).

## Gotchas
- `auto_explain.log_parameter_max_length` (PG16+; default -1 = log bound parameter values in full, 0 = none) controls parameter values in the logged plan; they can contain PII.
- Large JSON plans bloat logs; pair with log rotation and `log_min_duration` high enough.

## Verify
`SELECT pg_sleep(1)` with `log_min_duration = 500ms` writes a `duration: ... plan:` entry to the server log (JSON when `log_format = json`; with `log_analyze = off` the plan has estimates only, no `Actual` fields).

## Checked
- PostgreSQL 18.6 (EDB Windows binaries, scratch cluster): the settings block loads with `session_preload_libraries = 'auto_explain'`; `SELECT pg_sleep(1)` at `log_min_duration = 500ms` logged `duration: 1014 ms plan:` as JSON with `Actual Rows` and buffer counters; with `log_analyze = off` the text plan showed only `cost=` estimates; `log_timing = off`, `log_nested_statements`, `sample_rate` accepted.
- Docs (auto-explain page, 18 and 14/15/16 versions): `LOAD` needs superuser; `log_parameter_max_length` appears in the 16 page and not in 14 or 15; default -1, 0 disables; `sample_rate` explains a fraction of statements per session; `log_analyze` timing warning wording. `sql-load` page: non-superusers may only LOAD from `$libdir/plugins/`. `session_preload_libraries` is read at connection start.
- Links in `sources` return 200; explain.dalibo.com returns 200.
