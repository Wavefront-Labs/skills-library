---
id: computing-software.database-administration.sqlite.scripting-the-sqlite3-shell
name: scripting-the-sqlite3-shell
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-parameter, sqlite3-shell, sqlite-cli, shell-scripting, bail]
level: practitioner
status: verified
description: "Script the sqlite3 shell safely in CI and cron: -bail, -cmd, heredocs, .parameter bindings instead of string interpolation, exit codes, and .read for SQL files."
sources:
  - https://sqlite.org/cli.html#sql_parameters
  - https://sqlite.org/cli.html#command_line_options
  - https://sqlite.org/cli.html#reading_sql_from_a_file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scripting the sqlite3 shell non-interactively

## Exit on first error
```bash
sqlite3 -bail app.db < migrate.sql || { echo "migration failed"; exit 1; }
```
Without `-bail`, the shell reports errors and continues with later statements (3.54.1: after a UNIQUE failure on line 3 the next insert still ran, and the exit code was 1 in both the continue and `-bail` cases; with `-bail` nothing after the error ran). Check `$?` on your shell version rather than assuming. Wrap migrations in `BEGIN; ... COMMIT;` so a failure leaves nothing half-applied.

## Pre-commands and heredocs
```bash
sqlite3 -bail -cmd '.timeout 5000' -cmd 'PRAGMA foreign_keys=ON' app.db <<'SQL'
BEGIN;
UPDATE accounts SET plan='pro' WHERE id IN (SELECT account_id FROM upgrades);
COMMIT;
SQL
```
Quote the heredoc delimiter (`'SQL'`) so the shell does not expand `$` inside SQL.

## Parameters instead of interpolation
```bash
sqlite3 app.db \
  -cmd ".parameter set :email \"'o''brien@example.com'\"" \
  -cmd ".parameter set :days 30" \
  "SELECT id FROM users WHERE email = :email AND created_at > date('now', '-' || :days || ' days')"
```
`.parameter set` values are evaluated as SQL literals (quote strings, double embedded quotes). The dot-command line has its own quoting, so wrap the whole SQL literal in double quotes as above: the bare form `.parameter set :email 'o''brien@example.com'` was split into extra arguments and printed the `.parameter` usage instead of setting anything (3.54.1). `.parameter list`, `.parameter clear`. Parameters live in the temp table `sqlite_parameters`. This avoids SQL injection from shell variables containing quotes, which raw `"... WHERE email='$EMAIL'"` invites.

## Files and includes
```text
.read schema.sql
.read '|./generate.sh'      -- read output of a command (cli.html: ".read FILE: Read input from FILE or command output")
```
`-init file` replaces `~/.sqliterc` for reproducible runs; `-batch` forces batch mode even on a TTY.

## Read-only and safety
```bash
sqlite3 -readonly app.db "SELECT ..."       # cannot write
sqlite3 -safe app.db < untrusted.sql         # disables .shell, .system, file I/O commands
```

## Verify
`echo $?` after a deliberate failing statement with `-bail` is non-zero; your CI job fails when a migration statement errors.
