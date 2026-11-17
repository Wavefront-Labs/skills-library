---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-role-and-instance-profile
name: karpenter-ec2nodeclass-role-and-instance-profile
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [ec2nodeclass, role, instanceprofile, iam, private-cluster, node-role]
level: practitioner
status: docs-checked
description: "EC2NodeClass node identity: spec.role versus spec.instanceProfile, one is required, private clusters must use instanceProfile, and the generated profile in status."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass role and instanceProfile

You must specify one of `spec.role` or `spec.instanceProfile` for Karpenter to launch nodes. The page does not say what happens if both are set, so set only one.

```yaml
spec:
  role: "KarpenterNodeRole-${CLUSTER_NAME}"
  # or
  instanceProfile: "KarpenterNodeInstanceProfile-${CLUSTER_NAME}"
```

- `role`: Karpenter creates and manages an instance profile from the IAM role; the generated name appears in `status.instanceProfile` (example `${CLUSTER_NAME}-0123456778901234567789`).
- `instanceProfile`: a pre-provisioned profile that Karpenter does not manage; you are responsible for its contents.

Private clusters: a cluster without access to the regional IAM endpoint must use `spec.instanceProfile`, because Karpenter needs IAM access to manage a generated profile and the page states IAM does not support private endpoints.

Readiness: the `InstanceProfileReady` condition ("Instance Profile is discovered") feeds the top-level `Ready` condition, which also requires AMIs, subnets, security groups (and cluster CIDR on AL2023) to be discovered. NodePools referencing a NodeClass that is not Ready are not considered for scheduling.

Not in the page: IAM permissions required for the role, and the commands to create an instance profile.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 nodeclasses.md page; relaxed "exactly one" to the page's "one of", removed the getting-started and `aws iam` command details as not in the page, and added Ready condition detail.
