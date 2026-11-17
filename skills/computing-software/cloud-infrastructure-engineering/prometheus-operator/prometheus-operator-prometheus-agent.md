---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-prometheus-agent
name: prometheus-operator-prometheus-agent
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [prometheusagent, agent-mode, remote-write, daemonset-mode, agent-rbac]
level: advanced
status: docs-checked
description: "Deploy PrometheusAgent for scrape-and-forward setups with remote storage, with the RBAC it needs and the settings it does not support."
sources:
  - https://prometheus-operator.dev/docs/platform/prometheus-agent/
  - https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/Documentation/getting-started/design.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prometheus Agent (operator v0.64.0 and later) is a deployment model for environments where all data is forwarded to long-term storage (Cortex, Thanos, another Prometheus), so no local storage or rule evaluation is needed.

## Prerequisites
The `PrometheusAgent` CRD must be installed and the operator RBAC must include `prometheusagents`, `prometheusagents/finalizers` and `prometheusagents/status`.

## Agent identity
It needs its own ServiceAccount, ClusterRole and ClusterRoleBinding to discover and scrape targets: `get`/`list`/`watch` on `services`, `endpoints`, `pods` and `ingresses`, `get` on `configmaps`, and `get` on `/metrics`.

## Deploy
```yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: PrometheusAgent
metadata:
  name: prometheus-agent
spec:
  replicas: 2
  serviceAccountName: prometheus-agent
  serviceMonitorSelector:
    matchLabels:
      team: frontend
```
The `spec` is very similar to `Prometheus`, but features not applicable to agent mode (alerting, retention, Thanos and similar) are not available; the design page also lists PrometheusRule selectors, remote-read and storage as removed. `PrometheusAgent` selects `ServiceMonitor`, `PodMonitor`, `Probe` and `ScrapeConfig` objects with the same selector fields as `Prometheus`. The guide's example shows no remote storage settings, so look up `remoteWrite` in the API reference.

## Checked

2026-11-08. Read the Prometheus Agent guide and the design page in full. Version, RBAC and example match. Removed an unsourced DaemonSet feature gate claim and an unsourced remoteWrite instruction.

Method: documentation only; no commands were run.
