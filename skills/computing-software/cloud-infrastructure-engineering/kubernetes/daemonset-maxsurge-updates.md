---
id: computing-software.cloud-infrastructure-engineering.kubernetes.daemonset-maxsurge-updates
name: daemonset-maxsurge-updates
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, daemonset, daemonset-maxsurge, rollingupdate, maxunavailable, daemonset-rollback]
level: practitioner
status: docs-checked
description: "Use DaemonSet rollingUpdate.maxSurge for zero-gap node agent updates, its constraints (maxUnavailable 0, hostPort conflicts) and rollout monitoring."
sources: ["https://kubernetes.io/docs/tasks/manage-daemon/update-daemon-set/", "https://kubernetes.io/docs/tasks/manage-daemon/rollback-daemon-set/", "https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/daemon-set-v1/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DaemonSet maxSurge

Default DaemonSet RollingUpdate kills the old pod then starts the new one on each node
(`maxUnavailable: 1`), leaving a gap. For log shippers, CNI-adjacent agents or node-local DNS
that gap drops data or traffic. `maxSurge` (stable in 1.25) starts the new pod first. Default `maxSurge` is 0 and default `maxUnavailable` is 1.

```yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # or "10%"
      maxUnavailable: 0    # must be 0 when maxSurge > 0
  minReadySeconds: 10
```
Old pod is removed once the new one is Ready (plus minReadySeconds).

## Constraints
- `hostPort` and `hostNetwork` port binds: two pods on the same node cannot both bind the same
  port, so the surge pod cannot run beside the old one. Use surge only for agents without host
  port conflicts.
- Exclusive host resources (device files, lock files, a single GPU) conflict the same way.
- Node capacity: the API docs warn that allowing surge means the resources consumed by the
  DaemonSet on a node can double, so resource-intensive DaemonSets may cause evictions.
- `maxSurge` and `maxUnavailable` cannot both be zero, and (API validation) they cannot both be
  non-zero; `maxSurge` percentages round up to a minimum of 1.
- If the old pod becomes unavailable (not Ready, evicted or drained), an updated pod is created
  on that node immediately, without regard to surge limits.

## Rollout control
```bash
kubectl rollout status ds/fluent-bit -n logging
kubectl rollout history ds/fluent-bit -n logging
kubectl rollout undo ds/fluent-bit -n logging
kubectl get pods -n logging -l app=fluent-bit -L controller-revision-hash
```
`maxSurge` and `maxUnavailable` accept a percentage of desired pods, which suits large fleets.

## Verify
During the rollout `kubectl get pods -o wide` shows two pods on a node briefly, and agent
metrics show no gap (for example no drop in log ingestion per node).

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the update-daemon-set task, the apps/v1 Go types and the apps validation source: defaults maxUnavailable 1, maxSurge 0, minReadySeconds 0; maxSurge cannot be 0 when maxUnavailable is 0, and validation rejects both non-zero; percentage rounding; the surge pod's old pod is deleted once the new one is available for minReadySeconds; resource-doubling warning; feature gate DaemonSetUpdateSurge beta 1.22, stable 1.25 (removed 1.26); kubectl rollout status, history and undo accept daemonset (rollback task page).
Removed: SO_REUSEPORT and the "500-node update takes hours" remark.

Method: documentation only; no commands were run.
