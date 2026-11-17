---
id: computing-software.cloud-infrastructure-engineering.kubernetes.daemonset-missing-pod-troubleshooting
name: daemonset-missing-pod-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, daemonset, daemonset-troubleshooting, pods-desired-vs-current, taints, node-affinity, misscheduled]
level: practitioner
status: docs-checked
description: "Find why a DaemonSet has fewer pods than nodes: DESIRED vs CURRENT vs READY, taints, nodeSelector/affinity, resource fit, stuck rollouts and misscheduled pods."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/", "https://kubernetes.io/docs/tasks/manage-daemon/update-daemon-set/", "https://github.com/kubernetes/kubernetes/blob/v1.37.1/pkg/scheduler/framework/plugins/nodeports/node_ports.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DaemonSet pod missing on a node

## Read the counters
```bash
kubectl get ds -n logging fluent-bit
# DESIRED CURRENT READY UP-TO-DATE AVAILABLE NODE SELECTOR
kubectl get ds fluent-bit -n logging -o jsonpath='{.status}' | jq
```
| Gap | Meaning |
|---|---|
| DESIRED < node count | node excluded by nodeSelector/affinity/**untolerated taint** — by design or by mistake |
| CURRENT < DESIRED | pod could not be created/scheduled on some eligible node |
| READY < CURRENT | pods exist but crash/fail probes |
| UP-TO-DATE < DESIRED | rollout stalled |
| `numberMisscheduled` > 0 | pods on nodes that no longer qualify (labels/taints changed) |

## Which nodes lack a pod
```bash
comm -23 <(kubectl get nodes -o name | sed 's|node/||' | sort) \
         <(kubectl get pods -n logging -l app=fluent-bit -o jsonpath='{range .items[*]}{.spec.nodeName}{"\n"}{end}' | sort)
```
Then for one such node:
```bash
kubectl describe node <n> | grep -A5 Taints
kubectl get node <n> --show-labels
kubectl get events -n logging --field-selector involvedObject.kind=Pod | grep <n>
```

## Causes and fixes
- **Taint not tolerated** (GPU pools, control plane, spot, custom dedicated pools) → add the
  toleration (or `operator: Exists` for truly-everywhere agents).
- **Insufficient resources** on a full node → pod Pending `Insufficient cpu`; give the DS a
  PriorityClass that can preempt app pods, and keep requests small.
- **hostPort conflict** with another pod on that node → `node(s) didn't have free ports`.
- nodeSelector/affinity typo (`kubernetes.io/os: linux` on Windows nodes is intentional).
- Node `NotReady`/cordoned: DaemonSet pods automatically tolerate the `unschedulable`, `not-ready`
  and `unreachable` taints, so such nodes still get a pod; whether it becomes Ready depends on the node.
- **Rollout stalled**: `maxUnavailable: 1` and one updated pod crash-loops → rollout stops.
  Fix the image/config; `kubectl rollout status ds/fluent-bit` shows progress.
  `updateStrategy: OnDelete` means pods only update when you delete them.

## Gotchas
- DaemonSet pods are scheduled by the default scheduler with node affinity to the target node;
  "FailedScheduling" events are on the pod, not the DS.

## Verify
- [ ] DESIRED equals the number of nodes you intend; CURRENT = READY = UP-TO-DATE = DESIRED.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- DaemonSet pods are scheduled by the default scheduler with node affinity to the target node, may preempt other pods, and get
  automatic tolerations for `not-ready`, `unreachable`, `disk-pressure`, `memory-pressure`, `pid-pressure` and `unschedulable`
  taints: DaemonSet page.
- `OnDelete` and `maxUnavailable` update behaviour and troubleshooting section: update-daemon-set task page.
- Scheduler messages `node(s) didn't have free ports for the requested pod ports` and `Insufficient <resource>`: v1.37.1
  scheduler `node_ports.go` and `noderesources/fit.go`.
- Removed: the Karpenter / Cluster Autoscaler overhead remark, which none of the checked sources covers.

Method: documentation only; no commands were run.
