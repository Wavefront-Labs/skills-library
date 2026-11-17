---
id: computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-observability-apiserver-and-etcd
name: control-plane-observability-apiserver-and-etcd
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-apiserver, etcd, control-plane, apf, priority-and-fairness, etcd-compaction, etcd-db-size, request-latency, audit-log, controller-manager, scheduler-metrics]
level: sme
status: docs-checked
description: "Monitor kube-apiserver and etcd: request latency, API Priority and Fairness rejections, etcd DB size, compaction and disk latency, and early signs of control-plane degradation."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/flow-control/", "https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://etcd.io/docs/v3.6/op-guide/maintenance/", "https://etcd.io/docs/v3.6/faq/", "https://etcd.io/docs/v3.6/tuning/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control-plane observability: watching kube-apiserver and etcd before they fall over

**Goal:** know the handful of control-plane metrics that give leading warning of a cluster
going generally unresponsive — slow `kubectl`, stalled reconciliation, HPA/scheduler lag —
before workload-level symptoms (which show up last, after the control plane is already
struggling).

**Note on scope:** for a fully managed control plane (EKS/GKE/AKS), etcd and some apiserver
internals may be inaccessible — several of these metrics/logs are only available on
self-managed or semi-managed (e.g. exposed kube-apiserver metrics endpoints) clusters; check
what your provider actually exposes before building alerts on metrics you can't scrape.

## 1. kube-apiserver: request latency and saturation
- `apiserver_request_duration_seconds` (stable histogram, labels include `verb`, `group`, `resource`,
  `subresource`, `scope`, `component`, `dry_run`) is the primary signal; watch p99 **per verb and
  resource**, not in aggregate, since a slow `LIST` on a large collection can hide inside an
  otherwise-healthy aggregate.
- **API Priority and Fairness (APF)** is stable since v1.29 and enabled by default
  (`--enable-priority-and-fairness`, default true); it replaces the max-in-flight handler with one
  that queues and dispatches with priority and fairness. Beta metrics
  `apiserver_flowcontrol_rejected_requests_total` (labels `flow_schema`, `priority_level`, `reason`)
  and `apiserver_flowcontrol_request_wait_duration_seconds` show when APF is rejecting or queueing
  requests; a spike is an early sign that a client (a misbehaving controller doing heavy LIST/WATCH,
  or many clients reconnecting after a restart) is saturating request capacity.
- `apiserver_current_inflight_requests` (stable gauge, label `request_kind`) is the maximal number of
  in-flight requests used in the last second. With APF on, `--max-requests-inflight` (default 400) and
  `--max-mutating-requests-inflight` (default 200) are summed to give the server's total concurrency
  limit; with APF off they limit in-flight requests directly. Per-priority-level limits come from
  `PriorityLevelConfiguration` objects.
- Audit logs (separate from Events; see
  `computing-software.cloud-infrastructure-engineering.kubernetes.kubernetes-event-based-debugging`)
  are the forensic layer: who called what and with what response code, so you can trace a slow or
  failing request back to a client.

## 2. etcd: the metrics that predict an outage before it happens
etcd is where Kubernetes state lives; its degradation affects every controller.
- **`etcd_disk_backend_commit_duration_seconds`** and **`etcd_disk_wal_fsync_duration_seconds`**:
  disk latency. The etcd FAQ says etcd's performance depends strongly on disk performance (SSD
  recommended), and that for the "apply request took too long" warning you should monitor
  `backend_commit_duration_seconds`, where p99 should be less than 25ms; a slow or shared disk is
  the usual cause, and a dedicated or faster disk the usual fix. etcd's tuning guide also notes that
  other processes' disk activity can cause long `fsync` latencies and missed heartbeats.
