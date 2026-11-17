---
id: computing-software.cloud-infrastructure-engineering.kubernetes.vpa-updater-eviction-tuning
name: vpa-updater-eviction-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, vpa, min-replicas-vpa, eviction-tolerance, vpa-updater, pdb]
level: practitioner
status: docs-checked
description: "Tune VPA updater evictions with --min-replicas, --eviction-tolerance, rate limits and per-VPA minReplicas so applying recommendations never takes a workload down."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/flags.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/api.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPA updater eviction tuning

In `Recreate` (and `Auto`) mode the updater evicts pods whose requests drift from the
recommendation so the admission controller can resize them on recreation.

## Updater flags
| Flag | Default | Meaning |
|---|---|---|
| `--min-replicas` | 2 | do not evict if the controller has fewer live replicas |
| `--eviction-tolerance` | 0.5 | max fraction of a controller's replicas evicted in one pass |
| `--eviction-rate-limit` | -1 (0 or -1 disables) | evictions per second |
| `--eviction-rate-burst` | 1 | burst for the rate limit |
| `--updater-interval` | 1m | how often it runs |
| `--pod-update-threshold` | 0.1 | ignore updates with priority below this |
| `--in-recommendation-bounds-eviction-lifetime-threshold` | 12h | pods this old can be evicted even if their request is within the recommended range |
| `--evict-after-oom-threshold` | 10m | evict pods that OOMed within this time of start |

## Per VPA
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata: {name: api}
spec:
  targetRef: {apiVersion: apps/v1, kind: Deployment, name: api}
  updatePolicy:
    updateMode: Recreate
    minReplicas: 3          # overrides --min-replicas for this workload
```
Single-replica workloads are never evicted under the default; set `minReplicas: 1` only if
downtime is acceptable.

## Also respected
- PodDisruptionBudgets: the updater uses the eviction API, so a PDB blocks it.
- Eviction candidates are chosen by update priority (threshold `--pod-update-threshold`); pods whose
  request is already within the recommended range are only evicted once they are older than
  `--in-recommendation-bounds-eviction-lifetime-threshold`.
- The updater stops evicting when the admission controller status is stale
  (`--use-admission-controller-status`, default true).

## Verify
```bash
kubectl -n kube-system logs deploy/vpa-updater
kubectl get events -A --field-selector reason=EvictedByVPA
```
Evictions should come in small waves and never drop ready replicas below the PDB.

## Checked

Checked 2026-10-24 against flags.md and api.md in kubernetes/autoscaler vertical-pod-autoscaler (master, VPA 1.8.1) and the updater source.
- Updater defaults confirmed: `min-replicas` 2, `eviction-tolerance` 0.5, `eviction-rate-limit` -1 (0 or -1 disables), `eviction-rate-burst` 1, `updater-interval` 1m, `pod-update-threshold` 0.1, `in-recommendation-bounds-eviction-lifetime-threshold` 12h, `evict-after-oom-threshold` 10m, `use-admission-controller-status` true.
- `updatePolicy.minReplicas` overrides the global flag and only positive values are allowed: api.md.
- `EvictedByVPA` event reason: updater source (pkg/updater/logic/updater.go).
- Eviction is subject to other checks such as PodDisruptionBudgets: api.md `updatePolicy.minReplicas` description.

Method: documentation only; no commands were run.
