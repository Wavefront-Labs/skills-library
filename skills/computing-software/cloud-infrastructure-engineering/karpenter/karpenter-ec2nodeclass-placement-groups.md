---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-placement-groups
name: karpenter-ec2nodeclass-placement-groups
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [placementgroupselector, placement-group, cluster, partition, spread, efa, ec2nodeclass]
level: advanced
status: docs-checked
description: "placementGroupSelector: one placement group per EC2NodeClass by name or id, cluster/partition/spread strategies and limits, partition topology label, and required IAM actions."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass placementGroupSelector

Each EC2NodeClass maps to exactly one placement group; every instance it launches goes into it. Select by `name` or `id` (only one of them).

```yaml
spec:
  placementGroupSelector:
    name: my-pg-a        # or: id: pg-123
```

Strategies supported:
- Cluster: instances in one AZ on the same network segment for low latency and high throughput (for example EFA workloads).
- Partition: instances spread over isolated partitions (up to 7 per AZ) for hardware fault isolation. Pods can spread across partitions with `topologySpreadConstraints` on the label `karpenter.k8s.aws/placement-group-partition`.
- Spread: each instance on distinct hardware, up to 7 instances per AZ per group.

IAM for the Karpenter role: `ec2:DescribePlacementGroups` to discover groups, plus `ec2:RunInstances` and `ec2:CreateFleet` to launch into them.

Status: the `PlacementGroupReady` condition reports whether referenced placement groups were discovered. Because one NodeClass equals one group, use separate EC2NodeClasses (and NodePools) for workloads needing different groups.

## Checked

2026-11-04. Confirmed against the NodeClasses concept page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
