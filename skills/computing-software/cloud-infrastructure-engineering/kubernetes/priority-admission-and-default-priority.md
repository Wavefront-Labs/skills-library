---
id: computing-software.cloud-infrastructure-engineering.kubernetes.priority-admission-and-default-priority
name: priority-admission-and-default-priority
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, priorityclass, priority-admission, globaldefault, preemption, admission-control]
level: practitioner
status: docs-checked
description: "Understand how the Priority admission plugin resolves priorityClassName into spec.priority, how globalDefault works and why manually set priorities are rejected."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#priority"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Priority admission

The `Priority` admission plugin (on by default) runs on pod create:
1. If `priorityClassName` is set, it looks up the PriorityClass and writes `spec.priority` and
   `spec.preemptionPolicy`. Unknown class: the pod is rejected.
2. If not set, it uses the class with `globalDefault: true`; if none exists, priority is 0.
3. If the pod already has `spec.priority` that disagrees with the class, it is rejected.

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata: {name: default-workload}
value: 1000
globalDefault: true
preemptionPolicy: PreemptLowerPriority
description: "Default for pods without a class"
```

## Rules worth knowing
- Only one class may have `globalDefault: true`.
- Changing a class's value does not change existing pods; priority is copied at admission.
- Deleting a class does not affect running pods, but new pods referencing it are rejected (and
  controllers stop creating replicas).
- Values above 1,000,000,000 are reserved for `system-cluster-critical` (2000000000) and
  `system-node-critical` (2000001000).
- `preemptionPolicy: Never` keeps queue position by priority without evicting others.

## Verify
```bash
kubectl get priorityclass
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,CLASS:.spec.priorityClassName,PRIO:.spec.priority | sort -k4 -n | tail
```

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and the kubernetes/kubernetes Priority admission plugin source.
Confirmed with no change needed: `Priority` plugin in the default list; lookup by `priorityClassName`, unknown class rejected;
`spec.priority` and `spec.preemptionPolicy` populated from the class and a conflicting value rejected (admission.go); only one
`globalDefault` class and the default priority of 0 without one; adding or deleting a class leaves existing pods unchanged and new
pods using a deleted class cannot be created; user class values up to 1000000000, `system-cluster-critical` 2000000000 and
`system-node-critical` 2000001000; `preemptionPolicy` default `PreemptLowerPriority` and `Never` semantics.
Method: documentation only; no commands were run.
