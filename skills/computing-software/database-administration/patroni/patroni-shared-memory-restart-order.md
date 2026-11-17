---
id: computing-software.database-administration.patroni.patroni-shared-memory-restart-order
name: patroni-shared-memory-restart-order
category: computing-software
field: database-administration
product: patroni
tags: [patroni, restart, max-connections, shared-memory, pending-restart]
level: advanced
status: docs-checked
description: "Restart ordering when changing max_connections and other shared-memory GUCs, and why systemctl restart is risky."
sources:
  - https://patroni.readthedocs.io/en/latest/patroni_configuration.html
  - https://patroni.readthedocs.io/en/latest/patronictl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change shared-memory parameters without crash loops.

The parameters are `max_connections`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_wal_senders` and `max_worker_processes`. Changing them needs a PostgreSQL restart, and their shared memory structures cannot be smaller on a standby than on the primary.

Procedure: apply the change with `patronictl edit-config` (or REST `/config`), then restart with `patronictl restart` (or REST `/restart`).

Order:
- Increasing a value: restart all standbys first, then the primary.
- Decreasing a value: restart the primary first, then all standbys.

If you decrease a value and restart every node in one go, Patroni ignores the change and restarts the standby with the original value, so you must restart the standbys again later. It does this to prevent an infinite crash loop: PostgreSQL exits with FATAL when a parameter is lower than what pg_controldata shows on the standby.

Restart Postgres through `patronictl restart` or the `/restart` endpoint. Restarting the Patroni daemon, for instance with `systemctl restart patroni`, can cause a failover if done on the primary.

To find nodes needing a restart, use `patronictl restart <cluster> --pending`, or look for the `*` in the Pending restart column of `patronictl list -e`.

## Checked

2026-11-08: the shared-memory parameter list, restart ordering, the ignore-and-restart-again behaviour and the systemctl warning confirmed in the Patroni configuration page; restart --pending and the Pending restart column confirmed in the patronictl page. Pages were read in full except where noted. Partial read: the patronictl page was read for the list and restart sections only.

Method: documentation only; no commands were run.
