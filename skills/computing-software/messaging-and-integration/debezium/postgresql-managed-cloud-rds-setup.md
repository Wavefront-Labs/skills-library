---
id: computing-software.messaging-and-integration.debezium.postgresql-managed-cloud-rds-setup
name: postgresql-managed-cloud-rds-setup
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, amazon-rds, cloud, pgoutput]
level: practitioner
status: docs-checked
description: "Prepare Amazon RDS and other managed PostgreSQL services for Debezium by enabling logical replication and pgoutput."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Managed PostgreSQL services need extra steps because you cannot edit `postgresql.conf` directly. The guide covers Amazon RDS, Azure Database for PostgreSQL, Google Cloud SQL and CrunchyBridge.

For Amazon RDS:

1. Set the instance parameter `rds.logical_replication` to `1`.
2. As the RDS master user, run `SHOW wal_level;` and verify it returns `logical`.

You cannot set `wal_level` yourself; it changes automatically when `rds.logical_replication` is set. In multi-zone replication setups, verify it because it may not be applied.

Plug-in choice: environments such as Google Cloud SQL and RDS require `pgoutput`, and you must say so explicitly:

```json
"plugin.name": "pgoutput"
```

`pgoutput` ships with PostgreSQL, so nothing needs installing. Other plug-ins such as `decoderbufs` must be compiled and installed on the server.

Create the replication user with the cloud superuser group, for example `CREATE USER replication_user WITH REPLICATION IN ROLE cloudsqlsuperuser LOGIN PASSWORD 'secret';` on Cloud SQL.

Gotcha: RDS makes writes to its own system tables invisible to clients about every five minutes, so an idle database can still show WAL growth. Use heartbeats.

Check: start the connector and confirm the slot appears as active in `pg_replication_slots`.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: RDS rds.logical_replication and wal_level, pgoutput requirement on Cloud SQL and RDS, Cloud SQL replication user, RDS five-minute system table writes.
Removed or reworded: the claim that managed services do not allow compiling plug-ins.
Method: documentation only; no commands were run.
