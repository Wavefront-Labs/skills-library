---
id: computing-software.cloud-infrastructure-engineering.metallb.prometheus-scraping
name: prometheus-scraping
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, prometheus, servicemonitor, prometheus-operator, podmonitor, kustomize, helm, rbac]
level: practitioner
status: docs-checked
description: "Scrape MetalLB with the Prometheus Operator: pick the overlay for your mode, Helm prometheus values, the monitoring-namespace assumption and ServiceMonitor selection."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/prometheus-metrics/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scraping MetalLB with Prometheus

MetalLB does not bundle a Prometheus stack; you wire yours to scrape it.

Manifests: overlays under `config/prometheus-native`, `config/prometheus-frr`, `config/prometheus-frr-k8s` define `ServiceMonitor` objects plus metrics Services for controller and speaker. Combined install manifests exist in `config/manifests/` (for example `metallb-native-prometheus.yaml`). Apply the one matching your mode.

Steps:
1. Apply the overlay for your mode.
2. Make sure your Prometheus instance selects the MetalLB `ServiceMonitor` labels.
3. Make sure RBAC lets it read endpoints in the MetalLB namespace.

Helm: enable scraping under the chart's `prometheus` values (ServiceMonitor or PodMonitor, scrape annotations, etc.); see the chart README.

Caveat: the all-in-one prometheus manifests assume the Prometheus operator in the `monitoring` namespace using the `prometheus-k8s` ServiceAccount (the kube-prometheus layout); they are mostly used by CI and may not suit your deployment. Prefer the chart or Kustomize when you need changes.

Alerts are not in the manifests: `computing-software.cloud-infrastructure-engineering.metallb.alert-rules`. Metric names: `computing-software.cloud-infrastructure-engineering.metallb.metrics-reference`.

## Checked

2026-11-04. Confirmed against the MetalLB Prometheus Metrics page (operator overlays, ServiceMonitor selection and RBAC, Helm prometheus values) and the Installation page (prometheus all-in-one manifests assume the monitoring namespace and prometheus-k8s service account, used mainly by CI, use charts or kustomize to change them, no alert rules in manifests). Removed the unsupported Verify line.

Method: documentation only; no commands were run.
