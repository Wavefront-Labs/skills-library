---
id: computing-software.cloud-infrastructure-engineering.kubernetes.daemonset-per-node-overhead-sizing
name: daemonset-per-node-overhead-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, daemonsets, daemonset-overhead, node-allocatable, capacity-planning, resource-requests]
level: practitioner
status: docs-checked
description: "Measure the per-node resources reserved by DaemonSets, size their requests honestly and choose node sizes where that overhead stays a small fraction."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/", "https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/pod-metrics.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/concepts/scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DaemonSet per-node overhead

Every DaemonSet pod's requests count against each node's allocatable capacity (capacity minus
kube-reserved, system-reserved and the eviction threshold) before any workload lands. Logging,
metrics, CNI, CSI, security agents and mesh node proxies all add up; measure your own total.

## Measure it
```bash
kubectl describe node <node> | sed -n '/Non-terminated Pods/,/Allocated resources/p'
```
PromQL with kube-state-metrics:
```promql
sum by (node) (
  kube_pod_container_resource_requests{resource="cpu"}
  * on (namespace, pod) group_left() max by (namespace, pod) (kube_pod_owner{owner_kind="DaemonSet"})
)
/ on (node) kube_node_status_allocatable{resource="cpu"}
```
The kube-state-metrics docs recommend the scheduler's `kube_pod_resource_request` metric over
`kube_pod_container_resource_requests` where it is available because it is more precise.

## Size the requests
- Set requests from measured usage over a representative period rather than chart defaults;
  check what your chart sets.
- Size agents against usage on your densest nodes, since some agents grow with pod count.
- A high `priorityClassName` on DaemonSet pods (for example `system-node-critical`, value
  2000001000, reserved for critical system pods) lets the scheduler preempt lower-priority pods to
  make room for them; this is best-effort and PDBs are honoured only on a best-effort basis.

## Choose node sizes
Overhead is fixed per node, so on a 2 vCPU node 1 vCPU of agents is 50 %; on 16 vCPU it is
6 %. Many small nodes waste capacity. Karpenter adds the requests of every DaemonSet that would
run on a node when sizing it (it evaluates DaemonSets per NodePool, using labels and taints, not
per instance type), and Cluster Autoscaler assumes a new node will run all DaemonSet pods.

## Verify
DaemonSet requests stay within the overhead budget you set (for example 10 % of allocatable) on
the standard node type, and no DaemonSet pods are `Pending` on new nodes.

## Checked

Checked 2026-10-27. Documentation checked: Kubernetes website main tree (v1.38 dev; latest release v1.37) reserve-compute-resources and priority pages; kube-state-metrics docs (main) for metric and label names; Karpenter v1.15 scheduling and FAQ pages; Cluster Autoscaler FAQ (master). Confirmed: allocatable definition, metric names `kube_pod_container_resource_requests`, `kube_pod_owner` (`owner_kind`) and `kube_node_status_allocatable`, `system-node-critical` value, Karpenter DaemonSet overhead behaviour. Removed as unconfirmed: the 0.5-1.5 vCPU and 1-3 GiB typical overhead, claims about chart default values, and the IP waste remark.

Method: documentation only; no commands were run.
