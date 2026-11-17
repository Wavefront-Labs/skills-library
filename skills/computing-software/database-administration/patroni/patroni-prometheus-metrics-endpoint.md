---
id: computing-software.database-administration.patroni.patroni-prometheus-metrics-endpoint
name: patroni-prometheus-metrics-endpoint
category: computing-software
field: database-administration
product: patroni
tags: [patroni, monitoring, prometheus, metrics, rest-api]
level: practitioner
status: docs-checked
description: "Scrape GET /metrics and use /patroni for monitoring, including the key gauges and state values."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: monitor role, replication and DCS health.

`GET /metrics` returns Prometheus format; `GET /patroni` returns a JSON document with similar information (the same structure as the health check responses) and is also used in the leader race.

Selected metrics, all labeled `scope` and `name`:
- `patroni_primary`, `patroni_replica`, `patroni_standby_leader`, `patroni_sync_standby`, `patroni_quorum_standby`: 1 if the node has that role.
- `patroni_postgres_running`, `patroni_postgres_streaming`, `patroni_postgres_in_archive_recovery`, `patroni_postgres_server_version` (for example 160004).
- `patroni_xlog_location` (0 if not the leader), `patroni_xlog_received_location`, `patroni_xlog_replayed_location`, `patroni_xlog_replayed_timestamp`, `patroni_xlog_paused`.
- `patroni_cluster_unlocked` (1 if no leader lock), `patroni_failsafe_mode_is_active`, `patroni_is_paused`, `patroni_pending_restart`.
- `patroni_postgres_timeline` (a gauge since 4.1.4, since it can reset to 0), `patroni_dcs_last_seen` (epoch of last successful DCS contact), `patroni_postmaster_start_time`.
- `patroni_postgres_state`: 0 initdb, 1 initdb_failed, 2 custom_bootstrap, 3 custom_bootstrap_failed, 4 creating_replica, 5 running, 6 starting, 7 bootstrap_starting, 8 start_failed, 9 restarting, 10 restart_failed, 11 stopping, 12 stopped, 13 stop_failed, 14 crashed (added in 4.1.0).

Example scrape: `curl http://localhost:8008/metrics`. Every metric carries `HELP` and `TYPE` lines; for instance `patroni_version` is the semver without periods (040000 for 4.0.0) and `patroni_xlog_location` is 0 on a node that is not the leader.

## Checked

2026-11-03. Confirmed against the REST API page: `/metrics` and `/patroni` output, metric names, and the `patroni_postgres_state` value mapping; 4.1.0 and 4.1.4 notes against the release notes.

Method: documentation only; no commands were run.
