---
id: computing-software.cloud-infrastructure-engineering.kubernetes.resourcequota-troubleshooting
name: resourcequota-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resourcequota, exceeded-quota, quota-troubleshooting, replicaset-events, failedcreate]
level: practitioner
status: docs-checked
description: "Diagnose quota failures where a Deployment shows fewer pods with no pod error: FailedCreate events on the ReplicaSet, exceeded-quota and missing-requests messages."
sources: ["https://kubernetes.io/docs/concepts/policy/resource-quotas/", "https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/policy/resourcequota-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ResourceQuota troubleshooting

## The silent symptom
`kubectl get deploy web` shows `READY 3/5` and there are only 3 pods — no Pending pod to
describe. Quota rejections happen at **pod creation**, so the error lives on the
**ReplicaSet** (or Job/StatefulSet/DaemonSet) events, not on a pod.
```bash
kubectl describe rs -l app=web -n team-a | grep -A5 Events
# Warning FailedCreate replicaset-controller Error creating: pods "web-7d9-abc" is forbidden:
#   exceeded quota: compute, requested: requests.memory=1Gi, used: requests.memory=19Gi, limited: requests.memory=20Gi
kubectl get events -n team-a --field-selector reason=FailedCreate
kubectl describe quota -n team-a
```
For Deployments the condition also shows:
`kubectl get deploy web -o jsonpath='{.status.conditions[?(@.type=="ReplicaFailure")].message}'`.

## Message → cause
| Message | Cause / fix |
|---|---|
| `exceeded quota: X, requested: ..., used: ..., limited: ...` | raise quota, shrink requests, or clean up (pods in a terminal phase, Succeeded or Failed, don't count) |
| `failed quota: X: must specify limits.cpu for: ...; requests.memory for: ...` | quota tracks those keys and the container lacks them → add a LimitRange with defaults |
| `exceeded quota ... count/jobs.batch` | CronJob history; lower history limits or `ttlSecondsAfterFinished` |
| `services.loadbalancers` exceeded | use Ingress/Gateway instead of more LBs |
| PVC `exceeded quota ... requests.storage` | expansion or new PVC over budget |

## Rolling updates and quota
With `maxSurge: 25%` the Deployment needs headroom for surge pods during rollout. A namespace
at 100% quota usage **cannot roll out** (new RS pods fail creation, old ones not removed with
`maxUnavailable: 0`). Keep ~25% quota headroom or use `maxSurge: 0, maxUnavailable: 1`.

## Stale usage
Quota `used` is recalculated by the controller; after deleting many objects it can lag
(`--resource-quota-sync-period`, default 5m). Usage that never decreases → objects stuck
Terminating (finalizers) still count.

## Verify
- [ ] Alert: `kube_resourcequota{type="used"} / ignoring(type) kube_resourcequota{type="hard"} > 0.85`.
- [ ] Rollouts in quota-limited namespaces succeed at current usage.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Messages `exceeded quota: <name>, requested: ..., used: ..., limited: ...` and `failed quota: <name>: must specify ...`:
  apiserver resource quota admission controller and pods evaluator source v1.37.1.
- Quota counts pods in a non-terminal phase only; compute quotas apply to non-terminal pods: resource-quotas page.
- `ReplicaFailure` condition with reason `FailedCreate` on Deployments: Deployment page.
- Deployment `maxSurge` default 25%: Deployment page.
- `--resource-quota-sync-period` default of 5 minutes (`ResourceQuotaSyncPeriod`): resource quota controller defaults source
  v1.37.1.
- `kube_resourcequota` with a `type` label: kube-state-metrics resourcequota metrics page.
- Removed: nothing beyond the Terminating-pods remark.

Method: documentation only; no commands were run.
