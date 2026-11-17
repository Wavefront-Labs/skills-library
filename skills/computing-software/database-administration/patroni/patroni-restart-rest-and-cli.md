---
id: computing-software.database-administration.patroni.patroni-restart-rest-and-cli
name: patroni-restart-rest-and-cli
category: computing-software
field: database-administration
product: patroni
tags: [patroni, restart, patronictl, pending-restart, rest-api]
level: practitioner
status: docs-checked
description: "Restart PostgreSQL through Patroni with conditions, scheduling and timeouts, via patronictl or POST /restart."
sources:
  - https://patroni.readthedocs.io/en/latest/patronictl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restart Postgres without confusing the HA loop.

CLI:

```
patronictl restart CLUSTER [MEMBER...] [-r ROLE] [--any] [--pg-version V] [--pending] [--timeout SEC] [--scheduled TIMESTAMP] [--force]
```

- `-r/--role`: leader, primary, standby-leader, replica, standby or any.
- `--any`: restart one random matching node.
- `--pg-version`: only members whose Postgres is older than the given version.
- `--pending`: only members flagged Pending restart.
- `--timeout`: abort the restart if it takes longer than the given seconds, and fail over to a replica if the primary is the problem.
- `--scheduled`: unambiguous timestamp, or the literal `now`.

REST `POST /restart` accepts optional conditions in the JSON body: `restart_pending` (bool), `role`, `postgres_version`, `timeout` (wait before Postgres accepts connections; overrides `primary_start_timeout`) and `schedule` (timestamp with time zone). `DELETE /restart` removes a scheduled restart (used by `patronictl flush CLUSTER restart`).

`patronictl flush CLUSTER [MEMBER...] restart|switchover [-r ROLE] [--force]` discards scheduled events.

Do not restart Postgres by restarting the Patroni service on the primary; that can cause a failover. `patronictl reload CLUSTER [MEMBER...]` also triggers `pg_ctl reload` even when nothing changed. The reload request is processed within 10 seconds in the documented example.

## Checked

2026-11-03. Confirmed against the patronictl page (restart, flush and reload synopses and options, including the 10 second reload message), the REST API page (`POST`/`DELETE /restart` conditions) and patroni_configuration (do not restart Patroni to restart Postgres).

Method: documentation only; no commands were run.
