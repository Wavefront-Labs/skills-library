---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-scheduling-resource-requests-and-daemonsets
name: karpenter-scheduling-resource-requests-and-daemonsets
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [resource-requests, limits, daemonset-overhead, priorityclass, startup-taints, bin-packing]
level: practitioner
status: docs-checked
description: "How Karpenter sizes nodes: only requests count, DaemonSet overhead added for sizing but not reserved, and options (startup taints, PriorityClass) to guarantee DaemonSet capacity."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Resource requests and DaemonSet overhead

Instance selection math uses pod `requests` only; `limits` can be higher to allow oversubscription.

```yaml
resources:
  requests: {memory: "128Mi", cpu: "500m"}
  limits: {memory: "256Mi", cpu: "1000m"}
```

DaemonSet overhead: when sizing a node for pending pods, Karpenter adds the requests of every DaemonSet that would run on that node and chooses an instance big enough for the total. This is only for sizing: Karpenter does not reserve the capacity after the node joins and does not bind pods itself.

To make sure DaemonSet pods get their capacity:
- Use startup taints: workload pods stay off the node until an external agent removes them, so DaemonSets tolerating the taints schedule first.
- Give DaemonSet pods a high PriorityClass so kube-scheduler preempts lower-priority pods. This is best effort: equal or higher priority pods are never preempted, and PDBs are only honoured best effort.

Related kube-scheduler tuning: by default `NodeResourcesFit` uses `LeastAllocated`, which spreads pods, opposite to Karpenter's bin packing, and leaves nodes under-packed. Configure the `MostAllocated` scoring strategy (on EKS via advanced control plane configuration on Kubernetes 1.31+). Trade-off: scoring uses requests, so tightly packed nodes leave less room for pods whose limits exceed requests to burst, risking OOM kills or earlier CPU throttling.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. All claims matched the page; nothing changed.
