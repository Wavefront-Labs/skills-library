---
id: computing-software.cloud-infrastructure-engineering.contour.contour-prometheus-metrics-and-dashboards
name: contour-prometheus-metrics-and-dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [prometheus, metrics, podmonitor, grafana, port-8000, port-8002, kube-prometheus, stats-prometheus]
level: practitioner
status: docs-checked
description: "Scraping Contour (/metrics, port 8000) and Envoy (/stats/prometheus, port 8002) with Prometheus Operator PodMonitors, plus sample Grafana dashboards from the examples directory."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/prometheus.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus metrics for Contour and Envoy

Endpoints:
- Contour serves `/metrics` on port 8000 by default; change with `--http-address` and `--http-port` on `contour serve`. The Contour Service manifest must show the same port.
- Envoy serves `/stats/prometheus` on port 8002. A static Envoy listener forwards only to the stats endpoint, so the rest of the admin interface is not exposed to Prometheus or other workloads.

Sample stack using kube-prometheus (Prometheus Operator, Prometheus, Grafana):

1. Install the monitoring stack following the Prometheus Operator quick start (it is a quickstart, not production).
2. Optionally expose Prometheus and Grafana through Contour with `examples/prometheus/httpproxy.yaml` and `examples/grafana/httpproxy.yaml`.
3. Allow scraping in the `projectcontour` namespace: `kubectl apply -f examples/prometheus/rbac.yaml` (a Role and RoleBinding).
4. Add `PodMonitor` resources for Contour and Envoy pods: `kubectl apply -f examples/prometheus/podmonitors.yaml`.
5. Grafana dashboards ship as ConfigMaps: `kubectl apply -f examples/grafana/dashboards.yaml`, then patch the Grafana Deployment:

```sh
kubectl -n monitoring patch deployment grafana --type=json --patch-file examples/grafana/deployment-patch.json
```

The Contour and Envoy dashboards then appear in Grafana.

## Checked

2026-11-04. Confirmed against the Contour Prometheus guide (guides/prometheus.md): the fields, defaults, flags and behaviours stated above. Removed: the advice to alert on specific Envoy counters (not on the page).

Method: documentation only; no commands were run.
