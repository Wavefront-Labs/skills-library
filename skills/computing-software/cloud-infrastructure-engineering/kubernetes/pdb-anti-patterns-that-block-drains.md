---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pdb-anti-patterns-that-block-drains
name: pdb-anti-patterns-that-block-drains
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, poddisruptionbudget, pdb-anti-patterns, blocked-drain, node-drain, unhealthypodevictionpolicy, cluster-upgrades]
level: practitioner
status: docs-checked
description: "Spot PDBs that block node drains forever (single replica, maxUnavailable 0, minAvailable equal to replicas, unhealthy pods) and fix them so upgrades and autoscaling proceed."
sources: ["https://kubernetes.io/docs/tasks/run-application/configure-pdb/", "https://kubernetes.io/docs/concepts/workloads/pods/disruptions/", "https://kubernetes.io/docs/tasks/run-application/configure-pdb/#unhealthy-pod-eviction-policy", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/kubectl/pkg/cmd/drain/drain.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PDB anti-patterns that block drains

Symptom: `kubectl drain` loops on
`error when evicting pods/"x" -n "y" (will retry after 5s): Cannot evict pod as it would violate the pod's disruption budget.`
Anything that drains nodes through the Eviction API (upgrades, node replacement) waits on the
blocked pod.

## Find the blockers
```bash
kubectl get pdb -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,MIN:.spec.minAvailable,MAXU:.spec.maxUnavailable,ALLOWED:.status.disruptionsAllowed,CUR:.status.currentHealthy,EXP:.status.expectedPods
```
`ALLOWED 0` in steady state = a drain blocker.

## Anti-patterns
| Pattern | Why it blocks | Fix |
|---|---|---|
| `minAvailable: 1` on a 1-replica Deployment | can never evict the only pod | 2+ replicas, or `maxUnavailable: 1`, or no PDB for singletons |
| `maxUnavailable: 0` | zero disruptions, ever | use 1 or a percentage |
| `minAvailable: 100%` / equal to replicas | same | `minAvailable: N-1` or `maxUnavailable: 1` |
| pods crash-looping / not Ready | unhealthy pods count against budget | `unhealthyPodEvictionPolicy: AlwaysAllow` (stable since 1.31) |
| PDB selector matches nothing / several workloads | confusing math, `expectedPods` wrong | one PDB per workload, exact selector |
| HPA at min=1 with PDB minAvailable 1 | same as singleton | minReplicas ≥ 2 for PDB-protected apps |
| StatefulSet quorum app with `maxUnavailable: 1` but one member already down | correct protection — fix the down member first | — |

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: {name: web}
spec:
  maxUnavailable: 1
  unhealthyPodEvictionPolicy: AlwaysAllow
  selector: {matchLabels: {app.kubernetes.io/name: web}}
```

## Policy
Enforce with Kyverno/Gatekeeper: deny PDBs with `maxUnavailable: 0` or `minAvailable` ≥ replicas;
require replicas ≥ 2 when a PDB exists. Communicate a "PDBs must allow ≥1 disruption" rule
before platform upgrades.

## Escape hatch (understand the risk)
`kubectl drain --disable-eviction` makes drain use delete even when eviction is supported, which
bypasses the PodDisruptionBudget check ("use with caution" in kubectl's own help). Use it only
after telling the owning team.

## Verify
- [ ] No PDB with `disruptionsAllowed == 0` while all its pods are healthy; test drain of a node completes.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (eviction and kubectl drain source, 2026-10-24). Confirmed: the drain error text `Cannot evict pod as it would violate the pod's disruption budget.` (source `eviction.go`; kubectl prints "will retry after"), zero-eviction configurations (`maxUnavailable` 0 or 0%, `minAvailable` 100% or the replica count) block drains, `unhealthyPodEvictionPolicy` semantics and its stable status from v1.31, `kubectl drain --disable-eviction` bypasses PDB checks, `ALLOWED DISRUPTIONS`/`currentHealthy`/`expectedPods` status fields. Removed as unconfirmed: the managed-service upgrade timeouts and the `jq` filter.

Method: documentation only; no commands were run.
