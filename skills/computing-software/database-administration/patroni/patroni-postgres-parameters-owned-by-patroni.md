---
id: computing-software.database-administration.patroni.patroni-postgres-parameters-owned-by-patroni
name: patroni-postgres-parameters-owned-by-patroni
category: computing-software
field: database-administration
product: patroni
tags: [patroni, postgres-parameters, max-connections, wal-level, dynamic-config]
level: advanced
status: docs-checked
description: "Which PostgreSQL GUCs Patroni forces through the DCS, with documented defaults and minimums."
sources:
  - https://patroni.readthedocs.io/en/latest/patroni_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know which parameters cannot be set locally.

Parameters that must hold the same value on the primary and replicas can be changed only through the shared DCS configuration; local files or environment values take no effect. Defaults and minimums:

- `max_connections`: default 100, minimum 25
- `max_locks_per_transaction`: default 64, minimum 32
- `max_worker_processes`: default 8, minimum 2
- `max_prepared_transactions`: default 0, minimum 0
- `wal_level`: default `hot_standby`; accepted `hot_standby`, `replica`, `logical`
- `track_commit_timestamp`: default off

Restricted to dynamic configuration because a replica may become primary:
- `max_wal_senders`: default 10, minimum 3
- `max_replication_slots`: default 10, minimum 4
- `wal_keep_segments`: default 8, minimum 1
- `wal_keep_size`: default 128MB, minimum 16MB
- `wal_log_hints`: on

Also controlled: `listen_addresses` and `port` (from `postgresql.listen`), `cluster_name` (from `scope`), and `hot_standby: on`.

These values are written into postgresql.conf and passed as command-line arguments to postgres, giving them the highest precedence (except `wal_keep_segments` and `wal_keep_size`), even above ALTER SYSTEM. Values are validated to be sane or meet a minimum. Set them with `patronictl edit-config --pg max_connections="150"`.

## Checked

2026-11-03. Confirmed against Patroni Dynamic Configuration / patroni_configuration: the list of parameters controlled by Patroni with their defaults and minimums, the precedence over ALTER SYSTEM, and the `patronictl edit-config --pg max_connections="150"` form (patronictl page example).

Method: documentation only; no commands were run.
