---
id: computing-software.database-administration.pgbackrest.timeouts-and-keepalive
name: timeouts-and-keepalive
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, db-timeout, protocol-timeout, io-timeout, tcp-keep-alive]
level: advanced
status: docs-checked
description: "How db-timeout, protocol-timeout and io-timeout relate, plus TCP keep-alive options."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune timeouts for slow checkpoints or networks.

- `db-timeout` (default 30m): seconds allowed for database queries, including the backup start and stop functions, which can each take a long time. Keep it high unless you know they return quickly, for example start-fast=y with little WAL generated during the backup.
- `protocol-timeout` (default 31m): how long a local or remote process waits for a new protocol message, preventing indefinite waits.
- `io-timeout` (default 1m, range 100ms to 1h): timeout for connections and reads/writes. The whole operation need not finish in that time, but some progress, even one byte, must be made.

`db-timeout` must be less than `protocol-timeout`; raise them together.

```
[global]
db-timeout=3600
protocol-timeout=3660
```

TCP keep-alive (where the OS supports the matching socket option):

- `tcp-keep-alive-count`: lost messages before the connection is dead (1 to 32).
- `tcp-keep-alive-idle`: idle seconds before a probe (1 to 3600).
- `tcp-keep-alive-interval`: seconds before retransmitting an unacknowledged probe (1 to 900).

`sck-keep-alive` (default y) enables keep-alive messages on socket connections, and `archive-timeout` (default 1m) separately bounds waiting for a WAL segment in check and backup.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Nothing needed removing. 

Method: documentation only; no commands were run.
