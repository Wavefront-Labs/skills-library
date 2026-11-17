---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.database-exporters-mysqld-postgres
name: database-exporters-mysqld-postgres
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, mysqld-exporter-setup, postgres-exporter-setup, mysql, postgresql, database-monitoring, least-privilege]
level: practitioner
status: gated
description: "Deploy mysqld_exporter and postgres_exporter with least-privilege users, choose collectors, monitor many instances via multi-target, and the key metrics to alert on."
sources: ["https://github.com/prometheus/mysqld_exporter", "https://github.com/prometheus-community/postgres_exporter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mysqld_exporter and postgres_exporter

## MySQL
```sql
CREATE USER 'exporter'@'%' IDENTIFIED BY '<pw>' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'%';
```
```ini
# .my.cnf
[client]
user=exporter
password=<pw>
```
```bash
mysqld_exporter --config.my-cnf=.my.cnf \
  --collect.info_schema.processlist --collect.perf_schema.eventsstatements --collect.engine_innodb_status
```
Key alerts: `mysql_up == 0`; `mysql_global_status_threads_connected / mysql_global_variables_max_connections > 0.8`;
`mysql_slave_status_seconds_behind_master > 60` (or `mysql_replica_*` on newer); `rate(mysql_global_status_slow_queries[5m])`. (gated: unconfirmed, source is paywalled or blocked) The exporter READMEs do not list metric names; confirm these names on your `/metrics` output before alerting.

## PostgreSQL
```sql
CREATE USER postgres_exporter WITH PASSWORD '<pw>';
GRANT pg_monitor TO postgres_exporter;      -- PG10+ built-in role: stats views without superuser
```
```bash
DATA_SOURCE_NAME="postgresql://postgres_exporter:<pw>@db:5432/postgres?sslmode=require" \
postgres_exporter --collector.stat_statements
```
Key alerts: `pg_up == 0`; replication lag `pg_replication_lag_seconds`; connections
`sum(pg_stat_activity_count) / pg_settings_max_connections > 0.8`; transaction ID wraparound
`pg_database_age` (approaching 2^31); deadlocks `rate(pg_stat_database_deadlocks[5m])`. (gated: unconfirmed, source is paywalled or blocked)
Custom SQL metrics: `--extend.query-path` is deprecated (as is `--auto-discover-databases`); prefer a separate `sql_exporter` for business queries.

## Many instances (multi-target)
Both exporters support `/probe?target=...` (postgres via `auth_modules` in config; mysqld via
`[client.<name>]` sections + `auth_module` param), so one exporter Deployment can serve many DBs, like blackbox.

## Gotchas
- Never use the root/superuser account; the exporter connection appears in processlists and audit logs.
- Cap exporter connections (MAX_USER_CONNECTIONS / `ALTER ROLE ... CONNECTION LIMIT 3`); a stuck DB plus
  frequent scrapes can exhaust connections.
- Managed DBs (RDS, Cloud SQL): some views/permissions are restricted; check collector errors
  (`mysql_exporter_collector_success`, `pg_exporter_last_scrape_error`).

## Verify
- [ ] `mysql_up`/`pg_up` = 1 and collector success metrics are 1.
- [ ] Replication-lag alert tested by pausing a replica.

## Checked

2026-11-02. Confirmed against the mysqld_exporter and postgres_exporter READMEs: the `CREATE USER ... WITH MAX_USER_CONNECTIONS 3` and `GRANT PROCESS, REPLICATION CLIENT, SELECT` statements; `--config.my-cnf`; the `info_schema.processlist`, `perf_schema.eventsstatements` and `engine_innodb_status` collectors; `pg_monitor` for PostgreSQL 10+; `DATA_SOURCE_NAME`; `--collector.stat_statements` (off by default); `--extend.query-path` and `--auto-discover-databases` both DEPRECATED; `auth_module` with `[client.<name>]` (mysqld) and `auth_modules` (postgres). Removed: the unsourced 'mysqld 0.15+' version and the deprecated `--auto-discover-databases=false` flag from the example. Gated: the specific alert metric names (`mysql_up`, `pg_up`, `pg_replication_lag_seconds`, `pg_database_age`, collector-success metrics), which the READMEs do not list.

Method: documentation only; no commands were run.
