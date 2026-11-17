---
id: computing-software.messaging-and-integration.temporal.production-checklist-self-hosted
name: production-checklist-self-hosted
category: computing-software
field: messaging-and-integration
product: temporal
tags: [production-checklist, self-hosted, history-shards, omes, load-testing, service-metrics, persistence-metrics, control-plane]
level: advanced
status: docs-checked
description: "Self-hosting Temporal checklist: shard count fixed at build, metric categories, 99.99 percent availability testing, control plane, sequential upgrades, load testing with Omes."
sources:
  - https://docs.temporal.io/self-hosted-guide/production-checklist
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Self-hosting means owning scalability, global hosting, uptime, a management plane, low latency, security, upgrades, support and cost.

Scaling: size well above average throughput because spikes are sustained. Throughput is often capped by the History Shard count (the unit that scales concurrent Workflow Execution throughput), set at build time. Adding Shards requires a rebuild and a migration to a new Temporal Service, so run proof-of-concept load tests (the Omes benchmarking tool, Temporal's published stress-test approach, or your own).

Track three metric categories:
- Service metrics: `service_requests`, `service_errors`, `service_latency`, tagged `type`, `operation`, `namespace`.
- Persistence metrics: `persistence_requests`, `persistence_errors`, `persistence_latency`, tagged by `operation`; the best signal for database trouble.
- Workflow Execution stats: counters `workflow_success`, `workflow_failed`, `workflow_timeout`, `workflow_terminate`, `workflow_cancel`, tagged `namespace`.

Availability: mission-critical deployments target 99.99 percent; test it during load testing and during server upgrades. Multi-Cluster Replication provides high availability and regional coverage. Deploy per region for data residency, latency or isolation.

Control plane: Temporal ships none as open source. Self-hosted has no RBAC or audit logging out of the box, so build these into your own control plane when running many Services.

Upgrades: releases come as often as every two weeks; upgrade sequentially without skipping minor versions (patches may be skipped), and load-test the upgrade.

Cost: following the guidance can oversize installs; performance testing right-sizes them, and trained administrators are a real cost.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: self-hosted-guide/production-checklist (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
