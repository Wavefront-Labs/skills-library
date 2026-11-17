---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-monitoring-and-alerting
name: etcd-monitoring-and-alerting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, etcd-metrics, endpoint-health, etcd-alerting, prometheus, wal-fsync, leader-changes, etcd-db-size, proposals-failed, servicemonitor, kube-prometheus-stack]
level: advanced
status: docs-checked
description: "Scrape etcd securely, know the six metrics that predict an etcd outage (fsync p99, leader changes, failed proposals, DB size, peer RTT, heartbeat failures) and the alert thresholds."
sources: ["https://etcd.io/docs/v3.6/metrics/", "https://etcd.io/docs/v3.6/faq/", "https://github.com/etcd-io/etcd/blob/main/contrib/mixin/alerts/alerts.libsonnet", "https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/values.yaml", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/phases/etcd/local.go", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apiserver/pkg/storage/etcd3/metrics/metrics.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd monitoring and alerting

**Goal:** see etcd trouble (slow disk, flapping leader, DB growth) hours before the API server
starts timing out. Pairs with `etcd-defragmentation-and-compaction` and
`etcd-storage-requirements` for the fixes.

## 1. Health, by hand
```bash
etcdctl endpoint health --cluster -w table     # per-member health + latency
etcdctl endpoint status --cluster -w table     # version, DB size, leader, raft index/term, errors (alarms)
etcdctl alarm list
```
A member with a RAFT INDEX far behind the others is lagging; a RAFT TERM that climbs between
runs means elections are happening.

## 2. Scraping etcd with Prometheus
kubeadm etcd serves `/metrics` on `--listen-metrics-urls` (default `http://127.0.0.1:2381`,
plaintext, no TLS). Easiest safe setup: set it to `http://0.0.0.0:2381` via
`ClusterConfiguration.etcd.local.extraArgs` and scrape port 2381 (metrics only, no data access).
With kube-prometheus-stack:
```yaml
kubeEtcd:
  enabled: true
  endpoints: [10.0.0.11, 10.0.0.12, 10.0.0.13]   # control-plane IPs, needed because etcd has no Service
  service: {port: 2381, targetPort: 2381}
  serviceMonitor: {scheme: http}
```
If you must scrape 2379 instead, etcd requires client certificates: set `serviceMonitor.scheme: https` and
the certificate settings under `serviceMonitor.tlsConfig` (any Prometheus Operator `SafeTLSConfig` field), with
the client certificate mounted into Prometheus.

## 3. The metrics that matter
| Metric | Alert when | Meaning |
|---|---|---|
| `histogram_quantile(0.99, rate(etcd_disk_wal_fsync_duration_seconds_bucket[5m]))` | etcd FAQ: p99 should stay under 10 ms; mixin warns above 0.5 s, critical above 1 s | disk too slow: the usual cause of etcd instability |
| `histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m]))` | etcd FAQ: p99 under 25 ms; mixin warns above 0.25 s | slow backend commits |
| `increase(etcd_server_leader_changes_seen_total[15m])` | mixin: 4 or more | elections: network or disk stalls |
| `etcd_server_has_leader` | mixin: == 0 for 1 minute | a member without a leader is unavailable |
| `rate(etcd_server_proposals_failed_total[15m])` | mixin: above 5 for 15 minutes | failed proposals: leader elections or quorum loss |
| `etcd_server_proposals_pending` | rising | client load, or the member cannot commit proposals |
| `etcd_mvcc_db_total_size_in_bytes / etcd_server_quota_backend_bytes` | mixin: above 95 percent (critical); alert earlier | approaching NOSPACE |
| `histogram_quantile(0.99, rate(etcd_network_peer_round_trip_time_seconds_bucket[5m]))` | mixin: above 0.15 s for 10 minutes | peer latency; keep the heartbeat interval near it |

Also watch the API server side: `apiserver_resource_objects` (what is growing; `apiserver_storage_objects` is
deprecated since Kubernetes 1.34) and `etcd_request_duration_seconds` (etcd latency as the API server sees it).

## 4. Ready-made rules
The etcd mixin (`contrib/mixin`) ships `etcdMembersDown`, `etcdInsufficientMembers`, `etcdNoLeader`,
`etcdHighNumberOfLeaderChanges`, `etcdHighNumberOfFailedGRPCRequests`, `etcdGRPCRequestsSlow`,
`etcdMemberCommunicationSlow`, `etcdHighNumberOfFailedProposals`, `etcdHighFsyncDurations`,
`etcdHighCommitDurations`, `etcdDatabaseQuotaLowSpace`, `etcdExcessiveDatabaseGrowth` and
`etcdDatabaseHighFragmentationRatio`. kube-prometheus-stack renders them when `kubeEtcd.enabled` and
`defaultRules.rules.etcd` are on; the rules only help if the etcd targets are actually `up`
(the chart's `kubeEtcd.endpoints` defaults to an empty list).

## Gotchas
- On managed clusters etcd is usually not exposed to you; use the API-server-side metrics (`etcd_request_duration_seconds`,
  `apiserver_resource_objects`) as proxies.
- `etcd_debugging_*` metrics are implementation dependent and may change or be removed without warning (etcd docs); do not build alerts on them.
- Counting leader changes per member double-counts; use `max by (job)` or alert per member.
- A single bad disk shows up only on that member's fsync histogram — always alert per instance,
  never on the aggregate.

## Verify
- [ ] `up` for your etcd scrape job is 1 for every member.
- [ ] A dashboard panel shows WAL fsync p99 under 10 ms at steady state (etcd FAQ guidance).
- [ ] In a test cluster, cutting one member off from its peers fires `etcdMembersDown` (check the rule's `for` duration).

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master); etcd mixin (etcd-io/etcd main); kube-prometheus-stack chart values (prometheus-community/helm-charts main).

Fixed: the kube-prometheus-stack chart now takes TLS settings for the etcd ServiceMonitor under `kubeEtcd.serviceMonitor.tlsConfig` (not `caFile`, `certFile`, `keyFile`); `apiserver_storage_objects` is deprecated since Kubernetes 1.34 in favour of `apiserver_resource_objects`; the etcd mixin thresholds are fsync p99 above 0.5 s (warning) and 1 s (critical), commit p99 above 0.25 s, peer round trip p99 above 0.15 s, quota use above 95 percent, four or more leader changes in 15 minutes, and `etcd_server_has_leader == 0` for 1 minute. Confirmed: kubeadm `--listen-metrics-urls=http://127.0.0.1:2381`; the etcd FAQ guidance of wal fsync p99 under 10 ms and backend commit p99 under 25 ms; the metric names `etcd_server_has_leader`, `etcd_server_leader_changes_seen_total`, `etcd_server_proposals_pending`, `etcd_server_proposals_failed_total`, `etcd_disk_wal_fsync_duration_seconds`, `etcd_disk_backend_commit_duration_seconds`, `etcd_network_peer_round_trip_time_seconds`; the chart's `kubeEtcd` defaults (enabled, port and targetPort 2381, scheme http) and that its etcd rules render with `kubeEtcd.enabled`. Removed as unconfirmed: `etcd_server_heartbeat_send_failures_total`, `etcd_server_slow_apply_total`, `etcd_server_slow_read_indexes_total`, `etcd_cluster_version`, the 100 ms hard-fail figure and the iptables test.

Method: documentation only; no commands were run.
