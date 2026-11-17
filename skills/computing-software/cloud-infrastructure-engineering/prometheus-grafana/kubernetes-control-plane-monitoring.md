---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.kubernetes-control-plane-monitoring
name: kubernetes-control-plane-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [control-plane-monitoring, apiserver-metrics, etcd-monitoring, kube-scheduler, kube-controller-manager, kubernetes-monitoring]
level: advanced
status: docs-checked
description: "Scrape and alert on kube-apiserver, etcd, scheduler and controller-manager metrics: RBAC for /metrics, bind-address fixes, etcd health metrics and mixin burn-rate alerts."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/", "https://etcd.io/docs/v3.5/metrics/", "https://monitoring.mixins.dev/kubernetes/", "https://prometheus-operator.dev/docs/platform/troubleshooting/", "https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes control-plane monitoring

## Endpoints
- Kubernetes components emit Prometheus-format metrics on `/metrics`. For components that do not expose the
  endpoint by default, enable it with `--bind-address`. The Kubernetes page lists kube-controller-manager,
  kube-proxy, kube-apiserver, kube-scheduler and kubelet as examples.
- The kubelet also serves `/metrics/cadvisor`, `/metrics/resource` and `/metrics/probes`.
- With RBAC, the scraping identity needs a ClusterRole with `nonResourceURLs: ["/metrics"]` and verb `get`.
- kubeadm clusters: the Prometheus Operator troubleshooting page fixes unreachable controller-manager and scheduler
  targets by editing their static pod manifests under `/etc/kubernetes/manifests/` from `127.0.0.1` to `0.0.0.0`
  (its example edits `- --address=127.0.0.1`; check which address flag your Kubernetes version uses).
- kube-proxy: the kube-prometheus-stack README says the metrics bind address defaults to `127.0.0.1:10249`; set
  `metricsBindAddress: 0.0.0.0:10249` in the `kube-proxy` ConfigMap (`config.conf`, `KubeProxyConfiguration`) to scrape it.
- etcd: its metrics are served from its `/metrics` endpoint (the etcd page says to cURL it). Look up the listen
  address your distribution uses; it is not stated on the pages checked.
- Managed clusters: which control-plane endpoints you can reach is provider-specific. Disable the chart's
  `kubeControllerManager`, `kubeScheduler` and `kubeEtcd` ServiceMonitors if you cannot reach them.

## Key queries
```promql
# apiserver request error ratio (code and verb are labels of apiserver_request_total in the kubernetes-mixin rules)
sum(rate(apiserver_request_total{job="kube-apiserver",code=~"5.."}[5m])) / sum(rate(apiserver_request_total{job="kube-apiserver"}[5m]))
# etcd
etcd_server_has_leader == 0
increase(etcd_server_leader_changes_seen_total[1h])
histogram_quantile(0.99, sum by (le, instance) (rate(etcd_disk_wal_fsync_duration_seconds_bucket[5m])))
histogram_quantile(0.99, sum by (le, instance) (rate(etcd_disk_backend_commit_duration_seconds_bucket[5m])))
```
- etcd docs: `has_leader` is 1 when a leader exists and 0 otherwise; a member without a leader is totally
  unavailable. Rapid `leader_changes_seen_total` growth signals an unstable leader (network or load).
- etcd docs: high `wal_fsync_duration_seconds` or `backend_commit_duration_seconds` often indicates disk issues.
  The page gives no alert threshold; pick one from your own baseline.
- etcd docs: the `etcd_` prefix metrics are the stable ones intended for monitoring and alerting;
  `etcd_debugging_` metrics may change or vanish without warning.
- The kubernetes-mixin ships `KubeAPIErrorBudgetBurn` alerts built on `apiserver_request:burnrate*` recording
  rules: critical at 1h/5m (14.4x) and 6h/30m (6x), warning at 1d/2h (3x) and 3d/6h (1x) windows.

## Gotchas
- Kubernetes metrics follow a lifecycle (alpha, beta, stable, deprecated, hidden, deleted). A hidden metric needs
  `--show-hidden-metrics-for-version` on the component to reappear, so check release notes before upgrades.
- Opening bind addresses exposes endpoints on the node network; restrict with firewall or NetworkPolicy.

## Verify
- [ ] Targets for every control-plane component you can reach are up, or explicitly disabled in Helm values.
- [ ] `etcd_server_has_leader` alert fires when tested (for example in a non-production cluster).

## Checked
2026-11-08. Confirmed against the Kubernetes system-metrics page (`/metrics`, `--bind-address`, kubelet endpoints,
RBAC ClusterRole, hidden-metrics flag), the etcd v3.5 metrics page (has_leader, leader_changes_seen_total, wal_fsync,
backend_commit, stable versus debugging prefixes), kubernetes-mixin page (apiserver_request_total labels,
KubeAPIErrorBudgetBurn windows and multipliers), Prometheus Operator troubleshooting page (manifest address edit) and
the kube-prometheus-stack README (kube-proxy metricsBindAddress). Removed: per-component port numbers, etcd mvcc
size and quota query, scheduler attempts query, apiserver latency and inflight queries, fsync 10 ms threshold,
cardinality advice and provider-specific managed-cluster claims, none of which the pages state.
Method: documentation only; no commands were run.
