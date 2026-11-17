---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-deletion-cost-scale-down
name: pod-deletion-cost-scale-down
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, replicaset, pod-deletion-cost, scale-down, reconciliation]
level: practitioner
status: docs-checked
description: "Influence which pods a ReplicaSet removes on scale-down with the controller.kubernetes.io/pod-deletion-cost annotation, and the default victim ordering."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/#pod-deletion-cost", "https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/#scaling-a-replicaset", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod deletion cost

## Default victim order when a ReplicaSet scales down
1. Pending (and unschedulable) pods first.
2. Pods with a lower `controller.kubernetes.io/pod-deletion-cost` first.
3. Pods on nodes with more replicas of this ReplicaSet first.
4. Pods created more recently first (creation times are bucketed on an integer log scale).
If all of these match, the choice is random.

## The annotation (beta since 1.22, on by default)
```bash
kubectl annotate pod web-7d9c-abcde controller.kubernetes.io/pod-deletion-cost=-100 --overwrite
kubectl scale deployment/web --replicas=4       # that pod is removed first
```
The value is an integer in [-2147483648, 2147483647]; pods that do not set it count as 0 and
negative values are allowed; invalid values are rejected by the API server. Lower is deleted first.
The `PodDeletionCost` feature gate (beta, on by default) is on kube-apiserver and kube-controller-manager.

## Uses
- Remove pods with the lowest utilisation: the docs suggest an application that controls its own
  scale-down (for example a Spark driver) sets the annotation once, proportional to utilisation,
  just before issuing the scale-down.
- Give pods that must survive (for example a leader) a high cost.

## Caveats
- Honoured on a best-effort basis: no guarantee about deletion order. It is a ReplicaSet
  scale-down preference.
- Avoid updating the annotation frequently (for example from a metric value): each update is a pod
  update on the API server.
- The Deployment's HPA chooses how many, not which; this annotation chooses which.

## Verify
```bash
kubectl get pods -l app=web -o custom-columns=POD:.metadata.name,COST:.metadata.annotations.controller\\.kubernetes\\.io/pod-deletion-cost
```

## Checked

Checked 2026-10-24 against the ReplicaSet concepts page in Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24), and the PodDeletionCost feature gate source (beta from 1.22, still beta, default true).
- Scale-down ordering (pending first, deletion cost, nodes with more replicas, recency in log buckets, then random), value range and default 0, best-effort note, and the advice not to update frequently: ReplicaSet page.

Method: documentation only; no commands were run.
