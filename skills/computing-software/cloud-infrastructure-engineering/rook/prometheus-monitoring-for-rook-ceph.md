---
id: computing-software.cloud-infrastructure-engineering.rook.prometheus-monitoring-for-rook-ceph
name: prometheus-monitoring-for-rook-ceph
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [prometheus, servicemonitor, ceph-exporter, prometheus-mgr-module, prometheusendpoint, monitoring]
level: practitioner
status: docs-checked
description: "Monitor a Rook Ceph cluster with Prometheus: metric sources, the Prometheus operator, service monitors, and the dashboard prometheusEndpoint settings."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Monitoring/ceph-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Rook Ceph cluster has built-in collectors for Prometheus. An existing Prometheus finds Rook's scrape endpoint through the standard `prometheus.io/scrape` and `prometheus.io/port` annotations, provided it watches all namespaces. If it does not watch third-party service monitors, add those annotations or consult the Prometheus operator docs.

Two metric sources:
- The Prometheus manager module exposes all metrics other than daemon performance counters.
- The Ceph exporter exposes only Ceph daemon performance counters as Prometheus metrics.

To set up a new instance: start the Prometheus operator and wait for it to be `Running`, then from the cloned Rook repo's monitoring directory create the service monitor plus the Prometheus server pod and service. Confirm the pod:
```
kubectl -n rook-ceph get pod prometheus-rook-prometheus-0
```
Get the URL with `echo "http://$(kubectl -n rook-ceph -o jsonpath={.status.hostIP} get pod prometheus-rook-prometheus-0):30900"`.

Let the dashboard read metrics through two settings in the CephCluster CR: `prometheusEndpoint` (the URL) and `prometheusEndpointSSLVerify` (verify SSL if the server uses https). In the Prometheus UI, graph a metric such as `ceph_cluster_total_used_bytes`.

Do not use storage from the monitored Ceph cluster for Prometheus: if Ceph fails, Prometheus becomes unresponsive and cannot alert you.

## Checked

2026-11-03. Confirmed against the Ceph Monitoring page: the scrape annotations, the two metric sources, the prometheus-rook-prometheus-0 pod and port 30900 URL, prometheusEndpoint and prometheusEndpointSSLVerify, and the advice not to host Prometheus on the monitored Ceph. Removed: nothing.

Method: documentation only; no commands were run.
