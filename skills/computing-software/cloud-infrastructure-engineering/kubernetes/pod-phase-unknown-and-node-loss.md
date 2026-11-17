---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-phase-unknown-and-node-loss
name: pod-phase-unknown-and-node-loss
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pod-lifecycle, pod-phase-unknown, taint-based-eviction, node-not-ready]
level: practitioner
status: docs-checked
description: "What happens to pods when their node is lost: Unknown status, unreachable taints and tolerationSeconds, stuck Terminating pods, and safe recovery."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase", "https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#taint-based-evictions", "https://kubernetes.io/docs/concepts/cluster-administration/node-shutdown/#non-graceful-node-shutdown", "https://kubernetes.io/docs/tasks/run-application/force-delete-stateful-set-pod/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pods on a lost node

## Timeline
1. Kubelet stops renewing its Lease. After `node-monitor-grace-period` (kube-controller-manager
   flag; default 50 s) the node's Ready condition becomes `Unknown`.
2. The node lifecycle controller adds `node.kubernetes.io/unreachable:NoExecute` (or
   `not-ready`).
3. Pods have default tolerations for those taints with `tolerationSeconds: 300` (added by the
   DefaultTolerationSeconds admission plugin). After 5 minutes the controller deletes them.
4. The kubelet is unreachable, so deletion cannot complete: pods show `Terminating`, and the
   pod `phase` can read `Unknown` because the control plane cannot get the pod's state from the
   node. ReplicaSets and other workload resources no longer treat a terminating pod as an
   in-service replica, so replacements are created elsewhere.
5. StatefulSet pods are NOT replaced: the controller waits for the old pod to be gone to
   preserve at-most-one identity. Volumes with RWO attachments stay attached.

## Recovery
```bash
kubectl get nodes; kubectl describe node <n> | grep -A5 Taints
kubectl get pods -A -o wide --field-selector spec.nodeName=<n>
```
- Node comes back: kubelet finishes deletions, things converge on their own.
- Node is gone for good: confirm it is powered off (fencing), then either
  `kubectl delete node <n>` or add the out-of-service taint (non-graceful node shutdown, GA in
  v1.28) so stateful pods and volumes move:
  ```bash
  kubectl taint nodes <n> node.kubernetes.io/out-of-service=nodeshutdown:NoExecute
  ```
- Force deleting individual pods (`--grace-period=0 --force`) is a last resort; the API server
  does not wait for the kubelet to confirm, so a pod on a partitioned but live node keeps running.
- Remove the out-of-service taint yourself once the pods have moved and the node is recovered.

## Tuning
Shorter failover for stateless apps:
```yaml
tolerations:
- {key: node.kubernetes.io/unreachable, operator: Exists, effect: NoExecute, tolerationSeconds: 30}
- {key: node.kubernetes.io/not-ready, operator: Exists, effect: NoExecute, tolerationSeconds: 30}
```
Too short causes churn on brief network blips.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- `node-monitor-grace-period` default 50s and the 5 minute default before eviction: node-status page, node controller
  defaults in v1.37.1 source.
- DefaultTolerationSeconds adds 300s tolerations for not-ready and unreachable: admission plugin source v1.37.1.
- `Unknown` phase meaning, terminating pods no longer counted as in-service replicas, and the StatefulSet at-most-one rule:
  pod-lifecycle page and force-delete StatefulSet pod task.
- `node.kubernetes.io/out-of-service` taint (NoExecute or NoSchedule), manual removal, stable since v1.28: node-shutdown page and
  the `NodeOutOfServiceVolumeDetach` feature-gate page (stable 1.28, removed 1.31).
- Removed: nothing beyond the older-tooling remark.

Method: documentation only; no commands were run.
