---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-running-exporters-and-default-labels
name: prometheus-operator-running-exporters-and-default-labels
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [exporters, kube-state-metrics, joblabel, default-labels, metric-relabeling, relabelings, basic-auth]
level: practitioner
status: docs-checked
description: "Run exporters behind a generic ServiceMonitor, know which labels ServiceMonitors and PodMonitors add, and apply relabeling and basicAuth."
sources:
  - https://prometheus-operator.dev/docs/user-guides/running-exporters/
  - https://prometheus-operator.dev/docs/user-guides/basic-auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scraping an exporter or metrics port needs a Service targeting its pods. Creation order of Service and ServiceMonitor does not matter.

## One ServiceMonitor for many Services
Aim for one generic ServiceMonitor covering many Services. Example: `selector.matchExpressions: [{key: k8s-app, operator: Exists}]`, `namespaceSelector.matchNames: [kube-system, monitoring]`, `jobLabel: k8s-app`, endpoint `port: http-metrics`, `interval: 15s`. The kube-state-metrics Service example carries `k8s-app: kube-state-metrics` and the annotation `alpha.monitoring.coreos.com/non-namespaced: "true"`.

## Default target labels
- ServiceMonitor: `instance`, `job` (the Service name, or `jobLabel`), `namespace`, `service`, `pod`, `container`, `endpoint`, and `node` or `pod`.
- PodMonitor: `job` is `{namespace}/{name}` of the PodMonitor (or `jobLabel`), plus `namespace`, `container`, `pod`, `endpoint`.

## Relabeling
`relabelings` run before the scrape on the target label set, in order of appearance; `metricRelabelings` run on samples as the last step before ingestion and do not apply to automatically generated series such as `up`. Examples: `action: labeldrop, regex: pod` removes the `pod` label; `action: replace, replacement: prometheus, targetLabel: team` sets a label; `keep` on `__meta_kubernetes_pod_label_team` with regex `prometheus` plus `drop` on `__meta_kubernetes_pod_label_datacenter` regex `west_europe` filters targets.

## Basic auth
In an endpoint use `basicAuth.username` and `basicAuth.password`, each a `{name, key}` reference to a Secret key (the guide's Secret holds `user` and `password` keys).

## Checked

2026-11-08. Read the running exporters page and the basic auth page in full. Examples, default label tables and relabeling snippets match. Added the in-order and up-series notes; removed an unsourced Secret namespace claim.

Method: documentation only; no commands were run.
