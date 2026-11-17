---
id: computing-software.database-administration.patroni.patroni-postgresql-connection-settings
name: patroni-postgresql-connection-settings
category: computing-software
field: database-administration
product: patroni
tags: [patroni, postgresql, listen, connect-address, bin-dir]
level: practitioner
status: docs-checked
description: "Core postgresql section keys: listen, connect_address, data_dir, bin_dir, unix sockets, pgpass and pg_ctl_timeout."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set the local PostgreSQL parameters Patroni needs.

- `listen`: IP and port Postgres listens on, reachable by other nodes for streaming replication. Multiple comma-separated addresses allowed with the port after the last, for example `127.0.0.1,127.0.0.2:5432`; Patroni uses the first for local connections.
- `connect_address`: IP and port through which Postgres is reachable by other nodes and applications.
- `proxy_address`: address of a connection pool (for example pgbouncer) next to Postgres; written to the member key as `proxy_url` for service discovery.
- `data_dir`: existing or to-be-initialized data directory. `config_dir`: defaults to the data directory and must be writable by Patroni.
- `bin_dir`: path to binaries (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind); if empty, `PATH` is used. `bin_name` overrides individual binary names.
- `use_unix_socket` / `use_unix_socket_repl` (default false): prefer unix sockets for Patroni and replication connections, using the first suitable value of `unix_socket_directories`, falling back to TCP.
- `pgpass`: path of the .pgpass Patroni writes before pg_basebackup and the post_init script; must be writable.
- `pg_ctl_timeout`: how long pg_ctl waits on start, stop or restart; default 60 seconds.
- `use_pg_rewind`, `recovery_conf`, `custom_conf`, `parameters`, `pg_hba`, `pg_ident` as covered elsewhere.

Top-level: `name` (unique per cluster), `scope` (cluster name), `namespace` (default `/service`), `thread_pool_size` (default and minimum 5), `thread_stack_size` (default 512kB, minimum 64kB, aligned to 64kB).

## Checked

2026-11-03. Confirmed against YAML Configuration Settings (postgresql section and top-level settings): listen, connect_address, proxy_address, data_dir, config_dir, bin_dir, use_unix_socket, pgpass, pg_ctl_timeout, thread_pool_size and thread_stack_size values.

Method: documentation only; no commands were run.
