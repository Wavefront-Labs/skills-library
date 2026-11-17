---
id: computing-software.cloud-infrastructure-engineering.netdata.replication-settings
name: replication-settings
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, replication, replication-period, replication-threads]
level: advanced
status: docs-checked
description: "Tune replication of past samples between Netdata Children and Parents: replication period, threads, obsolete chart cleanup, limits and progress monitoring."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/replication-of-past-samples.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replication backfills gaps after reconnects by appending missing samples. Settings in `netdata.conf`:

Receiving Parent:
- `[db].replication period` (default 1 day): caps how far back replication can reach; the sender's stored tier0 data also limits it.

Sending Child or clustered Parent:
- `[db].replication threads` (default 1): more threads speed up Parent-to-Parent replication with lots of data; each handles about two million samples per second.
- `[db].cleanup obsolete charts after` (default 1 hour, 3600 seconds): how long stopped metrics stay available. Raise it if Parent maintenance may exceed an hour; this can raise RAM in environments with many short-lived metrics.

```
[db]
    replication period = <duration>
    replication threads = <n>
```

Limits:
- Only tier0 samples replicate; maximum depth is the sender's tier0 retention.
- Only active metrics replicate. Archived metrics (archived 1 hour after collection stops) replicate only once collected again, so data is lost only if a Child stays disconnected longer than an hour.

Monitor: the `Netdata-streaming` Function under the Live tab, or `http://agent-ip:19999/api/v2/node_instances` on both Parents and Children.

## Checked

2026-11-04. Confirmed against the Netdata Replication of Past Samples page: the three settings and defaults, the two-million-samples-per-thread figure, the append-only, tier0-only and active-only limits, the 1-hour archive note, and both monitoring routes. Removed the closing restart and edit-config line, which the page does not state.

Method: documentation only; no commands were run.
