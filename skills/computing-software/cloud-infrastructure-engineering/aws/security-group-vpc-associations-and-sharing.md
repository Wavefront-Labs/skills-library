---
id: computing-software.cloud-infrastructure-engineering.aws.security-group-vpc-associations-and-sharing
name: security-group-vpc-associations-and-sharing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, security-groups, sg-vpc-association, shared-security-groups, vpc-sharing, ram]
level: advanced
status: docs-checked
description: "Reuse one security group across VPCs with security group VPC associations, and share security groups with participant accounts in a shared VPC."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/security-group-assoc.html", "https://docs.aws.amazon.com/vpc/latest/userguide/security-group-sharing.html", "https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security group VPC associations and shared security groups

## 1. Associate one SG with more VPCs (same Region)
```bash
aws ec2 associate-security-group-vpc --group-id sg-0abc --vpc-id vpc-0def
aws ec2 describe-security-group-vpc-associations --filters Name=group-id,Values=sg-0abc
aws ec2 disassociate-security-group-vpc --group-id sg-0abc --vpc-id vpc-0def
```
- Lets a central team maintain one baseline SG (for example "corp-admin-access") used in many VPCs.
- Rule changes apply everywhere the SG is associated.
- Requirements: you must own the VPC or have one of its subnets shared with you; the VPC and SG must be in the same
  Region; a default SG cannot be associated with another VPC and no SG can be associated with a default VPC. Services that
  support it include EC2, Auto Scaling, EKS, EFS, FSx, PrivateLink, Elastic Load Balancing (ALB, NLB), Route 53,
  CloudFormation and API Gateway REST APIs.
- Wait for the association status `associated` (check with `describe-security-group-vpc-associations`). You can disassociate
  only when no network interface in that VPC uses the SG, and an SG cannot be deleted while it is associated.

## 2. Share an SG in a shared VPC (VPC owner, same AWS Organization)
With VPC sharing, participant accounts launch into the owner's subnets. The owner can share SGs through AWS RAM. This works only
for accounts in the same Organization with resource sharing enabled; the sharing account must own both the VPC and the
SG; default SGs and SGs in a default VPC cannot be shared; participants cannot share SGs they create.
```bash
aws ram create-resource-share --name shared-sgs \
  --resource-arns arn:aws:ec2:<REGION>:<OWNER_ACCOUNT_ID>:security-group/sg-0abc \
  --principals <PARTICIPANT_ACCOUNT_ID>
```
- Participants can select the shared SG when launching instances in the shared subnet, and rule updates made by the owner
  apply to their resources. For custom IAM policies the sharer needs `ec2:PutResourcePolicy` and `ec2:DeleteResourcePolicy`
  (permission-only actions) as well as RAM permissions.
- Quota effect: if a participant puts any shared SG on an ENI, the lower of the owner's and participant's
  security-groups-per-interface quota applies to that ENI.
- Stop sharing with `aws ram delete-resource-share`: existing ENIs keep receiving rule updates and keep the SG, but participants can
  no longer associate it with new ENIs, and the owner cannot delete the SG until participants remove it from all ENIs.

## 3. When to use which
| Need | Use |
|---|---|
| Same baseline in many VPCs of one account | VPC association |
| Participants in a shared VPC need owner-managed SGs | RAM share |
| Common CIDR sets everywhere | managed prefix lists (shareable) |

## Verify
- [ ] An instance in the second VPC can be launched with the associated SG.
- [ ] A participant account can choose the shared SG when launching an instance in the shared subnet.

## Checked

Date: 2026-10-27. Sources: Amazon VPC User Guide pages "Associate security groups with multiple VPCs" and "Share security groups with AWS Organizations"; Amazon VPC quotas page (prefix list sharing).
Confirmed: associate-security-group-vpc, describe-security-group-vpc-associations and disassociate-security-group-vpc flow; same-Region, default-SG and default-VPC restrictions; owner must own both VPC and SG; same Organization and resource sharing enabled; RAM create-resource-share and delete-resource-share; unsharing behaviour; minimum-of-quotas rule.
Corrected: the VPC-association requirement is "VPC owner or shared subnet", not "same account"; RAM sharing is limited to the same Organization; participants' ability to edit the shared SG was not documented and was removed.
Removed: the claim that participants can reference owner SGs by ID without sharing.

Method: documentation only; no commands were run.
