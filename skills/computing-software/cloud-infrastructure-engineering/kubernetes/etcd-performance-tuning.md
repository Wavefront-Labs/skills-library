---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-performance-tuning
name: etcd-performance-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd-operations, election-timeout, heartbeat-interval, etcd-fio, etcd-metrics]
level: practitioner
status: docs-checked
description: "Tune etcd heartbeat-interval and election-timeout for real RTT, benchmark disks with fio for fsync latency, and read the metrics that prove it."
sources: ["https://etcd.io/docs/v3.6/tuning/", "https://etcd.io/docs/v3.6/faq/", "https://etcd.io/docs/v3.6/dev-guide/limit/", "https://etcd.io/docs/v3.6/op-guide/configuration/", "https://github.com/etcd-io/etcd/blob/main/contrib/mixin/alerts/alerts.libsonnet", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/phases/etcd/local.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd performance tuning

## Disk first
etcd's latency is dominated by WAL fsync. The etcd FAQ recommends SSD and benchmarking the disk with a
tool such as fio, and gives these guides: p99 `etcd_disk_wal_fsync_duration_seconds` under 10 ms and p99
`etcd_disk_backend_commit_duration_seconds` under 25 ms. Slow shared or network disks fail this; give etcd a
dedicated disk and keep it off the disk used by container images and logs.

## Timing flags
| Flag | Default | Rule |
|---|---|---|
| `--heartbeat-interval` | 100 ms | about 0.5 to 1.5 times the round-trip time between members |
| `--election-timeout` | 1000 ms | at least 10 times the round-trip time (tuning page); at least 5 times the heartbeat interval (FAQ) |

The defaults suit a local network. Across data centres, raise the heartbeat interval to about the round-trip
time and the election timeout to match (the tuning page's upper limit for the election timeout is 50000 ms).
Set identical values on every member, through the etcd static pod manifest or
`ClusterConfiguration.etcd.local.extraArgs`.

## Other knobs
- `--snapshot-count` (default 10000 in the 3.6 configuration reference): lowering it can reduce memory and disk use.
- `--quota-backend-bytes`: default 2 GiB; 8 GiB is the suggested maximum and etcd warns at startup above it.
- On Linux, `ionice -c2 -n0 -p <etcd-pid>` gives etcd the highest best-effort disk priority if disks are shared.
- CPU: the kubeadm etcd static pod requests 100m CPU and 100Mi memory; the FAQ names CPU starvation as the second
  most common cause of slow applies and missed heartbeats, so give heavy clusters dedicated machines.

## Metrics that prove it
```promql
histogram_quantile(0.99, rate(etcd_disk_wal_fsync_duration_seconds_bucket[5m]))     # FAQ: < 10ms
histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m])) # FAQ: < 25ms
rate(etcd_server_leader_changes_seen_total[1h])                                      # ~0
histogram_quantile(0.99, rate(etcd_network_peer_round_trip_time_seconds_bucket[5m]))
```
The warnings `apply entries took too long` and `failed to send out heartbeat on time` are usually caused by a
slow disk, then CPU starvation, then a slow network (etcd FAQ), before a timeout setting problem.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master); etcd mixin (etcd-io/etcd main); kube-prometheus-stack chart values (prometheus-community/helm-charts main).

Fixed: the election timeout rule: the tuning page says the election timeout must be at least 10 times the round-trip time (the FAQ says at least 5 times the heartbeat interval) and the heartbeat interval should be about 0.5 to 1.5 times the round-trip time, not "at least 10x the heartbeat"; the quota default is 2 GiB with 8 GiB a suggested maximum and a startup warning above it. Confirmed: heartbeat default 100 ms and election timeout default 1000 ms; identical values on all members; snapshot-count default 10000 in the 3.6 configuration reference; `ionice -c2 -n0` for etcd (tuning page); FAQ guidance of wal fsync p99 under 10 ms and backend commit p99 under 25 ms; the kubeadm etcd static pod requests 100m CPU and 100Mi memory (kubeadm source); the warnings "apply entries took too long" and "failed to send out heartbeat on time" are caused by slow disk, CPU starvation or network (FAQ). Removed as unconfirmed: the fio command line and its size and block-size values, and the 300/3000 cross-region example.

Method: documentation only; no commands were run.
