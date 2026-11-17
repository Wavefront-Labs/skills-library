---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-block-public-access-and-exclusions
name: vpc-block-public-access-and-exclusions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, vpc-bpa-mode, bpa-exclusions, internet-gateway-block, declarative-policies, network-security]
level: practitioner
status: docs-checked
description: "Turn on VPC Block Public Access account-wide (bidirectional or ingress-only), carve exclusions for VPCs or subnets that must stay public, and verify with Reachability Analyzer."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/security-vpc-bpa.html", "https://docs.aws.amazon.com/vpc/latest/userguide/security-vpc-bpa-basics.html", "https://docs.aws.amazon.com/vpc/latest/userguide/security-vpc-bpa-assess-impact-main.html", "https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_declarative_syntax.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/create-vpc-block-public-access-exclusion.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC Block Public Access (BPA)

**What it does:** a regional, account-level switch that blocks traffic through internet
gateways and egress-only internet gateways for every VPC in the account, regardless of
route tables and security groups, except where you add exclusions.

## 1. Modes
- `block-bidirectional`: no traffic in or out via IGW/EIGW (NAT gateways in public subnets
  lose internet egress too, unless that subnet is excluded).
- `block-ingress`: blocks inbound initiated from the internet; outbound via NAT gateways
  and EIGW still works. This is the common choice for "no public endpoints except
  approved ones".
Off by default (`off`). Documented as blocked: internet gateways, egress-only internet gateways, NAT gateways,
internet-facing ALBs and NLBs, CloudFront VPC origins, Direct Connect public virtual interfaces, Global Accelerator
inbound traffic, Wavelength carrier gateways, and Gateway Load Balancer and Network Firewall endpoints unless their subnet is
excluded. Documented as not affected: Client VPN, Cloud WAN, Outposts local gateway, Site-to-Site VPN, transit gateways and
Verified Access. Private traffic to services inside the VPC (such as the Route 53 Resolver) is allowed. You must own the VPCs
and subnets to turn it on; in a shared VPC the owner's mode also applies to participants.

## 2. Enable
```bash
aws ec2 modify-vpc-block-public-access-options --region eu-west-1 \
  --internet-gateway-block-mode block-ingress
aws ec2 describe-vpc-block-public-access-options --region eu-west-1
```
Regional: repeat per Region. It can take a few minutes; the state goes `update-in-progress` to
`update-complete`. Ingress-only mode is not supported in Local Zones where NAT gateways and egress-only internet gateways are
not allowed.

## 3. Exclusions
Exclude a whole VPC or individual subnets, with their own direction:
```bash
aws ec2 create-vpc-block-public-access-exclusion --subnet-id subnet-0pub1 \
  --internet-gateway-exclusion-mode allow-bidirectional
aws ec2 create-vpc-block-public-access-exclusion --vpc-id vpc-0edge \
  --internet-gateway-exclusion-mode allow-egress
aws ec2 describe-vpc-block-public-access-exclusions
```
- `allow-bidirectional`: public ALBs/NLBs and NAT gateways in this subnet work normally.
- `allow-egress`: only outbound, and it applies only when the account mode is bidirectional (for NAT subnets).
- An exclusion on a VPC applies to all its subnets. You can create exclusions before turning BPA on to avoid disruption.
- Up to 50 exclusions per account per Region by default (adjustable through a support request). Tag them with owner and reason.
- If an internet-facing load balancer has even one excluded subnet, it can still receive public traffic and route it privately
  to targets in non-excluded subnets; exclude none of its subnets to fully block it. A workload subnet behind an appliance
  that uses VPC ingress routing must be excluded.
- Typical design: account in `block-ingress`; exclude only the public subnets that host
  the internet-facing load balancers. Instances with public IPs in other subnets become
  unreachable, which is the point.

## 4. Organization-wide
Enforce with an Organizations **declarative policy** for EC2 (attribute
`vpc_block_public_access`) so member admins cannot turn it off, optionally permitting
exclusions:
```json
{"ec2_attributes": {"vpc_block_public_access": {
   "internet_gateway_block": {"mode": {"@@assign": "block_ingress"},
     "exclusions_allowed": {"@@assign": "enabled"}}}}}
```
The policy can only set whether exclusions are allowed; exclusions themselves are still created in the account that owns the VPC.
When the policy is enabled the account shows "Managed by Declarative Policy" and its BPA settings cannot be changed locally.

## 5. Rollout safely
1. Inventory internet-facing resources first:
   `aws ec2 describe-network-interfaces --filters Name=association.public-ip,Values=*`
   and every internet-facing ELB.
2. Create exclusions for the subnets that must stay public.
3. Enable `block-ingress` in a non-prod account, run smoke tests.
4. Use the Network Access Analyzer template "Assess impact of VPC Block Public Access" before enabling (it lists paths to and from
   internet gateways; IPv6 egress-only gateway traffic is not covered and analyses are charged). Afterwards, Reachability
   Analyzer reports `Not reachable` with explanation code `VPC_BLOCK_PUBLIC_ACCESS_ENABLED`.
5. Create a flow log with a custom format that includes `reject-reason`: traffic rejected by BPA shows `BPA`. BPA flow records
   have no `bytes` and no skipped records. CloudTrail records exclusion deletions (resource type
   `AWS::EC2::VPCBlockPublicAccessExclusion`).

## Gotchas
- An existing public-IP instance outside an excluded subnet silently loses inbound access;
  SSH via public IP stops. Use SSM Session Manager.
- `block-bidirectional` breaks NAT egress for the whole account unless the NAT subnets are
  excluded with at least `allow-egress`.

## Verify
- [ ] `describe-vpc-block-public-access-options` shows the intended mode in every used region.
- [ ] Exclusions list contains only documented subnets; each tagged with owner and reason.
- [ ] Public ALB with its subnets excluded still serves; a test instance with a public IP elsewhere is unreachable from the internet.
- [ ] Declarative policy attached at the OU (if org-managed) and member attempts to disable fail.

## Checked

Date: 2026-10-27. Sources: Amazon VPC User Guide pages "Block public access to VPCs and subnets", "VPC BPA basics" and "Assess impact of VPC BPA and monitor VPC BPA"; Amazon VPC quotas page; AWS Organizations declarative policy syntax reference; AWS CLI 2.38.6 references for modify-vpc-block-public-access-options and create-vpc-block-public-access-exclusion; botocore EC2 model (state enums).
Corrected: CloudFront VPC origins are blocked by BPA (the skill said they keep working); Direct Connect public virtual interfaces are blocked; the not-affected list is Client VPN, Cloud WAN, Outposts local gateway, Site-to-Site VPN, transit gateways and Verified Access; allow-egress applies only in bidirectional mode.
Confirmed: modes off, block-bidirectional and block-ingress; exclusion modes allow-bidirectional and allow-egress; 50 exclusions; declarative policy attribute vpc_block_public_access with internet_gateway_block and exclusions_allowed; flow log reject-reason BPA; Reachability Analyzer code VPC_BLOCK_PUBLIC_ACCESS_ENABLED.
Removed: the statement that BPA never blocks VPC Lattice (not on the pages) and the "no SCP denial errors" remark.

Method: documentation only; no commands were run.
