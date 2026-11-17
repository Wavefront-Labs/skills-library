---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-autoscaler-status-configmap
name: cluster-autoscaler-status-configmap
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-autoscaler, cluster-autoscaler-status, node-autoscaling, events, troubleshooting]
level: practitioner
status: docs-checked
description: "Read the cluster-autoscaler-status ConfigMap and the scale-up and scale-down events to find out why nodes are or are not being added or removed."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://github.com/kubernetes-sigs/cluster-autoscaler/blob/main/pkg/clusterstate/api/types.go", "https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cluster-autoscaler-status

## The ConfigMap
```bash
kubectl -n kube-system get configmap cluster-autoscaler-status -o jsonpath='{.data.status}'
```
Written every loop (`--write-status-configmap=true`, the default). It shows:
- Cluster-wide health: `Healthy` or `Unhealthy`, with ready, unready, not-started, registered and
  unregistered node counts.
- Per node group: health, `cloudProviderTarget` vs registered nodes, min and max size,
  ScaleUp status (`InProgress`, `NoActivity`, `Backoff`) and ScaleDown status
  (`CandidatesPresent`, `NoCandidates`).
The status is a YAML document. The ConfigMap name is set by `--status-config-map-name`
(default `cluster-autoscaler-status`).

## Events
```bash
kubectl get events -A --field-selector reason=TriggeredScaleUp
kubectl get events -A --field-selector reason=NotTriggerScaleUp     # on pending pods
kubectl get events -A --field-selector reason=ScaleDown
kubectl get events -A --field-selector reason=ScaleDownFailed
```
`NotTriggerScaleUp` is recorded on a pod when no node group can be scaled up to make it
schedulable, for example `pod didn't trigger scale-up (it wouldn't fit if a new node is added)`.
The ConfigMap itself also gets `ScaledUpGroup`, `ScaleDownEmpty` and `ScaleDown` events.

## Common states
| Status | Meaning |
|---|---|
| ScaleUp `Backoff` | a recent scale-up failed, so no further attempts for some time; check CA logs for the cloud error |
| node group target > registered for long | instances failing to register; CA waits `--max-node-provision-time` (default 15m) before treating them as unregistered |
| node never scaled down | pods with `safe-to-evict: "false"`, local storage, restrictive PDBs, non-replicated pods, or the `scale-down-disabled` annotation |

## Logs
```bash
kubectl -n kube-system logs deploy/cluster-autoscaler
```
The FAQ recommends `--v=4` to see the decision-making reasons; levels above `--v=1` produce much more log volume.

## Verify
After fixing, the next loop shows `ScaleUp: InProgress` and a `TriggeredScaleUp` event on the pod.

## Checked

Checked 2026-10-24. The documentation checked is the Cluster Autoscaler FAQ and provider READMEs in kubernetes/autoscaler (master, 2026-10-24); the autoscaler binary source now lives in kubernetes-sigs/cluster-autoscaler.
- Status ConfigMap contents (Healthy/Unhealthy, node counts, `cloudProviderTarget`, `minSize`, `maxSize`, ScaleUp `InProgress`/`NoActivity`/`Backoff`, ScaleDown `CandidatesPresent`/`NoCandidates`) and the YAML tags: status types in kubernetes-sigs/cluster-autoscaler `pkg/clusterstate/api/types.go`.
- `--write-status-configmap` default true, `--status-config-map-name` default, `--max-node-provision-time` default 15m, `--v=4` advice, event names and which object each event is recorded on (`TriggeredScaleUp`, `NotTriggerScaleUp`, `ScaleDown`, `ScaleDownFailed`, `ScaledUpGroup`, `ScaleDownEmpty`), the list of pods that block scale-down: FAQ.

Method: documentation only; no commands were run.
