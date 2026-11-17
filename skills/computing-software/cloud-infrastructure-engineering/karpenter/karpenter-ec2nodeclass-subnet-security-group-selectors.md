---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-subnet-security-group-selectors
name: karpenter-ec2nodeclass-subnet-security-group-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [ec2nodeclass, subnetselectorterms, securitygroupselectorterms, discovery-tag, wildcard, or-and-terms]
level: practitioner
status: docs-checked
description: "EC2NodeClass subnet and security group selector terms: OR across terms, AND within a term, tag/id/name selection, wildcards, most-free-IP subnet pick, ALB controller SG pitfall."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass subnet and security group selectors

`subnetSelectorTerms` and `securityGroupSelectorTerms` are required. Terms in the array are ORed; conditions inside one term are ANDed.

```yaml
subnetSelectorTerms:
  - tags:
      karpenter.sh/discovery: "${CLUSTER_NAME}"
      environment: test
  - id: subnet-09fa4a0a8f233a921
securityGroupSelectorTerms:
  - tags:
      karpenter.sh/discovery: "${CLUSTER_NAME}"
  - name: my-security-group
  - id: sg-063d7acfb4b06c82c
```

- Tags may be any tag including `Name`; `*` wildcards work (`Name: "*Public*"`); `MyTag: '*'` or `''` matches any value of that key.
- Subnet choice: Karpenter picks a subnet matching the desired zone; if several exist in a zone, the one with the most available IPs. `status.subnets` lists resolved id and zone sorted by free IPs, descending.
- Security groups: all matching groups are attached. EKS creates at least two by default.

Pitfall: selecting security groups by `kubernetes.io/cluster/$CLUSTER_NAME` can match several groups, and the AWS Load Balancer Controller supports only one group with that tag key. Check:

```bash
aws ec2 describe-security-groups --filters Name=vpc-id,Values=$CLUSTER_VPC_ID Name=tag-key,Values=kubernetes.io/cluster/$CLUSTER_NAME --query 'SecurityGroups[].[GroupName]' --output text
```

If more than one name prints, prefer the `karpenter.sh/discovery: $CLUSTER_NAME` tag. Changing either selector causes drift.

## Checked

2026-11-04. Confirmed against the NodeClasses concept page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
