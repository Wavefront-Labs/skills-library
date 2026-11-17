---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-wal-replay-and-slow-startup
name: prometheus-wal-replay-and-slow-startup
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [wal-replay-time, slow-startup-prometheus, wal, memory-snapshot-on-shutdown, startup-probe, prometheus-troubleshooting]
level: practitioner
status: docs-checked
description: "Understand and shorten Prometheus startup: why the WAL is replayed, the memory-snapshot-on-shutdown feature flag, WAL compression and the Operator's startup probe limit."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/", "https://prometheus.io/docs/prometheus/latest/feature_flags/#memory-snapshot-on-shutdown", "https://prometheus-operator.dev/docs/api-reference/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAL replay and slow startup

The current block for incoming samples is kept in memory and is secured against crashes by the write-ahead log (WAL), which is replayed when the Prometheus server restarts. WAL files hold raw, not yet compacted data, so they are significantly larger than regular block files. They are stored in 128MB segments in the `wal` directory; at least three are kept, and high-traffic servers may keep more to hold at least two hours of raw data. The more data in the WAL, the longer the replay.

## Making it faster
- `--enable-feature=memory-snapshot-on-shutdown`: on shutdown, takes a snapshot of the in-memory chunks plus series information and stores it on disk. On startup the memory state is restored from that snapshot and the m-mapped chunks, and a WAL replay is needed only for the parts of the WAL not covered by the snapshot. It is taken at shutdown, so it helps planned restarts; the docs do not say it helps after a crash.
- `--storage.tsdb.wal-compression` (enabled by default since 2.20.0) can roughly halve WAL size depending on your data.
- Fewer series means less to replay; the storage docs say reducing the number of series is more effective than changing the scrape interval for cutting ingestion.
- If WAL files are corrupted so Prometheus will not start, the docs advise backing up the storage directory and restoring corrupted blocks from backups; without backups, the last resort is removing the corrupted block directories or WAL files, which loses the data they cover.

## Prometheus Operator startup probe
For the Prometheus custom resource, `spec.maximumStartupDurationSeconds` is the maximum time the prometheus container's startup probe waits before being considered failed. The startup probe succeeds once WAL replay is complete. If set, the value should be greater than 60 seconds; otherwise it equals 900 seconds (15 minutes). Raise it when replay on your largest instance takes longer than that, so Kubernetes does not kill it mid-replay.

## Checked
Date: 2026-11-07.
Read in full: the Storage page (on-disk layout and WAL paragraph, WAL compression flag, corruption recovery) and the Feature flags page (Memory snapshot on shutdown section; the whole page was read). The Prometheus Operator API reference is about 650k characters, so it was not read in full: `maximumStartupDurationSeconds` was found by searching it and its field description (greater than 60, otherwise 900 seconds, startup probe returns success after WAL replay) was read.
Removed because no cited page confirms them: the replay log lines, `prometheus_tsdb_data_replay_duration_seconds`, the `/-/ready` 503 behaviour, the Operator's 600s `terminationGracePeriodSeconds`, the hand-written Kubernetes startupProbe YAML, the claims about scrapes, rules and remote write during replay, and the invented Verify checklist.
Method: documentation only; no commands were run.
