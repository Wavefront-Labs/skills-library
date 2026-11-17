---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-static-nodepool-replicas
name: karpenter-static-nodepool-replicas
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [static-capacity, replicas, nodepool, limits-nodes, kubectl-scale, fixed-size]
level: advanced
status: docs-checked
description: "Static NodePools via spec.replicas: fixed node count, constraints (limits.nodes only, no weight, no consolidation), scaling with kubectl scale, and per-AZ pinning."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodepools.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Static NodePools (spec.replicas)

Setting `spec.replicas` makes the NodePool maintain a fixed number of nodes regardless of pod demand.

Constraints:
- Cannot be removed once set; a NodePool cannot switch between static and dynamic.
- Only `limits.nodes` is allowed in `limits`.
- `weight` cannot be set.
- Nodes are not consolidated.
- Scale operations bypass node disruption budgets but respect PodDisruptionBudgets.

Requirements work as in dynamic pools but are evaluated once per NodeClaim at creation, so claims in the same static pool may get different instance types depending on availability, as long as compatible.

Scale with:

```bash
kubectl scale nodepool static-capacity --replicas=15
```

Example, pinned to one AZ (spread across zones by creating one static NodePool per AZ):

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: static-capacity
spec:
  replicas: 10
  template:
    spec:
      requirements:
      - key: node.kubernetes.io/instance-type
        operator: In
        values: ["m5.large", "m5.xlarge"]
      - key: topology.kubernetes.io/zone
        operator: In
        values: ["us-west-2a"]
  limits:
    nodes: 15   # maximum during scaling and drift
  disruption:
    budgets:
    - nodes: 20%   # drift replacement
```

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. All claims matched the page; nothing changed.
