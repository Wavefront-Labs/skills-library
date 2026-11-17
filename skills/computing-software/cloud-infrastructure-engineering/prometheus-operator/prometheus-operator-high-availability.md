---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-high-availability
name: prometheus-operator-high-availability
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [high-availability, ha-pair, external-labels, replica-label, alertmanager-gossip]
level: practitioner
status: docs-checked
description: "Run Prometheus and Alertmanager highly available under the operator, including HA pairs, replica labels and alert delivery to all Alertmanagers."
sources:
  - https://prometheus-operator.dev/docs/platform/high-availability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Monitoring must be at least as available as what it monitors.

## Prometheus
Run two or more instances with identical configuration except for one external label whose value differs per instance. They scrape the same targets and evaluate the same rules, so they hold essentially the same data, with small differences because scrape times and external labels differ. Queries against each instance may return slightly different results; for dashboards the page suggests sticky sessions (`sessionAffinity` on the Service) or a Thanos Querier. Replicas protect against failure but do not scale out; for that use sharding. The page prefers functional sharding (each shard scrapes a distinct set of Services); automatic address-based sharding needs query federation such as Thanos Query and distributed rule evaluation such as Thanos Ruler. Automated sharding and federation were described as roadmap work.

## Alertmanager
Each Prometheus sends alerts to **all** configured Alertmanager instances. The Alertmanagers form a gossip cluster to replicate silences and the notification log, avoiding duplicates. The operator handles:
- Alertmanager discovery through the Kubernetes API for Prometheus;
- a highly available cluster whenever `replicas > 1`.

## Exporters
Depends on the exporter. kube-state-metrics is effectively stateless, so run several load-balanced replicas, as long as the backing service (the Kubernetes API) is available.

## Checked

2026-11-08. Read the high availability page in full. Removed the unsourced claim that the operator sets a prometheus_replica label and the Mimir deduplication section (not in the page); added the sticky-session, functional sharding and Thanos notes from the page.

Method: documentation only; no commands were run.
