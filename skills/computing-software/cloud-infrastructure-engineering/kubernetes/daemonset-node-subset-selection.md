---
id: computing-software.cloud-infrastructure-engineering.kubernetes.daemonset-node-subset-selection
name: daemonset-node-subset-selection
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, daemonset, daemonset-node-selector, node-affinity, tolerations]
level: practitioner
status: docs-checked
description: "Run a DaemonSet only on a subset of nodes (GPU, edge, Linux) with nodeSelector or nodeAffinity, handle taints, and understand desired versus scheduled counts."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/#running-pods-on-select-nodes", "https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/#taints-and-tolerations", "https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DaemonSets on a node subset

## nodeSelector
```yaml
spec:
  template:
    spec:
      nodeSelector:
        kubernetes.io/os: linux
        example.com/gpu-node: "true"
      tolerations:
      - {key: example.com/gpu-node, operator: Exists, effect: NoSchedule}   # only if you taint those nodes
```
The DaemonSet controller creates pods on nodes that match `nodeSelector` (and, if set, `affinity`);
with neither set it creates pods on all nodes. DESIRED in `kubectl get ds` counts the nodes that should run the pod.

## nodeAffinity for richer rules
```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - {key: node-role.kubernetes.io/edge, operator: Exists}
        - {key: kubernetes.io/arch, operator: In, values: [amd64, arm64]}
```
The controller uses your node affinity to decide which nodes are eligible, then replaces the
affinity on each created pod with a `matchFields` term on `metadata.name` that pins the pod to its node.

## Label nodes
```bash
kubectl label node gpu-1 example.com/gpu-node=true
kubectl label node gpu-1 example.com/gpu-node-     # trailing dash removes the label
```
If node labels change, the DaemonSet promptly adds pods to newly matching nodes and deletes pods
from nodes that no longer match.

## Default tolerations the controller adds
`node.kubernetes.io/` keys `not-ready` and `unreachable` (NoExecute: pods on such nodes are not
evicted), `disk-pressure`, `memory-pressure`, `pid-pressure`, `unschedulable` (all NoSchedule), and
`network-unavailable` (NoSchedule, only for pods with `hostNetwork: true`).
Custom taints (GPU, dedicated pools, control plane) need explicit tolerations.

## Verify
```bash
kubectl get ds gpu-agent -o wide           # DESIRED vs CURRENT vs READY
kubectl get pods -l app=gpu-agent -o wide
kubectl get nodes -l example.com/gpu-node=true --no-headers | wc -l     # equals DESIRED
```

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the DaemonSet concept page: nodeSelector and affinity select eligible nodes, none means all nodes; the created pod's node affinity is replaced by a matchFields term on metadata.name; label changes add or delete pods promptly; the automatically added tolerations and their effects, including network-unavailable only for hostNetwork pods.
Removed: the claim that user affinity terms are ANDed with the matchFields term (the docs say the affinity is replaced on the created pod), and the NVIDIA label and taint key used in the example (a vendor label not checked here; example.com keys are placeholders).

Method: documentation only; no commands were run.
