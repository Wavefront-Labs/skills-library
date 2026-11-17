---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-sharing-with-resource-access-manager
name: vpc-sharing-with-resource-access-manager
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, shared-vpc, vpc-sharing, resource-access-manager, ram, multi-account, subnets]
level: practitioner
status: docs-checked
description: "Share VPC subnets across accounts with RAM: owner vs participant responsibilities, AZ ID mapping, security group referencing, quotas, billing and what participants cannot do."
sources: ["https://docs.aws.amazon.com/ram/latest/userguide/getting-started-sharing.html", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing.html", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-share-prerequisites.html", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing-share-subnet-working-with.html", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-share-limitations.html", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-share-billing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC sharing with Resource Access Manager

**Goal:** many workload accounts launch into a few centrally managed VPCs — fewer VPCs, NAT
gateways and TGW attachments — while keeping account-level isolation of resources and billing.

## 1. Share subnets
```bash
# once, in the management account
aws ram enable-sharing-with-aws-organization
# in the network (owner) account
aws ram create-resource-share --name prod-app-subnets \
  --resource-arns arn:aws:ec2:<REGION>:<NET_ACCOUNT>:subnet/subnet-a arn:aws:ec2:<REGION>:<NET_ACCOUNT>:subnet/subnet-b \
  --principals arn:aws:organizations::<MGMT_ACCOUNT>:ou/o-xxxx/ou-prod-xxxx \
  --no-allow-external-principals
```
Sharing to an OU makes new accounts in the OU participants automatically.

## 2. Who owns what
| Owner (network account) | Participant (workload account) |
|---|---|
| VPC, subnets, route tables, NACLs, peering, internet gateways, NAT gateways, VGW, TGW attachments, gateway and interface endpoints, Resolver endpoints | its own EC2 instances, databases, Lambda functions, network interfaces and **security groups** |
| can describe participants' ENIs and security groups but not modify them | can describe the shared subnets, route tables, NACLs and VPC, but cannot create, modify or delete them |
Participants pay for their own application resources and for inter-AZ, peering, internet gateway and Direct Connect data transfer; the owner pays hourly and data processing charges for NAT gateways,
virtual private gateways, transit gateways, PrivateLink and VPC endpoints, and for public IPv4 addresses used in the shared VPC. Allocate costs with tags or cost categories as needed.

## 3. AZ IDs, not names
`us-east-1a` maps to different physical AZs per account. Use AZ IDs (`use1-az1`) in
docs/IaC when talking about shared subnets: `aws ec2 describe-availability-zones --query 'AvailabilityZones[].[ZoneName,ZoneId]'`.

## 4. Security groups across participants
Security groups are per account, but a participant can create rules that reference security groups belonging to other participants or the owner as `account-number/security-group-id`.
The default SG of the VPC belongs to the owner, so participants cannot launch instances with it, and they cannot use the owner's or other participants' non-default groups unless those are shared with them.

## Gotchas
- Not every service supports shared subnets in participant accounts — check the
  "Limitations" list (e.g. some services cannot launch in shared subnets).
- The owner can unshare a subnet at any time; participants' existing resources keep running, but the owner cannot delete the subnet or VPC until participants delete their resources in it.
- All participants draw from the same subnet IP space — monitor free IPs per shared subnet. Participant-created VPC resources count against the participant's own VPC quotas.
- Participants can create, delete and describe flow logs only for network interfaces they own; the owner cannot describe or delete flow logs a participant created.
- Prerequisites: the accounts must be managed by AWS Organizations, resource sharing must be enabled from the management account, and subnets in a default VPC cannot be shared.

## Verify
- [ ] In a participant account, `aws ec2 describe-subnets` lists the shared subnets; launching an instance there succeeds.
- [ ] The participant cannot `create-route` in the shared route table (AccessDenied).
- [ ] Billing shows NAT, transit gateway and endpoint charges in the network account and instance charges in the participant.

## Checked

Checked 2026-10-27 against the Amazon VPC User Guide (share a subnet, prerequisites, working with shared subnets, responsibilities and permissions, billing and metering) and the botocore EC2 model.
- Owner and participant responsibilities, security group referencing as `account-number/security-group-id`, default security group ownership, flow log permissions and billing split confirmed.
- AZ names map independently per account and AZ IDs (for example `use1-az1`) are the consistent identifier, as the working-with-shared-subnets page states; prerequisites (Organizations, RAM sharing enabled, resource share) and the unshare behaviour confirmed.
- Corrected two claims: participants are not limited to seeing only their own resources (they can describe shared subnets, route tables, NACLs and the VPC), and an owner can unshare a subnet at any time.
- `aws ram enable-sharing-with-aws-organization` and automatic access for accounts added to a shared OU confirmed on the RAM guide.
- Removed the statement that all participants share the VPC ENI quota; the page says participant-created resources count against the participant account's quotas.

Method: documentation only; no commands were run.
