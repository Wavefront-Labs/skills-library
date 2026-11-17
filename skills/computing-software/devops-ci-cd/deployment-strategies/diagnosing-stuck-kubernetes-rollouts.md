---
id: computing-software.devops-ci-cd.deployment-strategies.diagnosing-stuck-kubernetes-rollouts
name: diagnosing-stuck-kubernetes-rollouts
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, kubectl-rollout-status, rolling-update, progressdeadlineseconds]
level: practitioner
status: docs-checked
description: "Diagnose a Deployment rollout that never finishes: rollout status and conditions, ProgressDeadlineExceeded, pending/crashing new pods, PDBs, quotas and readiness failures."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#deployment-status", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing stuck rollouts

```bash
kubectl rollout status deploy/api -n prod                  # exits non-zero if the progress deadline is exceeded
kubectl describe deploy api -n prod | sed -n '/Conditions/,/Events/p'
kubectl get rs -n prod -l app=api                          # old and new ReplicaSets, desired/ready
kubectl get pods -n prod -l app=api -o wide
```
`Progressing=False reason=ProgressDeadlineExceeded` appears after `progressDeadlineSeconds`
Kubernetes takes no action on a stalled Deployment other than reporting that condition; it is not rolled back automatically.

## Causes by new-pod state
| New pods | Look at | Typical fix |
|---|---|---|
| Pending | `kubectl describe pod` events: Insufficient cpu, node affinity, PVC unbound | requests, autoscaler, zone of volume |
| ImagePullBackOff | events | tag/digest, pull secret |
| CrashLoopBackOff | `kubectl logs --previous` | config/secret missing, migration not run |
| Running, 0/1 Ready | readiness probe failures in events | probe path/port/timeout, dependency down |
| Not created at all | `kubectl describe rs` events: quota exceeded, admission webhook denied | ResourceQuota, policy |

Old pods not terminating: with `maxUnavailable: 0` and new pods never Ready, old pods are never removed.

## Recover
```bash
kubectl rollout undo deploy/api -n prod            # back to previous ReplicaSet
kubectl rollout pause deploy/api -n prod           # stop mid-way while investigating
```
In GitOps setups revert in Git instead, or Argo will reapply the broken spec.

## Verify
- [ ] Pipeline uses `rollout status` and fails on non-zero; new RS reaches desired Ready.

## Checked

2026-10-28. Confirmed against the Kubernetes Deployment page: the Progressing condition with reason ProgressDeadlineExceeded after `progressDeadlineSeconds`, that Kubernetes takes no action on a stalled Deployment beyond reporting it, `kubectl rollout status` returning non-zero after the deadline, `kubectl rollout undo` and `kubectl rollout pause`. Removed: the default value of 600, the `--timeout` flag and the PodDisruptionBudget claim.

Method: documentation only; no commands were run.
