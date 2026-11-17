---
id: computing-software.cloud-infrastructure-engineering.kubernetes.priorityclass-tiers-design
name: priorityclass-tiers-design
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, priorityclass, system-cluster-critical, globaldefault, preemptionpolicy, non-preempting, preemption, scheduling]
level: practitioner
status: docs-checked
description: "Design a small PriorityClass ladder (platform, critical, default, batch, overprovisioning), set globalDefault, and use preemptionPolicy Never for batch."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/", "https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#non-preempting-priority-class"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PriorityClass tiers

Without PriorityClasses every pod has priority 0, so under pressure the scheduler cannot tell a
payment API from a nightly report. Keep the ladder short — 4-6 classes.

## A practical ladder
| Class | Value | preemptionPolicy | Who |
|---|---|---|---|
| `system-node-critical` (built-in) | 2000001000 | Preempt | CNI, CSI node, kube-proxy |
| `system-cluster-critical` (built-in) | 2000000000 | Preempt | CoreDNS, metrics-server, autoscaler |
| `platform` | 100000 | Preempt | ingress controllers, cert-manager, monitoring |
| `business-critical` | 10000 | Preempt | tier-1 apps |
| `default` (**globalDefault: true**) | 1000 | Preempt | everything unlabelled |
| `batch` | 100 | **Never** | jobs that may wait but shouldn't evict |
| `overprovisioning` | -10 | Never | placeholder pods for headroom |

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata: {name: default}
value: 1000
globalDefault: true
description: "Default for pods without priorityClassName"
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata: {name: batch}
value: 100
preemptionPolicy: Never
description: "Queued ahead of lower classes, never preempts"
```

## Rules
- Only one `globalDefault: true` class; it applies only to pods created **after** it exists and does
  not change the priority of existing pods. Without one, unlabelled pods get 0.
- `value` and `preemptionPolicy` are immutable (the API server rejects updates) — create a new class to change.
- `preemptionPolicy: Never` (stable since v1.24): the pod is queued ahead of lower-priority pods
  but cannot preempt others; it waits in the queue until resources free up.
- Priority also affects **kubelet eviction** order under node pressure: first whether usage exceeds
  requests, then priority, then usage relative to requests.
- Restrict high classes to namespaces with ResourceQuota `scopeSelector` on PriorityClass +
  `limitedResources` admission config, or a policy engine; otherwise anyone can claim
  `business-critical`.

## Gotchas
- Preemption ignores PDBs on a best-effort basis — it tries to respect them but will violate
  them if nothing else fits.
- Pods with very high priority and huge requests can cascade-evict many small pods. Pair
  high classes with right-sized requests.

## Verify
```bash
kubectl get priorityclass
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,POD:.metadata.name,PRIO:.spec.priority,CLASS:.spec.priorityClassName
```
- [ ] No production pod at priority 0; batch pods use the non-preempting class.

## Checked
2026-10-23, against the Kubernetes website pod priority and preemption page (built-in values 2000000000 and 2000001000, globalDefault rules, non-preempting class stable v1.24, PDB best effort, ResourceQuota PriorityClass scope), the node-pressure eviction page (eviction order), and the PriorityClass validation source (value and preemptionPolicy immutable). Example class values in the table are illustrative design choices, not defaults.
Method: documentation only; no commands were run.
