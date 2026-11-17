---
id: computing-software.database-administration.patroni.patroni-convert-standalone-postgres
name: patroni-convert-standalone-postgres
category: computing-software
field: database-administration
product: patroni
tags: [patroni, migration, existing-data, replication-slots, systemd]
level: practitioner
status: docs-checked
description: "Steps to bring an existing PostgreSQL cluster under Patroni management with minimal downtime."
sources:
  - https://patroni.readthedocs.io/en/latest/existing_data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: adopt running nodes without rebuilding them.

Prerequisites: all nodes up, and no Postgres configuration changes during migration.

1. Create the Postgres users matching the authentication section: a superuser, a replication user (`WITH REPLICATION`), and, for `use_pg_rewind`, a rewind user granted EXECUTE on `pg_catalog.pg_ls_dir(text, boolean, boolean)`, `pg_stat_file(text, boolean)`, `pg_read_binary_file(text)` and `pg_read_binary_file(text, bigint, bigint, boolean)`.
2. On each node, primary first, completing all steps on one node before the next:
   - Disable the Postgres systemd unit, since Patroni starts and stops Postgres.
   - Create the Patroni YAML (the generation and validation tooling can help).
   - On the primary, if replication slots are used between members, enable `use_slots` and list existing slots as permanent via `slots`. Patroni drops slots it does not recognise when `use_slots` is on.
   - Start Patroni; it detects running Postgres and monitors it.
   - Hand over startup with `patronictl restart cluster-name member-name`: restart standbys immediately and schedule the primary in a maintenance window.
3. Remove the permanent slots from `slots` with `patronictl edit-config` once Patroni-created slots have `restart_lsn` >= the original slot's `restart_lsn` (compare in `pg_replication_slots`).

FAQ: if Patroni cannot bind to the PostgreSQL port, check `listen_addresses`/`port` in postgresql.conf against `postgresql.listen`, and pg_hba.conf access.

## Checked

2026-11-08. Confirmed every step against the Patroni "Convert a Standalone to a Patroni Cluster" page (read in full), including the rewind-user grants and the FAQ entry.

Method: documentation only; no commands were run.
