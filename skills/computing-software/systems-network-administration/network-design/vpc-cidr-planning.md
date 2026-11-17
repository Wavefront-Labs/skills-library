---
id: computing-software.systems-network-administration.network-design.vpc-cidr-planning
name: vpc-cidr-planning
category: computing-software
field: systems-network-administration
product: network-design
tags: [cloud-networking, vpc, vpc-cidr-planning, vnet, subnet-sizing, ipam, multi-account, aws-ipam]
level: practitioner
status: verified
description: "Plan cloud VPC/VNet address space: per-region and per-account blocks from a central pool, subnet tiers and AZ layout, reserved addresses, Kubernetes pod ranges, and growth."
sources:
  - https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html
  - https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-faq
  - https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC CIDR planning

Cloud VPCs are cheap to create and painful to renumber. Overlaps block peering and transit
attachments later.

## Carve hierarchically from one pool
Example 10.64.0.0/10 for cloud:
- per cloud/region: 10.64.0.0/14 aws-eu-west-1, 10.68.0.0/14 aws-us-east-1, 10.72.0.0/14 azure-westeurope
- per environment/account inside a region: /16 or /18 per VPC.
Record every allocation in IPAM (AWS VPC IPAM, NetBox) and make VPC creation pull from
it (Terraform: on `aws_vpc` set `ipv4_ipam_pool_id` with `ipv4_netmask_length` instead of `cidr_block`).

## Subnet layout inside a VPC
- One subnet per tier per AZ: public (load balancers, NAT), private app, data, and dedicated
  subnets for endpoints/firewalls/transit attachments (small /28s).
- Size app subnets generously: autoscaling groups, ENIs per pod, Lambda in VPC and managed services
  consume addresses.
- Reserved addresses: AWS reserves 5 per subnet (network, router, DNS, future, broadcast); Azure
  reserves 5; GCP reserves 4. A /28 gives 11 usable on AWS.
- AWS limits VPC CIDRs to /16-/28 (you can add secondary CIDRs); Azure VNets can hold multiple
  ranges; GCP can expand a subnet's primary range but never shrink or replace it.

## Kubernetes
EKS with the VPC CNI gives pods VPC IPs: a cluster of 200 nodes x 30 pods eats 6,000+ addresses.
Options: large dedicated subnets, prefix delegation (the VPC CNI hands out /28 prefixes), a secondary
VPC CIDR (AWS allows blocks from 100.64.0.0/10), or an overlay CNI.

## Avoid
- The same /16 in every VPC (guaranteed overlap), and the AWS default VPC range 172.31.0.0/16; delete unused default VPCs.
- 172.17.0.0/16 (Docker default bridge) and ranges used by on-prem or VPN client pools.
- Sizing every VPC as /16 "just in case": the pool runs out.

## Verify
- [ ] Every VPC CIDR exists in IPAM with owner and environment, and an overlap check across clouds
  and on-prem returns nothing.
