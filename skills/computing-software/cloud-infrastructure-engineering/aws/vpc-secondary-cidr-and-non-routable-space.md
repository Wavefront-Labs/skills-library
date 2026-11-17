---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-secondary-cidr-and-non-routable-space
name: vpc-secondary-cidr-and-non-routable-space
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, secondary-cidr, non-routable-cidr, carrier-grade-nat, ip-exhaustion, eks, private-nat-gateway]
level: practitioner
status: docs-checked
description: "Extend an exhausted VPC with secondary CIDRs, use non-routable 100.64.0.0/10 space for pods and workers, and route it out through a private NAT gateway."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html", "https://docs.aws.amazon.com/vpc/latest/userguide/add-ipv4-cidr.html", "https://docs.aws.amazon.com/vpc/latest/userguide/subnet-route-tables.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html", "https://docs.aws.amazon.com/eks/latest/userguide/cni-custom-network.html", "https://docs.aws.amazon.com/eks/latest/userguide/cni-custom-network-tutorial.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secondary CIDRs and non-routable address space

**Goal:** more IPs for a VPC whose routable corporate allocation is too small (classic EKS
pod exhaustion) without asking the network team for another /16.

## 1. Rules for adding a CIDR
```bash
aws ec2 associate-vpc-cidr-block --vpc-id vpc-123 --cidr-block 100.64.0.0/16
aws ec2 describe-vpcs --vpc-ids vpc-123 --query 'Vpcs[0].CidrBlockAssociationSet'
```
- Up to 5 IPv4 CIDRs per VPC by default (adjustable up to 50); each block between /16 and /28.
- Must not overlap any CIDR already associated with the VPC, must not be the same as or larger than a destination range in
  any route of the VPC's route tables, and must not overlap the CIDRs of peered VPCs or of VPCs sharing a Direct Connect gateway.
- Association restrictions: if the VPC uses a 10.0.0.0/8 range you cannot add blocks from the other RFC 1918 ranges
  (172.16.0.0/12, 192.168.0.0/16), and vice versa; blocks from **100.64.0.0/10** are permitted alongside any RFC 1918
  range. 198.19.0.0/16 is restricted for VPCs that use RFC 1918 ranges. If any block is in 10.0.0.0/15 you cannot add one
  from 10.0.0.0/16. To combine an RFC 1918 CIDR with a non-RFC 1918 CIDR, the RFC 1918 CIDR must be the one the VPC was created with.
- Route tables contain a `local` route for each IPv4 CIDR block of the VPC.

## 2. The non-routable pattern
- Routable subnets (e.g. 10.20.0.0/22 from the corporate plan) hold load balancers, NAT
  gateways, TGW attachments.
- Non-routable subnets (100.64.0.0/16, reused identically in every VPC) hold EKS pods,
  batch workers.
- Outbound to on-prem/other VPCs: non-routable subnets route `0.0.0.0/0`/corporate ranges to a
  **private NAT gateway** in a routable subnet, which SNATs to its routable IP. Internet egress
  continues via public NAT.
- Never propagate 100.64.0.0/16 into the TGW route tables — it is duplicated everywhere.

## 3. EKS custom networking
Set `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true` on the `aws-node` DaemonSet and create one
`ENIConfig` per AZ pointing at the 100.64 subnet; pods get secondary-CIDR IPs, nodes keep
routable IPs. With custom networking, no addresses from the primary interface go to pods. Existing nodes must be cordoned and
drained and replaced to pick it up. The subnets and security groups must be in the same VPC as the node. Custom networking
cannot be used with an IPv6 cluster; EKS suggests an IPv6 cluster as the alternative when the only goal is relieving IPv4 exhaustion.

## Gotchas
- Confirm that nothing you must reach (on-premises or partner networks) already uses 100.64.0.0/10 before adopting it.
- Security groups/NACLs referencing CIDRs need the new range added.
- You cannot remove the primary CIDR, and removing a secondary one requires deleting all subnets in it first.

## Verify
- [ ] `describe-vpcs` shows the new association `associated`; route tables show the extra `local` route.
- [ ] An instance/pod in a 100.64 subnet reaches an on-prem host and the host sees the private NAT gateway's routable IP.
- [ ] TGW route tables contain no 100.64 routes.

## Checked

Date: 2026-10-27. Sources: Amazon VPC User Guide pages "VPC CIDR blocks" (restrictions table), "Add or remove a CIDR block from your VPC", "Subnet route tables" and "Scenarios for NAT gateways" (private NAT gateway and overlapping networks); Amazon EKS User Guide pages "Deploy Pods in alternate subnets with custom networking" and its tutorial.
Corrected: 198.19.0.0/16 cannot be added to a VPC that uses RFC 1918 ranges (the skill said it could be added to any VPC); the overlap rule now includes the route-destination condition; prefix delegation was removed as an unsupported alternative.
Confirmed: 5 IPv4 CIDRs by default up to 50; /16 to /28; 100.64.0.0/10 permitted; AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG on aws-node and one ENIConfig per subnet or AZ; drain nodes; private NAT gateway for overlapping networks via a routable subnet; primary CIDR cannot be removed.

Method: documentation only; no commands were run.
