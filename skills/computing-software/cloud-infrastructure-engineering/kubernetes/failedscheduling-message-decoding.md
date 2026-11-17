---
id: computing-software.cloud-infrastructure-engineering.kubernetes.failedscheduling-message-decoding
name: failedscheduling-message-decoding
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, failedscheduling, didnt-match-node-affinity, untolerated-taint, volume-node-affinity-conflict, pending-pods, troubleshooting, cka]
level: practitioner
status: docs-checked
description: "Decode FailedScheduling messages (untolerated taint, node affinity/selector mismatch, volume node affinity conflict, insufficient resources) and fix the right side."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/", "https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/", "https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode", "https://github.com/kubernetes/kubernetes/tree/master/pkg/scheduler/framework/plugins"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decoding FailedScheduling messages

```bash
kubectl describe pod <p> | grep -A3 FailedScheduling
# 0/6 nodes are available: 2 node(s) had untolerated taint(s), 3 node(s) didn't match
#   Pod's node affinity/selector, 1 node(s) didn't match PersistentVolume's node affinity.
#   preemption: 0/6 nodes are available: 6 Preemption is not helpful for scheduling.
```
Each count is a number of nodes rejected for that reason. The exact wording changes between releases
(the strings above are from the current kube-scheduler source), so match on the meaning.

## Per message
**`had untolerated taint(s)`**
```bash
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints
```
Either add a matching toleration (operator/effect must match; `Exists` ignores value) or the pod
is correctly excluded. The kubeadm control-plane taint `node-role.kubernetes.io/control-plane:NoSchedule`
shows up here too.

**`didn't match Pod's node affinity/selector`**
```bash
kubectl get pod <p> -o jsonpath='{.spec.nodeSelector}{"\n"}{.spec.affinity.nodeAffinity}'
kubectl get nodes -L <key>
```
Typo in label key/value, label missing from new node pools, `requiredDuringScheduling` with
multiple `nodeSelectorTerms` (ORed) vs `matchExpressions` in one term (ANDed).

**`didn't match PersistentVolume's node affinity`**
The pod's bound PV has `spec.nodeAffinity` (the zone of a zonal disk, or a local PV's node) and
no schedulable node in that zone/node satisfies everything else.
```bash
kubectl get pv $(kubectl get pvc <claim> -o jsonpath='{.spec.volumeName}') -o jsonpath='{.spec.nodeAffinity}'
kubectl get nodes -L topology.kubernetes.io/zone
```
Fix: capacity in that zone (node group lost the AZ, or Karpenter NodePool excludes it), remove
conflicting affinity, or for new PVCs use `volumeBindingMode: WaitForFirstConsumer`, which delays
binding and provisioning until a pod using the claim exists, so the volume matches the pod's
scheduling constraints. Restoring from a snapshot in another zone is the data-moving fix.

**`Insufficient cpu/memory`** — requests vs allocatable; autoscaler should react (check its
events: a `NotTriggerScaleUp` event from cluster-autoscaler says why it did not add a node).
**`didn't match pod anti-affinity rules`** / **`didn't match pod topology spread constraints`** —
a required anti-affinity or a `DoNotSchedule` spread leaves no eligible node.
**`node(s) didn't have free ports for the requested pod ports`** — hostPort clash.

## Preemption line
`Preemption is not helpful for scheduling` means the failing filter result cannot be resolved by
evicting pods (the scheduler marks such nodes unschedulable-and-unresolvable, for example for an
untolerated taint), so don't chase priority.

## Verify
- [ ] After the fix, `kubectl get events --field-selector involvedObject.name=<p>` shows `Scheduled`.

## Checked
2026-10-23, against the Kubernetes website pages for node assignment (nodeSelectorTerms ORed, matchExpressions ANDed), taints, storage-class volume binding mode, the cluster-autoscaler FAQ (NotTriggerScaleUp event), and kube-scheduler plugin source on the main branch for the message strings (taint, node affinity, PV node affinity, free ports, spread, anti-affinity, "Preemption is not helpful for scheduling"). Older releases word some messages differently.
Method: documentation only; no commands were run.
