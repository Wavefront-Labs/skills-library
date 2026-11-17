---
id: computing-software.database-administration.patroni.patroni-barman-integration
name: patroni-barman-integration
category: computing-software
field: database-administration
product: patroni
tags: [patroni, barman, backup, patroni-barman, recovery]
level: advanced
status: docs-checked
description: "Use patroni_barman recover for bootstrap and replica creation and config-switch for role changes."
sources:
  - https://patroni.readthedocs.io/en/latest/tools_integration.html
  - https://patroni.readthedocs.io/en/latest/replica_bootstrap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect Barman backups to Patroni lifecycle hooks.

Patroni ships `patroni_barman`, which talks to pg-backup-api so Barman operations run remotely. Sub-commands: `recover` and `config-switch`. Barman and pg-backup-api must be configured on the Barman host so a remote `barman recover` can run through the API.

Bootstrap a new cluster from Barman:

```
bootstrap:
  method: barman
  barman:
    keep_existing_recovery_conf: true
    command: patroni_barman --api-url https://barman-host:7480 recover
    barman-server: my_server
    ssh-command: ssh postgres@patroni-host
```

Create replicas from Barman:

```
postgresql:
  create_replica_methods:
    - barman
    - basebackup
  barman:
    command: patroni_barman --api-url https://barman-host:7480 recover
    barman-server: my_server
    ssh-command: ssh postgres@patroni-host
  basebackup:
    max-rate: '100M'
```

`patroni_barman recover --help` lists all parameters. `config-switch` is intended as an `on_role_change` callback: after failover it applies a Barman model on top of a server configuration so WALs stream from the new primary. Bootstrap methods are not chained and do not fall back to initdb. With `keep_existing_recovery_conf: true`, Patroni keeps recovery settings produced by the restore (recovery.signal/standby.signal on PostgreSQL 12+), so the backup tool's own recovery configuration is used. The example uses only a subset of the available parameters.

## Checked

2026-11-08: patroni_barman sub-commands, config-switch purpose and requirements confirmed in the tools integration page; the bootstrap and create_replica_methods examples, keep_existing_recovery_conf and the no-fallback note confirmed in the replica bootstrap page. Pages were read in full except where noted.

Method: documentation only; no commands were run.
