---
id: computing-software.cloud-infrastructure-engineering.kubernetes.scheduling-gates-and-nodename
name: scheduling-gates-and-nodename
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, schedulinggates, scheduling-gates, nodename, manual-scheduling, kueue, cka]
level: practitioner
status: docs-checked
description: "Hold pods out of scheduling with schedulingGates until an external controller (quota, Kueue) releases them, and bypass the scheduler with spec.nodeName for manual placement."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/pod-scheduling-readiness/", "https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodename", "https://kueue.sigs.k8s.io/docs/overview/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# schedulingGates and nodeName

## schedulingGates (GA 1.30)
A pod with gates is created but the scheduler ignores it (`SchedulingGated` status) until
every gate is removed. Unlike Pending pods, gated pods don't trigger cluster-autoscaler
scale-up and don't churn the scheduler queue.
```yaml
apiVersion: v1
kind: Pod
metadata: {name: train-0}
spec:
  schedulingGates:
  - name: example.com/quota-check
  containers: [{name: c, image: <image>}]
```
```bash
kubectl get pod train-0            # STATUS SchedulingGated
kubectl patch pod train-0 --type=json -p='[{"op":"remove","path":"/spec/schedulingGates"}]'
```
Rules: gates can only be set when the pod is created; afterwards they can be removed in any order but
not added. While gated you may only tighten scheduling directives (nodeSelector additions only,
node affinity narrowed) — used by controllers to decide placement before release. Typical owners:
queueing and quota controllers such as Kueue, or custom admission of expensive workloads.
Metric: `scheduler_pending_pods{queue="gated"}`.

## nodeName: bypass the scheduler
```yaml
spec:
  nodeName: worker-3
```
The scheduler ignores the pod and the kubelet on `worker-3` tries to place it; `nodeName` overrules
`nodeSelector` and affinity. Because the scheduler is bypassed, the pod is bound even if the node has
`NoSchedule` taints; if the node also has a `NoExecute` taint the kubelet evicts the pod unless it
tolerates it. If the node lacks resources the pod is not rescheduled elsewhere.
Uses: scheduling without the scheduler, debugging when the scheduler is down. For normal pinning prefer
`nodeSelector: {kubernetes.io/hostname: worker-3}` (goes through the scheduler and fit checks).

## Gotchas
- A controller that never removes its gate leaves pods gated forever — alert on gated pod age.

## Verify
- [ ] Gated pods are released by their controller within the expected time; no long-lived `SchedulingGated` pods.

## Checked
2026-10-23, against the Kubernetes website pod scheduling readiness page (stable v1.30, SchedulingGated status, gates set only at creation and removable but not addable, nodeSelector additions only), assign-pod-node (nodeName bypasses scheduler) and taints (nodeName ignores NoSchedule, NoExecute evicts), plus the scheduler metrics source (scheduler_pending_pods, gated queue). The OutOfcpu reasons, the ResourceQuota-counting claim and the nodeName immutability note were removed as unconfirmed.
Method: documentation only; no commands were run.
