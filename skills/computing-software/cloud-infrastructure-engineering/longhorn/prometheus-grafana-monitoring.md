---
id: computing-software.cloud-infrastructure-engineering.longhorn.prometheus-grafana-monitoring
name: prometheus-grafana-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [prometheus, grafana, servicemonitor, metrics, networkpolicy]
level: practitioner
status: docs-checked
description: "Scrape Longhorn Manager metrics with a Prometheus ServiceMonitor, handle the restrictInternalTraffic NetworkPolicy and import Grafana dashboard 17626."
sources:
  - https://longhorn.io/docs/1.13.0/monitoring/prometheus-and-grafana-setup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: collect and graph Longhorn metrics.

Longhorn Manager exposes Prometheus-format metrics at `http://LONGHORN_MANAGER_IP:PORT/metrics`; the NetworkPolicy section references TCP port 9500. The guide runs the monitoring stack in `default` and Longhorn in `longhorn-system`.

ServiceMonitor:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: longhorn-prometheus-servicemonitor
  namespace: default
  labels:
    name: longhorn-prometheus-servicemonitor
spec:
  selector:
    matchLabels:
      app: longhorn-manager
  namespaceSelector:
    matchNames:
    - longhorn-system
  endpoints:
  - port: manager
```

With Helm set `metrics.serviceMonitor.enabled: true` and upgrade.

Steps:
1. Install the Prometheus Operator.
2. Create the ServiceMonitor (kubectl or Helm).
3. Deploy Alertmanager (3 replicas, config in secret `alertmanager-<name>`) and a PrometheusRule; add RBAC objects if RBAC is enabled.
4. Create the Prometheus resource selecting the ServiceMonitor and rules.
5. If `networkPolicies.restrictInternalTraffic` is enabled (default `true` as of v1.12.1), apply a scoped NetworkPolicy so your monitoring pods can reach port 9500 on Longhorn Manager, otherwise scraping is blocked.
6. Create a Grafana datasource ConfigMap pointing at `http://prometheus-longhorn.default.svc:9090`, deploy Grafana, log in (admin/admin by default in the guide) and import dashboard 17626.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/monitoring/prometheus-and-grafana-setup/

No claim needed changing.

Method: documentation only; no commands were run.
