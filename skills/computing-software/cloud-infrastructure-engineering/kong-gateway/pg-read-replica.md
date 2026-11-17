---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.pg-read-replica
name: pg-read-replica
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, pg-ro-host, read-replica, read-splitting, postgres, kong-conf]
level: advanced
status: docs-checked
description: "Send Kong's read-only queries to a PostgreSQL replica by setting pg_ro_host and pg_ro_* overrides, plus db_update_propagation for replication lag."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
  - https://developer.konghq.com/gateway/traditional-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL read-only replica

With PostgreSQL, Kong can send read-only queries to a separate replica to reduce load on the primary.

Setting `pg_ro_host` enables read splitting; when empty (the default) the feature is disabled.

Every other `pg_ro_*` option inherits the matching `pg_*` value unless overridden: port, timeout, user, password, database, schema, SSL, concurrency, pool and backlog. For example, if the replica listens on a different port, set `pg_ro_port`.

Replication lag matters because nodes poll the datastore. Set `db_update_propagation` (default `0`, seconds) to the maximum expected replication lag so changes are not read before they reach the replica.

Related polling settings:
- `db_update_frequency`: default `5` seconds
- `db_cache_ttl`: default `0` (no expiry)

## Checked

2026-11-04. Confirmed against kong.conf.default and the Traditional mode page: read-only connection purpose, `pg_ro_host` needed to enable, inheritance from the main `pg_*` values, `db_update_propagation` guidance and the three defaults. Nothing removed.
Method: documentation only; no commands were run.
