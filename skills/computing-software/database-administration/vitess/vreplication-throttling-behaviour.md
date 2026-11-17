---
id: computing-software.database-administration.vitess.vreplication-throttling-behaviour
name: vreplication-throttling-behaviour
category: computing-software
field: database-administration
product: vitess
tags: [vreplication, throttler, throttle-threshold, replication-lag, vstreamer, copy-phase]
level: practitioner
status: docs-checked
description: "How VReplication uses the tablet throttler on target and source, the default 1 second lag threshold, and why workflows may slow or stall under load."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/throttling/
  - https://vitess.io/docs/25.0/reference/vreplication/tablet_selection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VReplication copies large tables then applies the changelog, loading both sides: the source reads pages (contending for IO and polluting the buffer pool; a replica source may lag, a primary source may see write contention) and the target writes a lot (its replicas may lag). It therefore uses the tablet throttler to push back.

Target side: before writing to a shard's primary, VReplication consults the throttler, which checks MySQL replication lag on relevant replicas of that shard and any other configured metrics. Writes of both table-copy and changelog events are delayed until lag and other metrics are below their thresholds. The shard may be serving unrelated production traffic, which is why the whole shard's health is consulted.

Source side: VStreamer, the source endpoint, consults the throttler of the tablet it reads from, by default that tablet's replication lag. While any metric exceeds its threshold it reads neither table data nor changelog events. It affects only that one MySQL server.

Effect: production traffic is preferred, and VReplication may take longer or stall entirely under heavy load, resuming when load drops. The default threshold is 1 second of replication lag. On systems where replication lag is normally high, set `--throttle-threshold` to a value that fits your constraints so workflows can proceed.

If the throttler is enabled and you want RDONLY sources, see the tablet selection page note on `--throttle-tablet-types`.

## Checked

2026-11-08. Read in full: VReplication Throttling and Tablet Selection pages (vitess.io docs 25.0, via the website repo markdown). Confirmed: source and target load, target throttling, VStreamer source throttling, impact, --throttle-threshold and the default of 1 second of replication lag (Throttling page); the --throttle-tablet-types note for RDONLY sources (Tablet Selection page). Nothing removed.

Method: documentation only; no commands were run.
