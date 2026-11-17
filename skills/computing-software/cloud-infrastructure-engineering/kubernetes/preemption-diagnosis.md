---
id: computing-software.cloud-infrastructure-engineering.kubernetes.preemption-diagnosis
name: preemption-diagnosis
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, preemption, nominatednodename, preempted, priorityclass, disruptiontarget, scheduler-events]
level: advanced
status: docs-checked
description: "Work out which pods were preempted, by whom and why: Preempted events, nominatedNodeName, DisruptionTarget conditions and scheduler metrics, and how to stop unwanted preemption."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#preemption", "https://kubernetes.io/docs/concepts/workloads/pods/disruptions/#pod-disruption-conditions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing preemption

## How it unfolds
1. A higher-priority pod P can't fit (`FailedScheduling`).
2. PostFilter (DefaultPreemption) finds a node where evicting lower-priority victims makes room;
   it tries to pick victims whose PDBs are not violated but will violate them if it must.
3. Victims get a graceful delete (their termination grace period) and condition
   `DisruptionTarget` with reason `PreemptionByScheduler`; P gets `status.nominatedNodeName`.
4. When victims are gone, P is scheduled — possibly on a different node if one freed up.

## Evidence
```bash
# victims
kubectl get events -A --field-selector reason=Preempted
#   message form in current source: "Preempted by pod <uid> on node <node>"
kubectl get pod <victim> -o jsonpath='{.status.conditions[?(@.type=="DisruptionTarget")]}'
# preemptor
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,POD:.metadata.name,NOMINATED:.status.nominatedNodeName
kubectl describe pod <preemptor>
```
Prometheus: `scheduler_preemption_attempts_total`, `scheduler_preemption_victims` (histogram).

## Why did *that* pod get preempted?
- It had lower priority (check `.spec.priority`, not just the class name; pods created before
  a `globalDefault` existed have 0).
- Its PDB couldn't prevent it — preemption only *prefers* not violating PDBs.
- `nominatedNodeName` and the final `nodeName` can differ: if another node frees up while victims
  terminate, P may land there (documented behaviour).

## Stopping unwanted preemption
- Give the workload a proper class; set `globalDefault` so nothing is 0.
- Use `preemptionPolicy: Never` for classes that should queue, not evict (batch).
- Restrict who can use high classes (ResourceQuota PriorityClass scope with `limitedResources`, or admission policy).
- Add capacity headroom (overprovisioning pods at negative priority get preempted first —
  that's their job).
- Victims' graceful termination period delays the preemptor; that's expected.

## Verify
- [ ] Preempted events correlate only with intended class pairs (e.g. platform over batch).

## Checked
2026-10-23, against the Kubernetes website pod priority and preemption page (nominatedNodeName behaviour, PDB best effort, graceful termination, existing pods keep priority when a globalDefault class is added), the Pod disruptions page (DisruptionTarget condition, reason PreemptionByScheduler), and the scheduler source (Preempted event message, metric names). The audit-log tip and the newer-versions message form were removed as unconfirmed.
Method: documentation only; no commands were run.
