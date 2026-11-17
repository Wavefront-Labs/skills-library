---
id: computing-software.database-administration.dragonfly.configure-replicaof
name: configure-replicaof
category: computing-software
field: database-administration
product: dragonfly
tags: [replicaof, replication, masterauth, primary-replica, dragonfly]
level: practitioner
status: docs-checked
description: "Make a Dragonfly instance replicate another with REPLICAOF host port, including masterauth, the replicaof flag and what happens to existing data."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/replicaof.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly uses a primary-replica model. Replicas keep reconnecting if the link breaks and aim to stay an exact copy of the primary.

Run on the intended replica:

```bash
dragonfly> REPLICAOF hostname_or_IP port
```

Rules from the docs:

- If the server already replicates another primary, it stops, **discards its entire old dataset** and synchronises with the new one.
- If the primary needs a password, set the `masterauth` flag on the replica.
- At startup the `--replicaof` flag takes `<IPv4>:<PORT>`, `host:<PORT>` or `[<IPv6>]:<PORT>`.
- Redis OSS up to version 6.2 data structures and replication protocol are supported as a primary, so `REPLICAOF` can pull from Redis for migration.
- `--master_connect_timeout_ms` (default 20000) and `--master_reconnect_timeout_ms` (default 1000) govern connection attempts.
- `--replica_partial_sync` (default true) lets an interrupted replica reconnect with a partial sync.

Verify with `ROLE` or `INFO replication`.

## Checked

2026-11-04. Confirmed in the Replication page, the REPLICAOF page (`masterauth` flag) and the flags page (`replicaof` format, `masterauth`, `master_connect_timeout_ms` 20000, `master_reconnect_timeout_ms` 1000, `replica_partial_sync`). Nothing removed.

Method: documentation only; no commands were run.
