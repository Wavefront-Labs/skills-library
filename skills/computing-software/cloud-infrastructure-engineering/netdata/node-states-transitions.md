---
id: computing-software.cloud-infrastructure-engineering.netdata.node-states-transitions
name: node-states-transitions
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, node-states, stale-node, tcp-keepalive]
level: advanced
status: docs-checked
description: "Read Netdata Cloud node states (Live, Stale, Offline, Unseen), failover behaviour, detection timings, TCP keepalive tuning and node cleanup rules."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-cloud/node-states-and-transitions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
States: Live (connected directly or via Parents), Stale (disconnected but a Cloud-connected Parent holds its history), Offline (disconnected, no data), Unseen (claimed, never connected). Parent dashboards show only Live and Stale.

Single Parent losing Cloud connection takes all its children Offline. HA pair (child, P1, P2): either Parent losing Cloud stays Live; P1 stopping gives brief Stale then Live via P2; both disconnecting gives Offline. A child also connected directly stays Live regardless.

Detection:
- Agent or Parent losing Cloud: about 60 s (MQTT keepalive); UI updates in 1-2 min.
- Child graceful shutdown: immediate. Crash or network drop: TCP keepalive idle plus probes. Silent child: `max(10 min, 2 x fastest chart cadence)`.
- Override idle with `tcp keepalive idle` in the receiving `[API_KEY]` or `[MACHINE_GUID]` section; `off`, `0` or `never` disables it. Up to three probes, 10 s apart.

Cloud cleanup (not configurable): standalone nodes 7 days, children 48 hours, Unseen 48 hours. Stale nodes are never removed automatically.

Gotchas:
- `streaming_disconnected` is an aggregate count and cannot name the node; find the time in the Events tab ("Node Became Offline").
- Stale nodes cannot be deleted in the UI; use `netdatacli remove-stale-node`.
- Node reappears after deletion: stop the Agent, remove `/var/lib/netdata/cloud.d/claimed_id`, clear related environment variables.

## Checked

2026-11-04. Confirmed against the Netdata Node States page: the four Cloud states, Parent view, HA failover table, single-Parent behaviour, detection timings including the max(10 minutes, 2 x fastest chart cadence) silent-child timeout, keepalive override and probes, cleanup windows, the streaming_disconnected note, remove-stale-node and the claimed_id steps. Nothing removed.

Method: documentation only; no commands were run.
