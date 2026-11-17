---
id: computing-software.cloud-infrastructure-engineering.kubernetes.statefulset-rolling-update-maxunavailable
name: statefulset-rolling-update-maxunavailable
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, statefulset, statefulset-maxunavailable, rollingupdate, partition]
level: practitioner
status: docs-checked
description: "Speed up StatefulSet rollouts with rollingUpdate.maxUnavailable, feature gate status, interaction with podManagementPolicy and partition, and quorum safety."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#maximum-unavailable-pods", "https://github.com/kubernetes/enhancements/tree/master/keps/sig-apps/961-maxunavailable-for-statefulset"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# StatefulSet maxUnavailable

Default StatefulSet RollingUpdate replaces one pod at a time, highest ordinal first, waiting
for each to be Ready. For 50+ replica sets that is slow.

## Field
```yaml
spec:
  podManagementPolicy: Parallel
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 3        # int or percentage, default 1
      partition: 0
```
Status: beta (feature-state v1.35 in the docs). The `MaxUnavailableStatefulSet` gate was alpha
1.24-1.34; beta and on by default in 1.35.0-1.35.3, off by default in 1.35.4-1.36, and on by
default again from 1.37. Check the gate default for your exact patch release before relying on it.

## Semantics
- The value is an absolute number or a percentage of desired pods (percentages round up); it
  cannot be 0; default 1. Any unavailable pod in ordinals `0` to `replicas - 1` counts toward it.
- The docs describe the burst behaviour under `Parallel` pod management: with `maxUnavailable`
  above 1 the controller terminates and creates up to that many pods at once, so pods can become
  ready out of order.
- `partition` still applies: only ordinals >= partition are updated.
- `minReadySeconds` counts towards availability.

## Quorum safety
For Raft/Paxos systems (etcd, ZooKeeper, Kafka KRaft controllers) keep maxUnavailable below
quorum loss (a quorum of 5 members is 3, so at most 2, and preferably 1), plus a PDB with the same
limit so evictions do not stack on top of the rollout.

## Verify
```bash
kubectl rollout status sts big --watch
kubectl get pods -l app=big -L controller-revision-hash --sort-by=.metadata.name
```
Several pods updating at once, on a set with `podManagementPolicy: Parallel`, indicates the field is active.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the StatefulSet concept page: `maxUnavailable` under `updateStrategy.rollingUpdate`, absolute or percentage (rounded up), cannot be 0, default 1, counts unavailable pods in `0..replicas-1`, beta; bursting under `Parallel` with maxUnavailable above 1 may make pods ready out of order; `minReadySeconds` delays availability; partition semantics. Feature gate stages for MaxUnavailableStatefulSet are from the feature-gates reference. The KEP directory exists in kubernetes/enhancements.
Removed: the claim that the field is accepted but ignored when the gate is off, and the claim that updates stay in reverse ordinal order.

Method: documentation only; no commands were run.
