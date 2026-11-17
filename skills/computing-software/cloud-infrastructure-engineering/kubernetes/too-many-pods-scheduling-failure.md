---
id: computing-software.cloud-infrastructure-engineering.kubernetes.too-many-pods-scheduling-failure
name: too-many-pods-scheduling-failure
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pending, too-many-pods, failedscheduling, maxpods]
level: practitioner
status: docs-checked
description: "Resolve Pending pods with 'Too many pods': per-node maxPods, CNI IP limits, DaemonSet overhead, and fixes via node sizing, maxPods or autoscaling."
sources: ["https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/", "https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Too many pods

## Symptom
```
0/6 nodes are available: 6 Too many pods. preemption: 0/6 nodes are available: 6 No preemption victims found for incoming pod.
```
Each node's `allocatable.pods` is full, even if CPU and memory are free.

## Check
```bash
kubectl get nodes -o custom-columns=NODE:.metadata.name,MAX:.status.allocatable.pods
kubectl get pods -A -o wide     # count the pods per NODE column
```

## Causes
- Small nodes with a low pod cap: the kubelet `maxPods` setting and the CNI or cloud pool limits set
  `allocatable.pods`; look up the default for your provider and node size in its documentation.
- DaemonSet overhead: every per-node agent consumes one pod slot on every node.

## Fixes
| Fix | Notes |
|---|---|
| raise `maxPods` (kubelet) | within pod CIDR and CNI IP limits; see kubelet maxPods sizing |
| IP-limited CNIs (for example the AWS VPC CNI) | the per-node pod limit may come from the CNI, not only `maxPods`; check the CNI documentation |
| bigger instance types | more ENIs/IPs and amortised DaemonSet overhead |
| cluster autoscaler / Karpenter | may add nodes; check that they know your per-node pod limit |
| consolidate DaemonSets | fewer agents per node |

Check whether your autoscaler reacts to the "Too many pods" reason; if nothing happens, check the
node group maximum size.

## Verify
After the fix, `kubectl get pods -A --field-selector=status.phase=Pending` shrinks and
`kubectl describe node` shows pod count under allocatable.

## Checked
2026-10-23, against the kube-scheduler source on the main branch (the exact reasons "Too many pods", and "No preemption victims found for incoming pod" in the preemption line). Vendor pod-per-node numbers (EKS, AKS, GKE, prefix delegation) and the Terminating-pod counting claim were removed as unconfirmed.
Method: documentation only; no commands were run.
