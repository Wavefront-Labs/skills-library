---
id: computing-software.cloud-infrastructure-engineering.netdata.parent-cpu-sizing
name: parent-cpu-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, cpu-requirements, parent-sizing, ml-training]
level: advanced
status: docs-checked
description: "Estimate Netdata Parent CPU from ingest, re-streaming and machine learning per million metrics, keep total under 60 percent, and expect a startup spike."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/sizing-netdata-agents/cpu-requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Children on defaults (three tiers, ML, per-second collection, alerts, streaming): typically 1% to 5% of a single core.

Parent estimates per million:
- Metrics ingest: 2 cores per million samples received per second.
- Re-streaming: 2 cores per million samples resent per second.
- Machine learning: 2 cores per million unique series collected concurrently.

The docs give no explicit formula beyond these figures, so add the drivers that apply to your Parent.

Guidance: keep total CPU utilisation below 60% while the Parent processes metrics, trains models and runs health checks.

Startup: initialisation (backfilling higher tiers, metadata sync, replication, ML and health setup) temporarily raises CPU, network and disk I/O. The impact typically diminishes as the Parent stabilizes and enters steady state.

Lever if CPU is too high on Children: run ML on Parents and turn it off on Children (see optimize-agent-performance).

## Checked

2026-11-04: Child CPU range and its components, the per-million figures for ingest, re-streaming and ML, the 60 percent guidance and the startup tasks confirmed against the Netdata CPU Utilization page. Removed unsourced levers and a verify line.

Method: documentation only; no commands were run.
