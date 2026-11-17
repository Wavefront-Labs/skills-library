---
id: computing-software.database-administration.pgbackrest.stanza-pg-options
name: stanza-pg-options
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, pg1-path, pg-host, stanza, postgresql-connection]
level: practitioner
status: docs-checked
description: "The pgN options that tell pgBackRest how to find and connect to PostgreSQL clusters."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect to the right cluster with the right user.

Indexed `pgN-` options describe each cluster in a stanza (pg1 is the primary in examples; a standby is pg2).

- `pg-path`: should equal the `data_directory` PostgreSQL reports. Set it even though it can be read elsewhere, because those resources may be unavailable during restore or offline backup. It is checked against PostgreSQL on every online backup.
- `pg-port` (default 5432), `pg-database` (default `postgres`; PGDATABASE is ignored for legacy reasons).
- `pg-socket-path`: only needed if `unix_socket_directories` was changed from the OS default.
- `pg-user`: connect user; if unset, pgBackRest uses the local OS user or PGUSER.
- `pg-host`, `pg-host-type` (ssh or tls), `pg-host-user` (default `postgres`, should be the cluster owner), `pg-host-cmd`, `pg-host-config` for a remote database host.

```
[demo]
pg1-path=/path/to/pgdata
pg1-user=backupuser
pg1-socket-path=/var/run/postgresql
```

Stanza names should describe the function of the cluster, such as `app` or `dw`, rather than the local cluster name like `main`, because the same name serves the primary and all replicas.

After a major upgrade, update `pg1-path` on all hosts and run `stanza-upgrade`.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest Command Reference (pgbackrest.org/command.html) (stanza naming). Nothing needed removing. 

Method: documentation only; no commands were run.
