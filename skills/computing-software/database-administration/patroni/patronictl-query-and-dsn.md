---
id: computing-software.database-administration.patroni.patronictl-query-and-dsn
name: patronictl-query-and-dsn
category: computing-software
field: database-administration
product: patroni
tags: [patroni, patronictl, query, dsn, connection-string]
level: practitioner
status: docs-checked
description: "Run SQL on a chosen member with patronictl query and get a connection string with patronictl dsn."
sources:
  - https://patroni.readthedocs.io/en/latest/patronictl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reach the right member from scripts.

`patronictl dsn [CLUSTER] [-r ROLE | -m MEMBER] [--group N]` prints the connection string of one member. If several match, the primary is preferred.

```
patronictl -c postgres0.yml dsn batman -r primary
host=127.0.0.1 port=5432
```

Roles: `leader` (regular or standby cluster leader), `primary`, `standby-leader`, `replica`, `standby` (same as replica), `any`.

`patronictl query [CLUSTER] [-r ROLE | -m MEMBER] [-d DBNAME] [-U USER] [--password] [--format pretty|tsv|json|yaml] [-f FILE | -c SQL] [--delimiter] [-W | -w SECONDS]`:
- `-d` defaults to the username; `-U` defaults to the OS user running patronictl.
- `--password` prompts; otherwise libpq mechanisms such as `PGPASSWORD` or a pgpass file apply.
- Output format defaults to `tsv`; `--delimiter` sets the tsv delimiter (tab if omitted).
- `-W` reruns every 2 seconds; `-w` sets the interval.

```
patronictl -c postgres0.yml query batman -r replica -c "SHOW port"
patronictl -c postgres0.yml query batman -m postgresql2 -c "SHOW port"
```

The first picks any standby, the second a named member. Use `--group` to target a Citus group in either command.

## Checked

2026-11-03. Confirmed against the patronictl page: `dsn` synopsis, roles, `--group`, examples, and `query` options and defaults.

Method: documentation only; no commands were run.
