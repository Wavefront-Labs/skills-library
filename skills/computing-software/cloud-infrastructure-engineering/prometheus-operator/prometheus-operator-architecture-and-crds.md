---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-architecture-and-crds
name: prometheus-operator-architecture-and-crds
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [prometheus-operator, crds, servicemonitor, podmonitor, probe, prometheusrule, alertmanagerconfig, thanosruler, architecture]
level: intro
status: docs-checked
description: "Explain the ten Prometheus Operator custom resources: which deploy instances, which configure scraping or alerting, and what each reconciles to."
sources:
  - https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/getting-started/design.md
  - https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/getting-started/introduction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prometheus Operator is a Kubernetes operator that deploys and manages Prometheus and related components from custom resources. It ships ten CRDs, split into two groups.

## Instance-based resources (deploy and lifecycle)
- `Prometheus`: sets up a Prometheus server. The operator creates one `StatefulSet` per shard (default 1) in the same namespace. Replicas, persistent storage and Alertmanager targets are set here.
- `Alertmanager`: one `StatefulSet` per resource; with several replicas the instances run in high availability mode.
- `ThanosRuler`: evaluates recording and alerting rules across Prometheus instances. It needs at least one query endpoint (a Thanos Querier or Prometheus).
- `PrometheusAgent`: like `Prometheus` but without alerting, rule selectors, remote-read, storage or Thanos sidecar options.

## Config-based resources (what to scrape and alert on)
- `ServiceMonitor`: selects Services (via their `EndpointSlice` or `Endpoints`) and configures Prometheus to scrape the pods behind them.
- `PodMonitor`: selects pods directly by label.
- `Probe`: monitors ingresses and static targets through a prober, typically the blackbox exporter.
- `ScrapeConfig`: scrapes targets outside the cluster or setups the higher-level monitors cannot express.
- `AlertmanagerConfig`: sub-sections of Alertmanager configuration (routes, receivers, inhibition rules).
- `PrometheusRule`: alerting and recording rules, reconciled and loaded without restarting Prometheus or Thanos Ruler.

## Why it matters
Instead of writing Prometheus relabeling by hand, you use Kubernetes label selectors; the operator also validates `AlertmanagerConfig` and `PrometheusRule` objects. Sharding, `ThanosRuler` and the Thanos sidecar cover scaling and long-term storage.

## Checked

2026-11-08. Read the design and introduction pages in full. Resource list, StatefulSet behaviour, ThanosRuler query endpoint, PrometheusAgent removed options and PrometheusRule dynamic loading all match; no changes needed.

Method: documentation only; no commands were run.
