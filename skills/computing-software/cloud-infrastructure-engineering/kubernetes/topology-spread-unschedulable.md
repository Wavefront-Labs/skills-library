---
id: computing-software.cloud-infrastructure-engineering.kubernetes.topology-spread-unschedulable
name: topology-spread-unschedulable
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshooting-scheduling, spread-constraint-unschedulable, topology-spread-constraints, failedscheduling, maxskew]
level: practitioner
status: docs-checked
description: "Fix pods left Pending by topology spread constraints, covering skew maths, domains without eligible nodes, old replicas in the count and whenUnsatisfiable choices."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/", "https://kubernetes.io/docs/reference/scheduling/config/#scheduling-plugins"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Topology spread constraints blocking scheduling

## The message
```
0/9 nodes are available: 3 node(s) didn't match pod topology spread constraints,
6 node(s) didn't match Pod's node affinity/selector.
```

## Work out the skew
Skew for a domain = matching pods in it minus the global minimum (the minimum across eligible domains, or
zero if there are fewer eligible domains than `minDomains`). With
`maxSkew: 1` and `whenUnsatisfiable: DoNotSchedule`, a pod can only go to a domain that keeps
skew at or below 1.
```bash
kubectl get pods -l app=web -o wide      # NODE column per pod
kubectl get nodes -L topology.kubernetes.io/zone
```

## Common causes
| Cause | Fix |
|---|---|
| one zone has no free capacity, so the other zones cannot get more pods either | add capacity in that zone; or `whenUnsatisfiable: ScheduleAnyway` |
| `labelSelector` also matches old ReplicaSet pods during a rollout | `matchLabelKeys: [pod-template-hash]` |
| nodes missing a constraint's `topologyKey` label are bypassed (and their pods do not count) | label all nodes, or accept it |
| `minDomains` (valid only with `DoNotSchedule`) higher than the eligible zones, so the global minimum is treated as 0 | lower it, or add zones |
| tainted nodes the pod cannot use are still counted as domains (`nodeTaintsPolicy` null behaves as `Ignore`) | `nodeTaintsPolicy: Honor` |

## Choosing whenUnsatisfiable
- `DoNotSchedule`: hard guarantee; pods stay Pending when a zone is short. Pair with cluster
  autoscaler node groups per zone.
- `ScheduleAnyway`: preference; spread is best effort.

## Verify
After the fix, `kubectl get pods -l app=web` shows all Running and the per-zone counts differ by
at most `maxSkew`.

## Checked
2026-10-23, against the Kubernetes website pod topology spread constraints page (global minimum and minDomains definition, implicit conventions about missing topologyKey labels, nodeTaintsPolicy semantics, whenUnsatisfiable) and the kube-scheduler podtopologyspread source (message "node(s) didn't match pod topology spread constraints").
Method: documentation only; no commands were run.
