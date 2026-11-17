---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-conditions-and-readiness-gates
name: pod-conditions-and-readiness-gates
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pod-lifecycle, pod-conditions, readiness-gates, readinessgates, pod-phase, aws-load-balancer-controller]
level: practitioner
status: docs-checked
description: "Read pod phase vs conditions (PodScheduled, Initialized, ContainersReady, Ready, PodReadyToStartContainers) and use readinessGates so external systems gate pod readiness."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-conditions", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-readiness-gate", "https://github.com/kubernetes-sigs/aws-load-balancer-controller/blob/main/docs/deploy/pod_readiness_gate.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod conditions and readiness gates

## Phase is coarse; conditions are the truth
`status.phase`: Pending, Running, Succeeded, Failed, Unknown. A `Running` pod can be not
ready, and `kubectl get` STATUS column (CrashLoopBackOff, Init:0/1, Terminating) is computed
by kubectl, not a phase.

Conditions:
| Condition | True when |
|---|---|
| `PodScheduled` | bound to a node (False + reason `Unschedulable` = scheduling problem) |
| `PodReadyToStartContainers` (beta 1.29, stable 1.37) | sandbox and networking set up, volumes mounted (False = CNI/runtime issue) |
| `Initialized` | all init containers succeeded |
| `ContainersReady` | all containers ready (probes pass) |
| `Ready` | all containers ready **and** all `readinessGates` conditions True; the Pod should be added to load-balancing pools |

```bash
kubectl get pod p -o jsonpath='{range .status.conditions[*]}{.type}={.status} {.reason} {.lastTransitionTime}{"\n"}{end}'
kubectl wait pod -l app=web --for=condition=Ready --timeout=120s
```
Use the condition that failed to choose where to look: scheduler, CNI/runtime, init
containers, probes, or a gate.

## Readiness gates
Let an external controller decide part of readiness — e.g. "the cloud load balancer has
registered this pod IP and health-checks pass" — so rolling updates don't kill old pods before
the LB sends traffic to new ones.
```yaml
spec:
  readinessGates:
  - conditionType: "www.example.com/feature-1"   # name must be a valid label key
```
The controller writes a condition of that type into `status.conditions`. A missing condition counts as `False`, and the pod is not Ready until every gate is `True`. `kubectl get pod -o wide` shows a READINESS GATES column.

Example provider: the AWS Load Balancer Controller injects gates with the prefix
`target-health.elbv2.k8s.aws` through a mutating webhook, only at pod creation, for pods
selected by a Service or Ingress with `target-type: ip`. Label the namespace
`elbv2.k8s.aws/pod-readiness-gate-inject: enabled` and create the Ingress or Service before the pods.

## Gotchas
- If the controller that owns the gate is down or misconfigured, pods never become Ready and
  rollouts stall. Check `kubectl describe pod` and the pod `status.conditions`.
- `kubectl patch` does not support patching object status per the docs; set gate conditions with a PATCH from a client library.
- Readiness gates do not affect liveness/restarts; only endpoints and rollout availability.

## Verify
- [ ] During a rollout, new pods only become Ready after the LB target is healthy (no 5xx spike).

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the pod lifecycle page: condition list (PodScheduled, PodReadyToStartContainers, ContainersReady, Initialized, Ready); `readinessGates` conditions default to False when absent; a pod is ready only when all containers are ready and all gates are True; custom condition names must follow the label key format; `kubectl patch` cannot patch status; `PodReadyToStartContainers` is stable in 1.37 (beta 1.29). kubectl source has a priority-1 `Readiness Gates` column for pods. AWS gate prefix, namespace label, create-time injection and `target-type: ip` limit are from the aws-load-balancer-controller docs (pod_readiness_gate.md on GitHub).
Removed: GKE NEG gate name (not checked), a specific AWS conditionType value, and the progressDeadlineSeconds remark.

Method: documentation only; no commands were run.
