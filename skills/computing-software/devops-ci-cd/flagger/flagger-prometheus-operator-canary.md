---
id: computing-software.devops-ci-cd.flagger.flagger-prometheus-operator-canary
name: flagger-prometheus-operator-canary
category: computing-software
field: devops-ci-cd
product: flagger
tags: [prometheus-operator, servicemonitor, metrics-server, kubernetes-provider]
level: advanced
status: docs-checked
description: "Use Prometheus Operator ServiceMonitors as the metrics source for Flagger canary analysis."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/tutorials/prometheus-operator.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: Kubernetes v1.16+ and Prometheus Operator v0.40+. Install kube-prometheus-stack with `prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false` so the operator watches ServiceMonitors outside its own namespace, and `fullnameOverride=prometheus`.

Install Flagger pointed at it with the Kubernetes provider:

```bash
helm upgrade -i flagger flagger/flagger \
  --namespace flagger-system \
  --set metricsServer=http://prometheus-prometheus.monitoring:9090 \
  --set meshProvider=kubernetes
helm upgrade -i loadtester flagger/loadtester --namespace flagger-system
```

The demo app (podinfo) is instrumented with Prometheus, so create `ServiceMonitor` objects in the `test` namespace that scrape its `/metrics` endpoint for both the primary and canary services. Flagger metric templates then query those series instead of mesh telemetry.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/tutorials/prometheus-operator.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
