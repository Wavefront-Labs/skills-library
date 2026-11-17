---
id: computing-software.database-administration.vitess.vitess-tablet-throttler-metrics-and-scopes
name: vitess-tablet-throttler-metrics-and-scopes
category: computing-software
field: database-administration
product: vitess
tags: [throttler, tablet-throttler, replication-lag, thresholds, metrics, vreplication, checkthrottler]
level: advanced
status: docs-checked
description: "Understand the Vitess tablet throttler: why it exists, supported metrics and default thresholds, self versus shard scope, app names, and running a check with CheckThrottler."
sources:
  - https://vitess.io/docs/25.0/reference/features/tablet-throttler/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VTTablet runs a throttler that watches tablet and shard load and pushes back background work (VReplication, Online DDL, table lifecycle) so mass reads and writes do not cause replication lag, query contention or OS load. Lagging replicas give stale reads and slow failovers.

Configuration lives in the Keyspace record in topo, so all tablets of a keyspace share it. The primary polls replicas; participation is limited by the `--throttle-tablet-types` vttablet flag, which defaults to replica only. Warning from the page: if you enable the throttler and use RDONLY tablets as a VReplication or VStream source, use `--throttle-tablet-types "replica,rdonly"`.

Metrics (v21 and later monitor several at once; v20 used one): `lag` (seconds), `loadavg` (per core), `threads_running`, `custom` (user query), `mysqld-loadavg`, `mysqld-datadir-used-ratio` (0.0 to 1.0) and `history_list_length`. Factory thresholds: 5 for lag, 1.0 for loadavg, 100 for threads_running, 1.0 for mysqld-loadavg, 0.98 for datadir ratio, 1000000000 for history_list_length. A value at or above its threshold is bad; threshold 0 means undefined.

Scopes: `self` (the tablet and its MySQL) and `shard` (primary only; the worst value across participating tablets including itself). `lag` defaults to shard scope; other metrics default to self.

Apps identify themselves by name: `vreplication`, `tablegc`, `online-ddl`, `vplayer`, `schema-tracker`; special names `vitess`, `always-throttled-app`, `test`, `all`. Colon-separated names combine apps. Run a check:
```shell
vtctldclient --server localhost:15999 CheckThrottler --app-name "vreplication" zone1-0000000101
```
The response carries a response code, per-metric value, threshold and scope, and a summary such as `vreplication is granted access`.

## Checked

2026-11-04. Purpose, collaboration and tablet types, metrics, defaults, scopes, apps and the CheckThrottler example confirmed on the Tablet Throttler page up to the Checks section; app rules and configuration commands were not read.

Method: documentation only; no commands were run.
