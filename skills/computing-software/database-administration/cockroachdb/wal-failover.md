---
id: computing-software.database-administration.cockroachdb.wal-failover
name: wal-failover
category: computing-software
field: database-administration
product: cockroachdb
tags: [wal-failover, disk-stall, pebble, storage, cockroach-start]
level: advanced
status: docs-checked
description: "Configure WAL failover on CockroachDB nodes: among-stores or side-disk flag, required environment variables, log config, thresholds and disabling."
sources:
  - https://www.cockroachlabs.com/docs/stable/wal-failover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: limit the write-latency impact of transient disk stalls (common in cloud, lasting seconds) by failing WAL writes over to a second disk, bounding impact to a few hundred milliseconds (the configurable unhealthy-op threshold).

Enable at start:
- Multi-store node: `cockroach start --wal-failover=among-stores ...` or env `COCKROACH_WAL_FAILOVER=among-stores`.
- Single store with a side disk: `--wal-failover=path=<side-disk-path>` (or the `COCKROACH_WAL_FAILOVER=path=...` environment variable).

Required companions from the page's examples:
- Set `COCKROACH_ENGINE_MAX_SYNC_DURATION_DEFAULT=40s` (default fatal-stall detection is 20s; WAL failover needs headroom) and `COCKROACH_LOG_MAX_SYNC_DURATION=40s`.
- If you log to a file-based sink, supply a log config file (`--log-config-file logs.yaml`) that enables asynchronous buffering of `file-groups` sinks (or use remote sinks); otherwise log writes to the stalled disk can block the node and negate the benefit.
- Runtime equivalent of the engine variable: cluster setting `storage.max_sync_duration`; the page recommends `40s` when WAL failover is enabled and no change otherwise.

Threshold: `storage.wal_failover.unhealthy_op_threshold` must be lower than `storage.max_sync_duration`; the page recommends `100ms`.

Disable: `--wal-failover=disabled` (multi-store) or `--wal-failover=disabled,prev_path=<failover-disk>` (single store). On a running cluster, set `storage.wal_failover.unhealthy_op_threshold` to a duration greater than `storage.max_sync_duration`.

Test by inducing a transient disk stall shorter than the max sync duration, as the page's testing section does.

## Checked

2026-11-03. Confirmed against the WAL failover page: `--wal-failover` forms, `COCKROACH_WAL_FAILOVER`, `COCKROACH_ENGINE_MAX_SYNC_DURATION_DEFAULT` and `COCKROACH_LOG_MAX_SYNC_DURATION` at `40s` (default `20s`), log buffering, `storage.max_sync_duration`, `storage.wal_failover.unhealthy_op_threshold`, disabling. Removed: unsupported metric-increment verification.
Method: documentation only; no commands were run.
