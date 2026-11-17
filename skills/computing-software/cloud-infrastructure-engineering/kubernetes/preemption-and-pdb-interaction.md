---
id: computing-software.cloud-infrastructure-engineering.kubernetes.preemption-and-pdb-interaction
name: preemption-and-pdb-interaction
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, preemption, preemption-pdb, pdb, priorityclass, graceful-termination]
level: practitioner
status: docs-checked
description: "How scheduler preemption treats PodDisruptionBudgets (best effort, may violate), graceful termination of victims, and designing priorities so preemption is safe."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#poddisruptionbudget-is-supported-but-not-guaranteed", "https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#graceful-termination-of-preemption-victims"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preemption and PDBs

## Key facts
- The scheduler tries to pick victims whose eviction does not violate PDBs, but if no such set
  exists it **preempts anyway**. PDB support in preemption is best effort, unlike the Eviction
  API used by `kubectl drain`, which strictly honours PDBs.
- Victims get their graceful termination period; the preemptor waits (pod shows
  `nominatedNodeName`) and may be scheduled elsewhere if something frees up first. The docs suggest a zero or small grace period on lower-priority pods to shorten the gap.
- Only lower-priority pods are victims. Pods with equal or higher priority are never preempted.
- If the pending pod has inter-pod affinity to lower-priority pods on a node, the scheduler does not
  preempt on that node and looks elsewhere, so it may stay pending. The docs recommend inter-pod
  affinity only towards equal or higher priority pods.

## Consequences
- A critical batch job with high priority can take down replicas of a service protected by a
  PDB. Put user-facing services at a priority at or above batch workloads.
- Long grace periods on victims delay the preemptor; a 10 min drain on victims means 10 min
  pending for the important pod.

## Design
| Tier | Example | preemptionPolicy |
|---|---|---|
| system-node-critical / system-cluster-critical | CNI, DNS | default (PreemptLowerPriority) |
| high | user-facing services | PreemptLowerPriority |
| default (globalDefault) | most workloads | PreemptLowerPriority |
| batch-high | important batch | `Never` (waits instead of evicting services) |
| low | best-effort batch, overprovisioning pause pods | n/a |

## Observe
```bash
kubectl get events -A --field-selector reason=Preempted
kubectl get pod <pending> -o jsonpath='{.status.nominatedNodeName}'
```
Metrics: `scheduler_preemption_victims` (histogram) and `scheduler_preemption_attempts_total`.

## Checked
2026-10-23, against the Kubernetes website pod priority and preemption page (PDB best effort, graceful termination of victims, inter-pod affinity limitation, nominatedNodeName) and the kube-scheduler metrics source (preemption_victims, preemption_attempts_total). The Preempted event reason is emitted by the scheduler preemption executor.
Method: documentation only; no commands were run.
