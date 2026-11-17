---
id: computing-software.database-administration.cloudnative-pg.postgresql-conf-operator-managed-parameters
name: postgresql-conf-operator-managed-parameters
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [postgresql-conf, parameters, custom-conf, fixed-parameters, webhook, guc]
level: practitioner
status: docs-checked
description: "How CloudNativePG builds custom.conf from defaults, version defaults, your parameters and fixed parameters, which GUCs are forbidden, and why parameter values must be strings."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/postgresql_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You cannot edit `postgresql.conf`, `pg_hba.conf` or `pg_ident.conf` directly; configuration lives in the `postgresql` section of the `Cluster` and is identical on all instances. The pod starts with a default `postgresql.conf` that adds `listen_addresses = '*'` and `include custom.conf`. Your settings go in `custom.conf`:

```yaml
  postgresql:
    parameters:
      shared_buffers: "1GB"
```

Values must be strings. The operator generates `custom.conf` by applying, in order: global defaults, defaults depending on the PostgreSQL major version, user parameters, then **fixed** parameters. Because fixed ones come last they cannot be overridden.

Notable global defaults include `archive_timeout = '5min'`, `dynamic_shared_memory_type = 'posix'`, `logging_collector = 'on'`, `log_destination = 'csvlog'`, `max_parallel_workers`, `max_replication_slots` and `max_worker_processes` all `'32'`, TLS pinned to `TLSv1.3` min and max, `wal_keep_size = '512MB'`, `wal_level = 'logical'`, `wal_log_hints = 'on'` and `wal_sender_timeout`/`wal_receiver_timeout` of `5s`.

Fixed and exclusively controlled by the operator include `archive_command = '/controller/manager wal-archive %p'`, `hot_standby`, `port = '5432'`, `restart_after_crash = 'false'`, `ssl` and the `ssl_*_file` paths under `/controller/certificates`, and `unix_socket_directories`. A webhook rejects a long list of others, among them `archive_mode`, `data_directory`, `primary_conninfo`, `restore_command`, every `recovery_target*`, `synchronous_standby_names`, `shared_preload_libraries` (use the dedicated field) and the logging file settings.

## Checked

2026-11-04. Layering order, global defaults, fixed parameter list and string-only rule confirmed on the PostgreSQL Configuration page.

Method: documentation only; no commands were run.
