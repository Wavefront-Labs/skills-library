---
id: computing-software.database-administration.postgresql.postgres-exporter-metrics-and-alerts
name: postgres-exporter-metrics-and-alerts
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-exporter, prometheus, grafana, alerting, monitoring, pg-monitor]
level: practitioner
status: docs-checked
description: "Deploy prometheus-community postgres_exporter with a least-privilege role, choose collectors, and write the core PostgreSQL alert rules."
sources:
  - https://github.com/prometheus-community/postgres_exporter/blob/master/README.md
  - https://www.postgresql.org/docs/current/predefined-roles.html
  - https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus postgres_exporter metrics and alerts

## Monitoring role
```sql
CREATE ROLE postgres_exporter LOGIN PASSWORD '<PASSWORD>' CONNECTION LIMIT 3;
GRANT pg_monitor TO postgres_exporter;       -- read all pg_stat_* incl. other users' queries
```
No superuser needed. Allow it in pg_hba.conf from the exporter host only.

## Run
```bash
DATA_SOURCE_NAME="postgresql://postgres_exporter:<PASSWORD>@db1:5432/postgres?sslmode=verify-full" \
  postgres_exporter --collector.stat_statements --collector.long_running_transactions --web.listen-address=:9187
```
- One exporter per instance (sidecar or same host) is simplest; the multi-target `/probe?target=` mode exists for fleets.
- Enable `stat_statements` only with `pg_stat_statements` installed, and watch cardinality (top N queries only).
- Custom queries via `--extend.query-path` are deprecated (README); prefer built-in collectors for what they cover.

## Core alert rules
Write Prometheus alerting rules (format: the Prometheus alerting-rules page) for: exporter or instance down, replication lag, connections near `max_connections`, transaction-ID wraparound risk, WAL archiver failures, and long-running transactions.
Metric names differ between exporter versions and collectors: read them from the exporter's `/metrics` output on your version before writing each rule expression.

## Dashboards
Start from a maintained Grafana dashboard for postgres_exporter and trim; key panels: connections by state, TPS (xact_commit rate), cache hit, replication lag, dead tuples, checkpoints, WAL rate, archive status.

## Verify
Fetch `http://localhost:9187/metrics` (default listen address `:9187`) and confirm the PostgreSQL up metric is 1 and the exporter reports no scrape error.

## Gotchas
- Scraping every 15s with heavy collectors on thousands of tables adds load; disable unneeded collectors (collectors take a `--[no-]collector.<name>` flag).
- Exporter connects to one database; per-database table stats need a target per database (`auto-discover-databases` is marked DEPRECATED in the README).
- Host metrics (disk, CPU) come from node_exporter, not this exporter; alert on pg_wal disk usage there.

## Checked
2026-11-01. Confirmed against the postgres_exporter README (DATA_SOURCE_NAME, `/probe?target=` multi-target mode, default listen `:9187`, `collector.stat_statements` and `collector.long_running_transactions` flags, `extend.query-path` and `auto-discover-databases` deprecated) and the PostgreSQL predefined-roles page (`pg_monitor`). Removed: the alert expressions with metric names, the scrape-error verify commands and the statement_timeout setting, which were not confirmable from those pages.
Method: documentation only; no commands were run.
