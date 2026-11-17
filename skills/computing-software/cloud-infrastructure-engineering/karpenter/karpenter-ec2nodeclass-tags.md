---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-tags
name: karpenter-ec2nodeclass-tags
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [tags, ec2nodeclass, resource-tagging, restricted-tags, nodeclaim]
level: practitioner
status: docs-checked
description: "Default tags Karpenter puts on EC2 instances, volumes and launch templates, merging extra spec.tags, and which tag domains cannot be overridden."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass tags

Karpenter tags EC2 instances, EBS volumes and launch templates with:

```yaml
Name: <node-name>
karpenter.sh/nodeclaim: <nodeclaim-name>
karpenter.sh/nodepool: <nodepool-name>
karpenter.k8s.aws/ec2nodeclass: <ec2nodeclass-name>
kubernetes.io/cluster/<cluster-name>: owned
eks:eks-cluster-name: <cluster-name>
```

Add your own with optional `spec.tags`; they merge with the defaults.

```yaml
spec:
  tags:
    InternalAccountingTag: 1234
    dev.corp.net/app: Calculator
    dev.corp.net/team: MyTeam
```

Rules:
- You may override the default `Name` tag.
- Overrides to restricted domains are not allowed: `karpenter.sh`, `karpenter.k8s.aws`, `kubernetes.io/cluster`.
- Not stated by the page: tag count or length limits, and how the tags relate to cost allocation or IAM conditions. Check AWS tagging docs for those.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 nodeclasses.md page; removed claims about Cost Explorer, IAM conditions, orphan detection, auto-discovery of owned nodes and quoting numeric values as not in the page. Default tag list and restricted domains unchanged.
