---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-storage-and-persistence
name: alertmanager-storage-and-persistence
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alertmanager-storage-path, alertmanager-persistence, nflog, silence-replication, alertmanager]
level: practitioner
status: verified
description: "What Alertmanager persists in storage.path (silences, notification log), data.retention, and how persistence and clustering interact on restarts."
sources: ["https://prometheus.io/docs/alerting/latest/alertmanager/", "https://github.com/prometheus/alertmanager#usage", "https://prometheus.io/docs/alerting/latest/alertmanager/#high-availability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alertmanager storage and persistence

`--storage.path` (default `data/`) holds two snapshot files:
- `silences`: all silences (active and expired until retention).
- `nflog`: notification log, records what was sent to which receiver for each group, used to avoid re-sending and to honour `repeat_interval`.
Active alerts themselves are **not** persisted (after a restart `amtool alert query` listed none); Prometheus re-sends firing alerts at least every `--rules.alert.resend-delay` (default 1m).
Snapshots are written every `--data.maintenance-interval` (default 15m) and on clean shutdown, so a hard kill can lose up to that interval of silence changes (a silence added just before a hard kill left an empty storage directory).

`--data.retention` (default 120h) controls how long expired silences and nflog entries are kept.

## What happens on restart
| Setup | Silences | Duplicate notifications |
|---|---|---|
| Single replica, persistent volume | kept | none expected |
| Single replica, emptyDir | **lost**: silenced alerts notify again | repeats sent once |
| Cluster of 3, emptyDir | restored from peers via gossip on join | usually none |
| Cluster of 3, PV | kept and gossiped | none |
For a single instance, a persistent volume is mandatory if you rely on silences.

## Backups
Silences can be exported: `amtool silence query -o json > silences.json` and re-imported with `amtool silence import < silences.json`. Useful before migrations.

## Gotchas
- Changing `storage.path` or wiping the volume during maintenance re-notifies every active group.
- Very long-lived silences (months) are a smell; they persist through restarts and hide real problems. Review expiring/long silences.

## Verify
- [ ] Restarting one replica keeps existing silences visible in `/api/v2/silences`.
