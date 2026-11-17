---
id: computing-software.cloud-infrastructure-engineering.aws.security-group-referencing-and-prefix-lists
name: security-group-referencing-and-prefix-lists
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, security-groups, sg-referencing, security-group-reference, prefix-list, managed-prefix-list, prefix-lists, customer-managed-prefix-list]
level: practitioner
status: docs-checked
description: "Write security group rules by reference instead of CIDR: SG-to-SG rules, cross-VPC references over peering/TGW, AWS-managed and customer-managed prefix lists and their sizing."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html", "https://docs.aws.amazon.com/vpc/latest/userguide/managed-prefix-lists.html", "https://docs.aws.amazon.com/vpc/latest/tgw/tgw-vpc-attachments.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security group referencing and prefix lists

**Goal:** rules that describe *roles* ("app tier may reach DB tier") and *named ranges*
("office networks") so scaling, IP changes and new offices need no rule edits.

## 1. SG-to-SG references
```bash
aws ec2 authorize-security-group-ingress --group-id sg-db \
  --ip-permissions 'IpProtocol=tcp,FromPort=5432,ToPort=5432,UserIdGroupPairs=[{GroupId=sg-app,Description=app-tier}]'
```
- Matches traffic from instances associated with `sg-app` using their **private IP addresses**.
  No rules from the referenced group are copied into the referencing group.
- A rule referencing a group counts as one rule, however large the referenced group is.
- ALB → targets: reference the **ALB's** security group in the target SG.
- Referenced groups are not authorized: AuthorizeSecurityGroupIngress only checks that the group
  exists, so IAM policies naming the referenced group have no effect.

## 2. Cross-VPC references
- Inbound rules can reference a group in the same VPC, a peered VPC, or a VPC attached to the same
  transit gateway; outbound rules only the same VPC or a peered VPC.
- **Transit Gateway**: security group referencing works only if enabled on both the transit gateway
  and its VPC attachments. It is not supported across TGW peering, for PrivateLink endpoints, in
  attachments in AZ use1-az3, or on Outposts, Wavelength and some Local Zones; it does not work
  across a Gateway Load Balancer or Network Firewall inspection VPC.
- A rule is marked stale when the referenced group or the peering connection is deleted; list them with
  `aws ec2 describe-stale-security-groups --vpc-id <VPC_ID>`.

## 3. Prefix lists
AWS-managed lists cannot be created, modified, shared or deleted by you, and each has a weight:
```bash
aws ec2 describe-managed-prefix-lists
aws ec2 authorize-security-group-ingress --group-id sg-alb \
  --ip-permissions 'IpProtocol=tcp,FromPort=443,ToPort=443,PrefixListIds=[{PrefixListId=<PREFIX_LIST_ID>}]'
```
Customer-managed (office ranges, partner IPs):
```bash
aws ec2 create-managed-prefix-list --prefix-list-name offices --address-family IPv4 --max-entries 20 \
  --entries Cidr=203.0.113.0/24,Description=london Cidr=198.51.100.0/24,Description=nyc
aws ec2 modify-managed-prefix-list --prefix-list-id pl-abc --current-version 1 \
  --add-entries Cidr=192.0.2.0/24,Description=berlin
```
- A list holds IPv4 or IPv6 CIDRs, not both, and applies only to its Region.
- A customer-managed list counts against SG rule quotas as its **max-entries**, not its current size;
  an AWS-managed list counts as its weight. Set realistic `max-entries`.
- Share customer-managed lists with other accounts through RAM; update once and every SG and
  route table referencing it follows. Each change creates a new version, and referencing resources
  always use the latest.
- `modify-managed-prefix-list` takes `--current-version`; entries are added with `--add-entries`.

## Gotchas
- Egress rules default to allow-all; restricting egress with SG refs is good practice for DB tiers.
- A middlebox appliance between subnets needs the instance IP or subnet CIDR as source; a group
  reference does not allow that traffic.

## Verify
- [ ] Reachability Analyzer from app ENI to DB ENI on 5432: reachable; from another tier: not reachable.
- [ ] `describe-stale-security-groups` returns nothing.
- [ ] Adding an entry to the prefix list changes access in all referencing SGs without SG edits.

## Checked
2026-10-28. Confirmed against the VPC User Guide pages "Security group rules" (referencing rules, rule size counting, stale rules, default egress allow-all, middlebox limitation) and "Managed prefix lists" (single IP family, Region scope, max entries counting, versions, RAM, AWS-managed restrictions and weight), the Transit Gateway VPC attachments page (referencing prerequisites and limitations) and botocore ec2 (ModifyManagedPrefixList CurrentVersion, DescribeStaleSecurityGroups VpcId). Removed unconfirmed claims: AWS-managed list names and the CloudFront list weight, the peer-account sg reference format, same-Region limits, self-reference, shared VPC wording and the max-entries resize failure.
Method: documentation only; no commands were run.
