---
id: computing-software.database-administration.postgresql.predefined-roles-and-monitoring-access
name: predefined-roles-and-monitoring-access
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, database-roles, role-privileges, predefined-roles, pg-monitor-role, pg-read-all-data, pg-write-all-data, pg-signal-backend, least-privilege, monitoring-user]
level: practitioner
status: verified
description: "Grant PostgreSQL predefined roles (pg_monitor, pg_read_all_data, pg_signal_backend, pg_checkpoint and others) instead of superuser for monitoring, backup and ops tasks."
sources:
  - https://www.postgresql.org/docs/current/predefined-roles.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Predefined roles instead of superuser

**Goal:** monitoring agents, backup tools and on-call humans get exactly the
capability they need, and nothing runs as `postgres` except emergencies.

## The useful ones
| Role | Grants | Typical user |
|---|---|---|
| `pg_monitor` (= `pg_read_all_settings` + `pg_read_all_stats` + `pg_stat_scan_tables`) | See all rows in pg_stat_activity incl. query text, all settings, stats functions | Prometheus postgres_exporter, Datadog, pgwatch |
| `pg_read_all_data` (PG14) | SELECT on all tables/views/sequences, USAGE on all schemas | Reporting, logical pg_dump user |
| `pg_write_all_data` (PG14) | INSERT/UPDATE/DELETE everywhere | Data-fix tooling (rare) |
| `pg_signal_backend` | `pg_cancel_backend` / `pg_terminate_backend` on non-superuser sessions | On-call role |
| `pg_checkpoint` (PG15) | Run `CHECKPOINT` | Pre-restart scripts |
| `pg_maintain` (PG17) | VACUUM, ANALYZE, REINDEX, REFRESH MATVIEW, CLUSTER, LOCK on all relations | Maintenance jobs |
| `pg_read_server_files` / `pg_write_server_files` / `pg_execute_server_program` | COPY to/from server files or programs | Avoid: effectively superuser-equivalent |
| `pg_create_subscription` (PG16) | CREATE SUBSCRIPTION | Logical replication admin |
| `pg_use_reserved_connections` (PG16) | Use `reserved_connections` slots | Monitoring agent so it can still connect when full |

## Example: monitoring user
```sql
CREATE ROLE mon LOGIN CONNECTION LIMIT 5;
GRANT pg_monitor TO mon;
GRANT pg_use_reserved_connections TO mon;     -- with reserved_connections = 3
ALTER ROLE mon SET statement_timeout = '10s';
```

## Gotchas
- Without `pg_read_all_stats`, a non-superuser sees `<insufficient privilege>` in
  `pg_stat_activity.query` for other users' sessions: dashboards look empty (checked: a plain role's `LIKE` filter on `query` matched nothing, while a `pg_monitor` member saw the superuser's and another user's query text). The same hiding means a `pg_signal_backend` holder cannot find sessions by query text; look up pids as a monitoring role.
- `pg_read_all_data` acts as SELECT on everything but does not bypass row-level security (PG docs: predefined-roles); for full
  logical dumps of RLS tables also need BYPASSRLS.
- Backup tools that use the low-level API need `EXECUTE` on `pg_backup_start`/`pg_backup_stop` (a plain role gets `permission denied`; `GRANT EXECUTE ON FUNCTION pg_backup_start(text, boolean) TO role` worked); grant those individually, not superuser, and check your tool's docs for the rest (for example the REPLICATION attribute for `pg_basebackup`).
- `pg_execute_server_program` lets the holder run shell commands as postgres:
  treat as superuser.

## Verify
```sql
SELECT rolname FROM pg_roles WHERE pg_has_role('mon', oid, 'MEMBER');
```
Connect as `mon` and confirm `SELECT query FROM pg_stat_activity` shows other users' queries.

## Checked
PostgreSQL 17.6: `pg_roles` lists `pg_checkpoint`, `pg_create_subscription`, `pg_maintain`, `pg_monitor`, `pg_read_all_data`, `pg_read_all_settings`, `pg_read_all_stats`, `pg_signal_backend`, `pg_stat_scan_tables`, `pg_use_reserved_connections`, `pg_write_all_data`, `pg_read_server_files`, `pg_write_server_files`, `pg_execute_server_program` (plus `pg_database_owner`); granting `pg_monitor` shows membership in `pg_read_all_settings`, `pg_read_all_stats` and `pg_stat_scan_tables`; a `pg_signal_backend` member terminated another non-superuser's backend but got `Only roles with the SUPERUSER attribute may terminate processes of roles with the SUPERUSER attribute` for a superuser's; `pg_checkpoint` allowed `CHECKPOINT` (a plain role got `permission denied to execute CHECKPOINT command`); `pg_maintain` ran VACUUM, ANALYZE and REINDEX on a table it had no grants on (a plain role got `permission denied to vacuum`); `CONNECTION LIMIT 5` and `ALTER ROLE ... SET statement_timeout` work. Docs (predefined-roles) for the role descriptions; version tags confirmed in the release notes (14: pg_read_all_data/pg_write_all_data, 15: pg_checkpoint, 16: pg_create_subscription and pg_use_reserved_connections, 17: pg_maintain).
