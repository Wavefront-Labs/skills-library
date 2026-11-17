---
id: computing-software.database-administration.duckdb.duckdb-profiling-settings
name: duckdb-profiling-settings
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, profiling, explain, enable-profiling, query-plan, optimizer]
level: practitioner
status: docs-checked
description: "Configure DuckDB profiling and EXPLAIN output: enable_profiling formats, coverage, mode, output file, custom metrics, and disabled_optimizers for debugging."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/configuration/pragmas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: see where a slow query spends its time, and control how much plan detail is recorded.

Enable (mandatory for any profiling format):

```sql
PRAGMA enable_profiling;           -- alias enable_profile; default format query_tree
SET enable_profiling = 'json';     -- query_tree | json | query_tree_optimizer | no_output
PRAGMA disable_profiling;          -- alias disable_profile
```
- `query_tree`: physical plan with per-operator metrics. `json`: same plan as JSON. `query_tree_optimizer`: adds optimizer and planner metrics. `no_output`: only affects printing to the configured output; when reading profiling information through API calls, profiling must still be enabled.

Scope and detail:
- `SET profiling_coverage = 'SELECT'` (default; only SELECT operators) or `'ALL'` (also INSERT, ATTACH, ...).
- `SET profiling_mode = 'standard'` (default) or `'detailed'` (adds planner and optimizer stages).
- `SET profiling_output = '/path/to/file.json'` (alias `profile_output`) writes to a file instead of stdout; the file is overwritten by every query so it holds only the last one.
- `SET custom_profiling_settings = '{"CPU_TIME": "false", "EXTRA_INFO": "true", "OPERATOR_CARDINALITY": "true", "OPERATOR_TIMING": "true"}';` toggles individual metrics (JSON of metric name to "true"/"false"). It only affects `json` and `no_output`; the tree formats always use a default metric set.

EXPLAIN output: `SET explain_output = 'physical_only'` (default), `'optimized_only'`, or `'all'`.

Progress bar: `PRAGMA enable_progress_bar;` / `PRAGMA disable_progress_bar;` (print variants `enable_print_progress_bar`, `disable_print_progress_bar`).

Debugging optimizer effects (not for production): `PRAGMA disable_optimizer;` / `enable_optimizer`, or selectively `SET disabled_optimizers = 'filter_pushdown,statistics_propagation';`; list names with `duckdb_optimizers()`; restore with `SET disabled_optimizers = '';`.

Query log: `SET log_query_path = '/tmp/duckdb_log/';` logs queries; `''` turns it off (the newer logger is in duckdb-logging).

## Checked

2026-11-07. Read the DuckDB 1.4 docs page configuration/pragmas.md in full. Confirmed: enable_profiling formats and aliases, query_tree default, profiling_coverage SELECT/ALL, profiling_mode standard/detailed, profiling_output with alias and overwrite warning, custom_profiling_settings example and its json/no_output limitation, explain_output values, the progress-bar PRAGMAs, disable_optimizer, disabled_optimizers with `duckdb_optimizers()` and the debugging-only warning, log_query_path. Removed: the `progress_bar_time` setting and its 2000 ms default (not on the page), the claim that no_output "records metrics" (reworded to the page's text), and the invented Verify step.

Method: documentation only; no commands were run.
