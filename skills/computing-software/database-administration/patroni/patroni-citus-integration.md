---
id: computing-software.database-administration.patroni.patroni-citus-integration
name: patroni-citus-integration
category: computing-software
field: database-administration
product: patroni
tags: [patroni, citus, coordinator, workers, sharding]
level: sme
status: docs-checked
description: "Run Citus coordinator and worker groups under Patroni: requirements, citus section and automatic actions."
sources:
  - https://patroni.readthedocs.io/en/latest/citus.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: deploy a multi-node Citus cluster managed by Patroni.

Rules:
- The Citus extension must be on all nodes. The minimum supported version is 10.0; at least 11.2 is recommended for transparent switchovers and restarts of workers.
- The cluster name (`scope`) must be the same for all Citus nodes.
- Superuser credentials must be identical on coordinator and workers, with pg_hba.conf allowing superuser access between all nodes.
- Workers must be allowed REST API access to the coordinator (same credentials, client certificates accepted if configured).

```
citus:
  group: X      # 0 for coordinator, 1, 2, 3 for workers
  database: citus   # same on all nodes
```

Patroni then:
- sets `bootstrap.dcs.synchronous_mode` to `quorum` unless explicitly set otherwise;
- adds `citus` to `shared_preload_libraries`;
- sets `max_prepared_transactions` to `2*max_connections` if not set in the global dynamic configuration;
- adjusts the `citus.local_hostname` GUC from localhost to the address Patroni uses;
- creates the database and runs CREATE EXTENSION citus;
- adds superuser credentials to `pg_dist_authinfo` (update them if you change superuser credentials);
- lets the coordinator primary register worker primaries in `pg_dist_node` via `citus_add_node()` and maintain it on failover.

patronictl: `list` and `topology` show all groups with a Group column. Every command gains `--group`; `pause` defaults to the configured group, but `switchover` and `remove` need it explicitly.

## Checked

2026-11-03. Confirmed against the Citus page: version requirements, `citus.group` and `citus.database`, automatic settings Patroni applies, and the patronictl `--group` behaviour.

Method: documentation only; no commands were run.
