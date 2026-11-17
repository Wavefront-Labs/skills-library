---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-threat-model-aws-iam-and-tag-controls
name: karpenter-threat-model-aws-iam-and-tag-controls
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [threat-model, iam, tags, passrole, instance-profile, ami-owner, security]
level: advanced
status: docs-checked
description: "AWS-specific Karpenter threats and mitigations: tag-based IAM on CreateTags, iam:PassRole role enumeration, instance profile ownership tags, instance scoping and AMI owner filter."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/threat-model.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter AWS threats: IAM and tag controls

Tag orchestration: Karpenter maps EC2 instances to NodeClaims using tags `karpenter.sh/managed-by`, `karpenter.sh/nodepool` and `kubernetes.io/cluster/${CLUSTER_NAME}`. It also drifts on subnet and security group changes. Anyone who can create or delete tags on instances (`i-*`), subnets or security groups can therefore make Karpenter create or delete instances. Mitigation: tag-based IAM conditions on `ec2:CreateTags` / `ec2:DeleteTags` for those resources.

Wrong node role: many roles trust the EC2 service. Enumerate the allowed node roles in the Resource section of Karpenter's `iam:PassRole` statement. If `spec.role` in an EC2NodeClass is not enumerated, instance profile generation fails.

Instance profile ownership: Karpenter may only create, tag, modify and delete instance profiles that carry these tags matching the cluster: `karpenter.sh/managed-by`, `kubernetes.io/cluster/${CLUSTER_NAME}`, `karpenter.k8s.aws/ec2nodeclass`, `topology.kubernetes.io/region`.

Instances outside the cluster: IAM conditions require the `karpenter.sh/nodepool` tag and the cluster tag on instances Karpenter terminates. After creation, only the `Name` and `karpenter.sh/nodeclaim` tags are modifiable on instances, and `aws:ResourceTag` conditions restrict even that to Karpenter-owned instances.

Unintended AMI: when selecting AMIs by name or tags, Karpenter adds an owner filter of `self,amazon`, so a public look-alike AMI from another account is ignored.

## Checked

2026-11-04. Confirmed against the Threat model reference (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
