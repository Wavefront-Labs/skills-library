---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-weighted-nodepools-and-fallback
name: karpenter-weighted-nodepools-and-fallback
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [weight, nodepool, savings-plans, reserved-instances, fallback, default-arch, priority]
level: advanced
status: docs-checked
description: "Using spec.weight to prefer reserved-instance NodePools with limits, define cluster-wide default arch or capacity type, and why highest weight is not guaranteed."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/scheduling.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodepools.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Weighted NodePools: reserved capacity and defaults

Karpenter tries NodePools in order of `spec.weight` (higher first).

Savings Plans / Reserved Instances: create a high-weight NodePool pinned to the reserved instance types and cap it with `limits` to the amount you own; the generic pool takes the rest.

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata: {name: reserved-instance}
spec:
  weight: 50
  limits: {cpu: 100}
  template:
    spec:
      requirements:
      - {key: node.kubernetes.io/instance-type, operator: In, values: ["c4.large"]}
```

Cluster-wide defaults: pods with no selectors can land anywhere. Give the preferred default NodePool a higher weight (for example 50, `amd64`, spot and on-demand) and restrict it; the page's example `arm64-specific` NodePool has no weight and so ranks lower.

Caveat: highest weight is not guaranteed. Because of batching and bin packing, a pod that cannot use the top pool forces a node from a lower pool, and other pods from that batch may schedule onto it. Also, existing capacity may be used by kube-scheduler instead of provisioning from the weighted pool.

Weight cannot be set on static NodePools (`replicas`) and weight changes do not drift nodes.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Softened the claim that pods must select the lower-weight pool explicitly, which the page does not state; added NodePools and Disruption pages as sources for the static-pool and no-drift remarks.
