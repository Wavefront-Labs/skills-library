---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-rolling-updates
name: grafana-mimir-rolling-updates
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [rolling-update, upgrade, ingesters, store-gateway, alertmanager]
level: practitioner
status: docs-checked
description: "Gives Mimir rolling update rules per mode and component: monolithic one at a time, and limits for Alertmanagers, ingesters and store-gateways, with zone-aware shortcuts."
sources: ["https://grafana.com/docs/mimir/latest/manage/run-production-environment/perform-a-rolling-update/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rolling updates

A rolling update applies configuration changes or upgrades with no downtime.

## Monolithic mode

Update one instance at a time. When the restarted instance's `/ready` endpoint returns HTTP 200, proceed to the next. On Kubernetes set the Deployment or StatefulSet strategy to `RollingUpdate` with `maxUnavailable: 1`.

## Microservices mode

Stateless components can be updated many instances at once, and several components in parallel. Stateful ones are limited:

- **Alertmanagers**: at most two at a time. Alerts are in memory and each tenant's alerts replicate to three Alertmanagers by default; notification and viewing work while each tenant has one healthy Alertmanager in its shard.
- **Ingesters**: one at a time. Recent samples are in memory; this keeps at least one ingester per partition available (ingest storage) or a majority of ingesters (classic).
- **Store-gateways**: at most two at a time. Blocks are replicated to three by default, and queries succeed when each block is loaded by at least one.

With zone-aware replication enabled for a component, you can roll all instances in one zone at the same time.

## Checked

2026-11-04. Confirmed against the Mimir page "Perform a rolling update to Grafana Mimir": monolithic and microservices rules, per-component limits, zone-aware note. Removed the closing readiness tip for microservices mode (the page states the `/ready` check only for monolithic mode).
Method: documentation only; no commands were run.
