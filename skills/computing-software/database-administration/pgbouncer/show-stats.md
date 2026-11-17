---
id: computing-software.database-administration.pgbouncer.show-stats
name: show-stats
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, show-stats, metrics, wait-time, monitoring]
level: practitioner
status: docs-checked
description: "SHOW STATS, STATS_TOTALS, STATS_AVERAGES and TOTALS: counters since start, averages per stats_period, and their units."
sources:
  - https://www.pgbouncer.org/usage.html
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand the traffic statistics PgBouncer reports.

`SHOW STATS;` is per database. Totals are since process start; averages are updated every `stats_period` (default 60 seconds).

Totals: `total_xact_count` (SQL transactions pooled), `total_query_count` (SQL commands pooled), `total_server_assignment_count` (times a server was assigned to a client), `total_received` and `total_sent` (network bytes), `total_xact_time` (microseconds connected to PostgreSQL in a transaction, idle or executing), `total_query_time` (microseconds actively executing), `total_wait_time` (microseconds clients waited for a server, updated when a backend is assigned), `total_client_login_count`, and the prepared-statement counters `total_client_parse_count`, `total_server_parse_count`, `total_bind_count` (only with max_prepared_statements).

Averages: `avg_xact_count` and `avg_query_count` per second, `avg_server_assignment_count` per second, `avg_recv` and `avg_sent` bytes per second, `avg_xact_time` and `avg_query_time` in microseconds, `avg_wait_time` (average wait of clients assigned a backend during the current stats_period), `avg_client_login_count` per second, plus avg_client_parse_count, avg_server_parse_count, avg_bind_count.

Related views: `SHOW STATS_TOTALS` (only total_ columns), `SHOW STATS_AVERAGES` (only avg_ columns), `SHOW TOTALS` (like SHOW STATS aggregated across all databases).

If pool_idle_timeout or autodb_idle_timeout frees pools, per-database totals can decrease.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
