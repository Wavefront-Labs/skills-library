---
id: computing-software.database-administration.postgresql.logging-configuration
name: logging-configuration
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgresql-conf, log-line-prefix, log-min-duration-statement, jsonlog, log-lock-waits, log-autovacuum-min-duration, log-temp-files, pgbadger, log-checkpoints]
level: practitioner
status: verified
description: "Configure PostgreSQL logging for operations: a useful log_line_prefix, slow-statement logging, lock waits, temp files, autovacuum, checkpoints, and JSON logs for pgBadger or a log stack."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-logging.html
  - https://pgbadger.darold.net/documentation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL logging configuration

**Goal:** the log answers "what was slow, what waited, what spilled to disk, and
what was vacuum doing" without drowning the disk.

## A production baseline (all reloadable)
```conf
log_destination = 'jsonlog'            # PG15+; or 'stderr' / 'csvlog'; needs logging_collector = on (restart)
log_line_prefix = '%m [%p] %q%u@%d app=%a client=%h '   # used by stderr format
log_min_duration_statement = '500ms'   # log statements slower than this, with duration
log_lock_waits = on                    # waits longer than deadlock_timeout (1s)
log_temp_files = '64MB'                # sorts/hashes spilling to disk: work_mem hints
log_autovacuum_min_duration = '10s'    # PG15 default 10min; lower to see vacuum activity
log_checkpoints = on                   # default on since PG15
log_connections = off                  # on for auditing; noisy with poolers (PG18: also a list of stages, booleans still accepted)
log_statement = 'ddl'                  # record schema changes
log_min_error_statement = error
```
`%m` ms timestamp, `%p` pid, `%q` stops non-session processes printing the rest,
`%u` user, `%d` database, `%a` application_name, `%h` client host, `%x` xid.

## Sampling instead of logging everything
```conf
log_min_duration_sample = '50ms'
log_statement_sample_rate = 0.05        # 5% of statements between 50ms and 500ms
log_transaction_sample_rate = 0.001     # all statements of 0.1% of transactions
```
For plans of slow queries use `auto_explain`; for aggregate stats `pg_stat_statements`.

## Reports
```bash
pgbadger --format jsonlog /var/log/postgresql/postgresql-*.json -o report.html
```
pgBadger auto-detects the format; for stderr logs with a custom `log_line_prefix` pass `--prefix` with the same string (`--format` forces `jsonlog` etc.).

## Gotchas
- `log_min_duration_statement = 0` logs every statement and can produce very large logs and overhead on a busy server.
- Statements are logged with literal parameters: PII and secrets end up in logs
  (`log_parameter_max_length`, since PG13, limits logged bind values; default -1 = in full). Restrict log access.
- Logs inside the data directory (`log_directory = 'log'`, default) are included
  in base backups and can fill the data volume; ship them elsewhere and rotate
  (see log rotation skill).

## Verify
With a threshold below 1s, run `SELECT pg_sleep(1);` and see a `duration: ...` entry (in JSON, the `message` field) with the prefix fields; `log_statement = 'ddl'` writes `statement: CREATE TABLE ...`;
`SHOW log_destination;` and the newest file under `log_directory` match.

## Checked
- PostgreSQL 18.6: every parameter in the baseline and sampling blocks was accepted by `ALTER SYSTEM` and reload with no `pg_file_settings` error and none left `pending_restart`; with `jsonlog` the file `postgresql-Thu.json` held `duration: ...` entries for `pg_sleep` and `statement: CREATE TABLE ...` for DDL. `pg_settings` defaults: `log_autovacuum_min_duration` 600000 ms (10 min), `log_checkpoints` on, `log_lock_waits` off, `log_temp_files` -1, `log_min_duration_sample` -1, `log_statement_sample_rate` 1, `log_transaction_sample_rate` 0, `log_parameter_max_length` -1; `log_connections` is a string in 18 (boolean values still accepted).
- Docs/release notes: PG15 added `jsonlog` and flipped the `log_checkpoints` and `log_autovacuum_min_duration` defaults; `log_parameter_max_length` appears in the 13 release notes (the skill said PG16: fixed); `%q` and `%x` meanings; sampling parameter semantics; 18 notes on `log_connections`; pgBadger README (`--format` values include `jsonlog`, `--prefix`).
