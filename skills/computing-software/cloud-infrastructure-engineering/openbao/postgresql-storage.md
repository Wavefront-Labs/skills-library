---
id: computing-software.cloud-infrastructure-engineering.openbao.postgresql-storage
name: postgresql-storage
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, postgresql, storage, ha-enabled, connection-url]
level: practitioner
status: docs-checked
description: "Run OpenBao on PostgreSQL storage: connection_url, tables, ha_enabled, skip_create_table, SSL defaults and standby read scaling."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/storage/postgresql.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# storage "postgresql"

```hcl
storage "postgresql" {
  connection_url = "postgres://user:pass@localhost:5432/database?sslmode=verify-full"
}
```

## Parameters

- `connection_url` (env `BAO_PG_CONNECTION_URL`)
- `table` default `openbao_kv_store`
- `max_parallel` `"128"`; `max_idle_connections`
- `ha_enabled` off by default (needs PostgreSQL 9.5+); `ha_table` default `openbao_ha_locks`
- `skip_create_table` false: set true if the DB user cannot create tables, or OpenBao fails to start
- `max_connect_retries` 1, exponential backoff 15ms to 5s; 0 means unlimited

## Schemas

KV table: `parent_path`, `path`, `key`, `value` (BYTEA), primary key (`path`, `key`), index on `parent_path`, C collation text. HA table: `ha_key` (primary key), `ha_identity`, `ha_value`, `valid_until`.

## Gotchas

- SSL is attempted by default; `sslmode=disable` is not recommended. Prefer `verify-full`.
- Horizontal read scalability (since v2.7.0) needs a cluster gRPC connection: `cluster_address` in a `listener` block and `cluster_addr` in config. Standbys log gRPC streaming of invalidations when it works.
- Horizontal read scalability needs physical replication; with logical replication you must set `disable_standby_reads` because LSN index values differ.
- Legacy upsert was dropped in v2.4.0.

## Checked

2026-11-04. Read the OpenBao PostgreSQL storage backend page in full. Confirmed: parameter names and defaults, `BAO_PG_CONNECTION_URL`, both table schemas, SSL default and `sslmode` examples, horizontal scalability requirements and log messages, the `disable_standby_reads` note, PostgreSQL 9.5 minimum and the v2.4.0 and v2.7.0 version notes. Removed: nothing.
Method: documentation only; no commands were run.
