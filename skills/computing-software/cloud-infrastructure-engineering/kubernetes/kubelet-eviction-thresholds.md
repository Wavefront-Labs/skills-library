---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-eviction-thresholds
name: kubelet-eviction-thresholds
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet, kubelet-eviction, eviction-hard, eviction-soft, node-pressure-eviction, memory-pressure, eviction-signals]
level: advanced
status: docs-checked
description: "Tune kubelet node-pressure eviction: hard vs soft thresholds and grace periods, eviction signals, minimum reclaim, and how pods are ranked for eviction by QoS and usage."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubelet eviction thresholds

## Signals
| Signal | Source |
|---|---|
| `memory.available` | node memory capacity minus working set (the kubelet excludes `inactive_file`) |
| `nodefs.available`, `nodefs.inodesFree` | node filesystem (kubelet volumes and logs) |
| `imagefs.available`, `imagefs.inodesFree` | container runtime image filesystem (if separate) |
| `containerfs.available`, `containerfs.inodesFree` | writable layers if split from imagefs (CRI-O 1.29+ supports it) |
| `pid.available` | max PIDs minus current process count |

Default hard thresholds (Linux): `memory.available<100Mi, nodefs.available<10%, imagefs.available<15%,
nodefs.inodesFree<5%, imagefs.inodesFree<5%`. The defaults apply only if you change none of the
parameters: set **any** hard threshold and the unspecified ones become zero unless you repeat
them (or set `mergeDefaultEvictionSettings: true`) — specify the full map.

## Configure
```yaml
evictionHard:
  memory.available: 500Mi
  nodefs.available: 10%
  nodefs.inodesFree: 5%
  imagefs.available: 15%
evictionSoft:
  memory.available: 1Gi
  nodefs.available: 15%
evictionSoftGracePeriod:
  memory.available: 1m30s
  nodefs.available: 2m
evictionMaxPodGracePeriod: 60          # max pod termination grace (seconds) used for soft evictions
evictionMinimumReclaim:
  memory.available: 200Mi
  nodefs.available: 1Gi
evictionPressureTransitionPeriod: 5m   # wait before flipping a node condition back (default 5m)
```
- **Hard**: pods are killed immediately with a 0s grace period. **Soft**: only after the signal stays over
  threshold for its grace period; the kubelet respects `evictionMaxPodGracePeriod`.
- `evictionMinimumReclaim` keeps reclaiming until the stated amount is freed, avoiding repeated
  evictions near the threshold (default 0 for all resources).

## Who gets evicted
1. BestEffort or Burstable pods whose usage exceeds requests, ordered by Pod Priority and then by how far
   usage exceeds the request,
2. then Guaranteed pods and Burstable pods under their requests, last, by Priority.
The kubelet does not use the QoS class itself for the order. It first tries to reclaim node-level
resources (for example removing unused images when disk is short) before evicting pods.

## Observe
```bash
kubectl describe node <n>                            # MemoryPressure/DiskPressure/PIDPressure conditions
kubectl get events -A --field-selector reason=Evicted
kubectl get pods -A --field-selector status.phase=Failed
```
The node controller taints a node under pressure (for example `node.kubernetes.io/memory-pressure`, NoSchedule).

## Gotchas
- Eviction is not instant: thresholds are evaluated on the kubelet `housekeeping-interval` (default
  10s). If the node hits an OOM event before the kubelet reclaims memory, the kernel `oom_killer`
  decides. Leave headroom in the `memory.available` threshold.
- Evicted pods stay as `Failed` objects until they are garbage collected — clean up or they clutter.

## Verify
- [ ] The kubelet config (`/api/v1/nodes/<node>/proxy/configz`) shows the full evictionHard map; soft thresholds have grace periods set.
- [ ] Load test produces `Evicted` events, not kernel OOM kills of system processes.

## Checked
2026-10-23, against the Kubernetes website node-pressure eviction page (signal definitions, default hard thresholds and the "set one, others become zero" rule with mergeDefaultEvictionSettings, soft/hard grace behaviour, eviction order, 5m transition default, 10s housekeeping-interval, minimum-reclaim default 0, oom_killer note, containerfs support note). The 1.31 version tag, the `/var/lib/kubelet` filesystem statement and the PodGC remark were removed or reworded as unconfirmed.
Method: documentation only; no commands were run.
