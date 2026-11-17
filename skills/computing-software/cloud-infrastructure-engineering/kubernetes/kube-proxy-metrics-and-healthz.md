---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-proxy-metrics-and-healthz
name: kube-proxy-metrics-and-healthz
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-proxy, kube-proxy-metrics, healthz, prometheus, monitoring]
level: practitioner
status: docs-checked
description: "Scrape kube-proxy metrics by changing metricsBindAddress, read its healthz endpoint and alert on stale or slow rule syncs."
sources: ["https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/", "https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://kubernetes.io/docs/reference/networking/virtual-ips/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/proxy/healthcheck/proxy_health.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kube-proxy metrics and healthz

## Endpoints
| Port | Path | Default bind |
|---|---|---|
| 10249 | `/metrics`, `/proxyMode` | `127.0.0.1` (not scrapeable from Prometheus pods) |
| 10256 | `/healthz`, `/livez` | `0.0.0.0` |

Expose metrics (kubeadm clusters):
```bash
kubectl -n kube-system edit cm kube-proxy      # config.conf: metricsBindAddress: 0.0.0.0:10249
kubectl -n kube-system rollout restart ds kube-proxy
```
Set `healthzBindAddress` similarly if needed. Restrict port 10249 to the monitoring network.

## healthz
```bash
curl -s http://<node-ip>:10256/healthz
# {"lastUpdated":"...","currentTime":"...","nodeEligible":true}
```
`/healthz` returns 503 when a queued rules update is overdue or the node is not eligible (it has a deletion
timestamp or the cluster autoscaler's to-be-deleted taint). `/livez` returns 503 only for the overdue-sync case.

## Metrics to watch
```promql
histogram_quantile(0.99, rate(kubeproxy_sync_proxy_rules_duration_seconds_bucket[5m]))
time() - kubeproxy_sync_proxy_rules_last_timestamp_seconds          # staleness
histogram_quantile(0.99, rate(kubeproxy_network_programming_duration_seconds_bucket[5m]))
kubeproxy_sync_proxy_rules_iptables_total                          # rules owned by kube-proxy (labels ip_family, table)
```
Alert on growing staleness or sync times (large rule sets; consider nftables mode). The sync-duration metric is
also what the Service docs point to when deciding whether to raise `minSyncPeriod` (default 1s).

## Verify
Prometheus shows `up{job="kube-proxy"} == 1` for every node.

## Checked

2026-10-26: kube-proxy reference, generated metrics reference and virtual-ips page (v1.37 docs, kubernetes/website main 2026-10-25) plus kube-proxy healthcheck and server source (kubernetes/kubernetes main). Confirmed: metrics default 127.0.0.1:10249 and healthz default 0.0.0.0:10256, /proxyMode, /healthz and /livez behaviour and the nodeEligible JSON field, the four metric names. Removed the unconfirmed claims that port 10249 is unauthenticated and that load balancers use healthz in a particular way.

Method: documentation only; no commands were run.
