---
id: computing-software.data-engineering.dbt.debugging-macros-and-compiled-sql
name: debugging-macros-and-compiled-sql
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-debugging, dbt-compile, dbt-show, log-function, compiled-sql, dbt-debug, jinja-errors]
level: practitioner
status: docs-checked
description: "Debug dbt models and macros: dbt compile and dbt show, target/compiled vs target/run, log() and print(), --debug logs, dbt debug for connections, and reading Jinja errors."
sources:
  - https://docs.getdbt.com/reference/commands/compile
  - https://docs.getdbt.com/reference/commands/show
  - https://docs.getdbt.com/reference/dbt-jinja-functions/log
  - https://docs.getdbt.com/reference/dbt-jinja-functions/print
  - https://docs.getdbt.com/reference/commands/debug
  - https://docs.getdbt.com/guides/debug-errors
  - https://docs.getdbt.com/reference/global-configs/logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging macros and compiled SQL

**Goal:** see exactly what SQL dbt sends and why a macro produced it.

## See the SQL
```bash
dbt compile --select fct_orders               # compiled SQL goes to the terminal and target/compiled/
dbt compile --inline "select * from {{ ref('raw_orders') }}"
dbt show --select fct_orders --limit 20      # default is the first 5 rows; --limit n adds a SQL limit
dbt show --inline "select * from {{ ref('stg_orders') }} where amount < 0" --limit 50
```
- `target/compiled/`: select statements you can run in any query editor.
- `target/run/`: the SQL dbt executes to build your models.

## Print from Jinja
```jinja
{% do log("some value", info=true) %}                                      {# info=true: log file and stdout #}
{{ log("log file only") }}                                                {# info=false (default): log file only #}
{% do print("printed to log file and stdout") %}
```
Code that relies on database results errors during the parse phase; guard it with `execute`.

## Verbose logging
```bash
dbt --debug run -s fct_orders          # display debug logging
dbt run --log-format json              # json, text or default console format
# logs/dbt.log holds the debug-level log file
```
Warehouse side: the `query-comment` project config adds a comment to dbt queries so they can be found in query history.

## Connection and environment issues
```bash
dbt debug                      # checks project file, dependencies (such as git) and the database connection
dbt debug --config-dir         # prints the profiles directory location
dbt parse && dbt ls -s fct_orders --output json     # does it resolve? which config applied?
```

## Reading common errors
| Error | Usually |
|---|---|
| `Compilation Error ... 'None' has no attribute` | `run_query` / introspection at parse time; guard with `execute` |
| `depends on a node named 'x' which was not found` | the referenced model does not exist: check the name in `ref` |
| `Database Error` | the SQL failed at execution: open the matching file in `target/run/` and run it in the warehouse console |
| `Syntax error near line N` (Compilation Error) | Jinja or SQL syntax error in the named file |

## Gotchas
- Ephemeral models are interpolated as CTEs into dependents, so their SQL appears in the compiled dependent model.
- `dbt show` runs a query against the warehouse, so use `--limit`; `--inline` can run arbitrary SQL, so use a read-only role.

## Verify
- [ ] Reproduce the failing SQL from `target/run` directly in the warehouse.
- [ ] Fix confirmed with `dbt build -s model+` (model and its tests/children).

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt compile, show, debug and log/print docs, the debug-errors guide and logs docs: `--select` and `--inline` for compile and show, `show` default of 5 rows and `--limit` applied as a SQL limit, `target/compiled` vs `target/run`, `log(msg, info)` and `print()` behaviour, `execute` parse-phase error, `dbt debug` checks and `--config-dir`, `--debug`, `--log-format`, `logs/dbt.log`, `Compilation Error` and `Database Error` stages, and the missing-node and syntax error messages. Removed unconfirmed claims about double rendering, `dbt clean` advice and specific macro-signature errors.

Method: documentation only; no commands were run.
