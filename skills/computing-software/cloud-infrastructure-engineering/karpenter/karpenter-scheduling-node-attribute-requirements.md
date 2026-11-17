---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-scheduling-node-attribute-requirements
name: karpenter-scheduling-node-attribute-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [nvme, instance-local-nvme, network-bandwidth, node-attributes, exists-operator, workload-isolation, gte]
level: advanced
status: docs-checked
description: "Scheduling on node attributes: require local NVMe or minimum network bandwidth with Gte, the ephemeral-storage caveat, and Exists-operator team isolation on one NodePool."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scheduling on node attributes and Exists isolation

Use well-known labels at NodePool or workload level to get node properties Kubernetes cannot schedule on directly.

Any local NVMe, or at least 100 GiB:

```yaml
- key: karpenter.k8s.aws/instance-local-nvme
  operator: Exists          # or: Gte with values: ["100"]
```

At least 50 Gbps network:

```yaml
- key: karpenter.k8s.aws/instance-network-bandwidth
  operator: Gte
  values: ["50000"]
```

Caveat: Karpenter does not consider `ephemeral-storage` requests when scheduling; you are requesting node attributes and getting storage as a side effect. Tune CPU and memory for fit, especially with consolidation. The NodeClass must also support automatically formatting and mounting NVMe instance storage.

`Exists` for workload segregation: put a custom key on the NodePool and let each team supply the value; Karpenter stamps the value on nodes it launches, isolating teams without one NodePool each.

```yaml
requirements:
  - key: company.com/team
    operator: Exists
```

Deployments then set `nodeSelector: {company.com/team: team-a}` or `team-b`; their pods land on different nodes carrying the matching label.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Removed the instanceStorePolicy RAID0 detail, which the page does not state.
