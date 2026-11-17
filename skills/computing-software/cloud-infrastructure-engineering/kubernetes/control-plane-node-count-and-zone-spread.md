---
id: computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-node-count-and-zone-spread
name: control-plane-node-count-and-zone-spread
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, control-plane-sizing, etcd-quorum-sizing, etcd, control-plane-ha, availability-zones]
level: practitioner
status: docs-checked
description: "Choose control-plane and etcd member counts (3 or 5) and spread them across zones so one failure keeps quorum; why even counts and two zones do not help."
sources: ["https://etcd.io/docs/v3.5/faq/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/", "https://kubernetes.io/docs/setup/best-practices/multiple-zones/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control-plane node count and zone spread

## Quorum arithmetic
Quorum = floor(n/2) + 1.

| etcd members | quorum | failures tolerated |
|---|---|---|
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |

Even counts add a member without adding tolerance (etcd FAQ). Use 3 for most clusters, 5 when
you must survive two simultaneous failures (one in maintenance plus one unplanned). The etcd FAQ
suggests no more than seven members and says five tolerate two failures, enough in most cases;
larger clusters replicate data to more machines, so write performance suffers.

## Zone layout
- 3 members in 3 zones: any one zone can fail.
- 3 members in 2 zones: losing the zone with 2 members loses quorum. Two zones never give
  zone-level HA for etcd; add a small third-zone member (stacked or external) instead.
- 5 members over 3 zones (2-2-1): survives one zone loss.

## Sizing the machines
- Disk latency is part of etcd leader liveness (etcd FAQ): use fast disks and watch the
  `wal_fsync_duration_seconds` metric.
- Size control-plane machines from observed apiserver memory and request latency; no fixed
  figure is given here.
- Crossing data-center boundaries raises consensus latency (etcd FAQ), so keep members in
  one region unless you have tuned etcd's timeouts.

## Verify
```bash
etcdctl endpoint status --cluster -w table     # one leader, matching raft index
kubectl get nodes -l node-role.kubernetes.io/control-plane -L topology.kubernetes.io/zone
```
Each zone hosts at most floor((n-1)/2) members.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: etcd v3.5 FAQ (quorum is n/2+1 and the 3/4/5/7 member table, odd sizes, member limit guidance, latency across data centers, disk latency and leader liveness) and the kubeadm HA topology page. Zone-layout statements are arithmetic on those quorum rules. Removed the unconfirmed 10 ms and 4 vCPU/16 GiB figures.

Method: documentation only; no commands were run.
