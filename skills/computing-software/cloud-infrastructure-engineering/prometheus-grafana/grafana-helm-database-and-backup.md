---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-helm-database-and-backup
name: grafana-helm-database-and-backup
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, grafana-helm-chart, grafana-helm-values, grafana-database-config, postgres-backend, grafana-backup, grafana-migrate-db, grafana-self-metrics, monitoring-grafana, grafana-ha]
level: practitioner
status: docs-checked
description: "Configure Grafana's database (Postgres/MySQL vs SQLite), back it up, set up alerting HA peers, and expose Grafana's own metrics to Prometheus."
sources: ["https://github.com/grafana/helm-charts/tree/main/charts/grafana", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#database", "https://grafana.com/docs/grafana/latest/administration/back-up-grafana/", "https://grafana.com/docs/grafana/latest/setup-grafana/set-up-grafana-monitoring/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana database, backup and self-monitoring

## Helm chart
The `grafana/helm-charts` Grafana chart page states it has migrated to `grafana-community/helm-charts`, with updates
and support there after January 30th, 2026. Point your Helm repository configuration at the new location and read that
chart's README for current values; this skill does not list chart values.

## Database settings (`[database]` in grafana.ini)
```ini
[database]
type = postgres
host = grafana-db.internal:5432
name = grafana
user = grafana
ssl_mode = require
max_open_conn = 50
```
- `type` is `mysql`, `postgres` or `sqlite3`. The default is sqlite3, an embedded database; the docs caution it is not
  recommended for production, so use MySQL or PostgreSQL.
- `ssl_mode`: for Postgres any valid libpq sslmode (`disable`, `require`, `verify-full`...); for MySQL `true`, `false`
  or `skip-verify`.
- `max_open_conn` is the maximum open database connections (for MySQL set it on both Grafana and the database);
  `conn_max_lifetime` defaults to 14400 seconds.
- Alternatively use `url = type://user:password@host:port/name`. Passwords containing `#` or `;` need triple quotes.
- Any setting can be overridden with `GF_<SECTION NAME>_<KEY>` environment variables (for example
  `GF_SECURITY_ADMIN_USER`).
- `secret_key` (in `[security]`) signs data source secrets using AES-256 in CFB mode; it cannot be changed without
  updating data source settings to re-encode them. Keep it identical across instances and with your backups.

## Alerting HA
`[unified_alerting] ha_peers` is a comma-separated list of initial instances (`<HOST>:<PORT>`) forming the HA cluster;
setting it enables HA mode for alerting. `ha_listen_address` defaults to `0.0.0.0:9094` (TCP and UDP) and
`ha_peer_timeout` to 15s.

## Backup (Grafana "Back up Grafana")
- Configuration: copy `custom.ini`; with deb or rpm packages it is `/etc/grafana/grafana.ini`.
- Plugins: copy the plugin folders (`$WORKING_DIR/data/plugins`, or `/var/lib/grafana/plugins` for deb or rpm).
- SQLite: copy the database file (`$WORKING_DIR/data/grafana.db`, or `/var/lib/grafana/grafana.db` for deb or rpm)
  after shutting Grafana down to ensure integrity.
- MySQL: `mysqldump -u root -p[root_password] [grafana] > grafana_backup.sql`; restore with
  `mysql -u root -p grafana < grafana_backup.sql`.
- Postgres: `pg_dump grafana > grafana_backup`; restore with `psql grafana < grafana_backup`.

## Monitor Grafana
Enable internal metrics in the `[metrics]` section (`enabled = true`; optional `basic_auth_username` and
`basic_auth_password`) and restart. Metrics are at `/metrics` (and `/metrics/plugins/:pluginId`) and can be pulled by
Prometheus or pushed to Graphite. They cover active instances, dashboard, user and playlist counts, HTTP status codes,
requests by routing group, active alerts and performance. HTTP request metrics use native histograms, with classic
buckets also exposed by default; `classic_http_histogram_enabled = false` exposes only native histograms to reduce
cardinality.

## Verify
- [ ] Production Grafana uses Postgres or MySQL, not the default SQLite.
- [ ] A restore from the latest dump works with the same `secret_key` and data sources still connect.

## Checked
Checked 2026-11-08 against the Grafana configuration page ([database], secret_key, ha_peers, GF_ variables), the
"Back up Grafana" page and the "Set up Grafana monitoring" page, plus the Helm chart page (migration notice). Removed:
the Helm values block, the SQLite to Postgres migration advice and named converters, the specific metric names and
the sample histogram_quantile query, the "Grafana internals" dashboard mention and the two-replica verification
step, none of which the pages state.
Method: documentation only; no commands were run.