- **`etcd_mvcc_db_total_size_in_bytes`** against the backend quota (`--quota-backend-bytes`; 0 uses
  the default 2GiB, and the source's suggested maximum is 8GB). Exceeding the quota triggers an
  alarm and puts etcd in read-only mode: writes fail with `etcdserver: mvcc: database space
  exceeded`, so Kubernetes cannot persist new objects or status. Watch the trend and alert well
  before the quota.
- **Compaction**: etcd keeps the revision history until compacted. Without periodic compaction (for
  example `--auto-compaction-mode` with `--auto-compaction-retention`; the modes are `periodic`,
  which is the default, and `revision`) etcd eventually exhausts its storage space, and defragmentation
  is a separate step. The compaction metrics are in the `etcd_debugging_mvcc_db_compaction_*`
  family.
- `etcd_server_leader_changes_seen_total` counts leader changes; frequent changes point at
  disk, network or resource problems (the etcd FAQ ties slow disks to leader liveness).
- `etcd_network_peer_round_trip_time_seconds`: the etcd tuning guide says the heartbeat interval
  (default 100ms) should be set around the round-trip time between members, and the election
  timeout defaults to 1000ms; members spread across distant zones or data centers need those tuned.

## 3. kube-scheduler and controller-manager
- `scheduler_scheduling_attempt_duration_seconds` and `scheduler_pending_pods` (by queue:
  `active`, `backoff`, `unschedulable`) — a growing `unschedulable` queue with stable node
  capacity is a resource-fit problem (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.pod-scheduling-and-resource-requests`),
  not a scheduler performance problem; distinguish before tuning scheduler throughput.
- `workqueue_depth` and `workqueue_adds_total` per controller (exposed by controller-manager
  and most custom controllers using client-go's workqueue) show reconciliation backlog —
  a specific controller's queue growing unbounded while others stay flat points at that
  controller, not the control plane generally.

## Gotchas
- Control-plane metrics are themselves scraped **by** Prometheus, which depends on
  apiserver/kube-state-metrics being healthy to discover targets — in a severe control-plane
  outage, the monitoring system watching the control plane can degrade at the same time;
  a federated/remote-write setup shipping to storage outside the affected cluster
  (`computing-software.cloud-infrastructure-engineering.kubernetes.long-term-metrics-storage-thanos-and-mimir`)
  avoids losing visibility exactly when it matters most.
- etcd serves `/metrics` on its client port and optionally on the locations given by
  `--listen-metrics-urls`; if you use a separate metrics listener, make sure firewall and
  NetworkPolicy rules allow the scraper to reach it.
- Managed clusters (EKS/GKE/AKS) typically don't expose etcd metrics at all; apiserver
  metrics may also be restricted or emitted with reduced cardinality — verify what's
  actually available before designing alerts around metrics you can't reach.

## Verify
- [ ] `apiserver_request_duration_seconds` p99 is graphed per verb/resource, not only in aggregate.
- [ ] `apiserver_flowcontrol_rejected_requests_total` is alerted on, giving warning before apiserver CPU/memory alerts would fire.
- [ ] etcd DB size is graphed against its quota with headroom alerting, and auto-compaction is confirmed configured and running.
- [ ] etcd backend commit latency p99 is alerted against the 25ms level from the etcd FAQ, and fsync latency is graphed.

## Checked
Checked 2026-10-24 against the kubernetes/website Metrics Reference (names, types, stability and labels of
the apiserver, scheduler and workqueue metrics), the API Priority and Fairness page (stable v1.29, on by
default), the kube-apiserver flag reference (APF flag, in-flight defaults 400 and 200), the etcd website
(maintenance: quota, compaction modes; FAQ: 25ms commit-latency guidance, "database space exceeded";
tuning: heartbeat and election defaults; monitoring: `--listen-metrics-urls`) and etcd source (default
quota 2GiB, metric names). Removed: the 25-50ms fsync rule of thumb, "usually 2381" port and the
claim that exceeding the quota stops reads (etcd goes read-only).
Method: documentation only; no commands were run.
