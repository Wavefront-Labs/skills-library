---
id: computing-software.cloud-infrastructure-engineering.aws.public-ipv4-addressing-and-charges
name: public-ipv4-addressing-and-charges
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, auto-assign-public-ip, public-ipv4-charges, elastic-ip, ipam-public-ip-insights, cost-optimization]
level: practitioner
status: docs-checked
description: "Control public IPv4 use: auto-assign settings per subnet and launch, AWS charging for every public IPv4, finding them with IPAM Public IP Insights, and reducing them."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html", "https://docs.aws.amazon.com/vpc/latest/ipam/view-public-ip-insights.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/modify-network-interface-attribute.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-network-interfaces.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Public IPv4 addressing and charges

## 1. The charge
AWS charges for **all** public IPv4 addresses, including those associated with running
instances and Elastic IPs. Rates are on the Public IPv4 Address tab of the Amazon VPC
pricing page; check it rather than quoting figures. Unassociated (idle) addresses still
appear in your account and Public IP insights flags them for release.

## 2. Where public IPs come from
- **Subnet attribute**: all subnets have an attribute that decides whether network
  interfaces created there automatically get a public IPv4. In a default VPC instances get
  one by default; in a nondefault subnet they do not by default.
  `aws ec2 modify-subnet-attribute --subnet-id subnet-0pub --no-map-public-ip-on-launch`
- **At launch**: enabling or disabling public IP at launch (run-instances network
  interface `AssociatePublicIpAddress`, launch wizard) overrides the subnet attribute.
- **After launch**: unassign by managing the network interface; the CLI exposes
  `modify-network-interface-attribute --no-associate-public-ip-address` (applies only to the
  primary interface, eth0).
- **Elastic IPs**: persistent, allocated to your account, can be moved between instances.
- **Service-managed**: Public IP insights lists addresses used by Global Accelerator, DMS
  replication instances, Redshift, RDS, ALB/NLB, public NAT gateways and Site-to-Site VPN.
- An auto-assigned public IP comes from Amazon's pool, not your account. It is released
  when the instance is stopped, hibernated or terminated (a new one is assigned on start),
  and when you associate an Elastic IP (a new one is assigned on disassociate). It is not
  reassigned if the instance has a secondary network interface.

## 3. Find them
```bash
aws ec2 describe-addresses --query 'Addresses[].{ip:PublicIp,assoc:AssociationId,eni:NetworkInterfaceId}'
aws ec2 describe-network-interfaces --filters Name=association.public-ip,Values='*' \
  --query 'NetworkInterfaces[].{eni:NetworkInterfaceId,type:InterfaceType,desc:Description,ip:Association.PublicIp,owner:Association.IpOwnerId}'
```
In the IPAM console choose **Public IP insights**: it breaks addresses down by type (Amazon-owned
EIP, EC2 public IP, BYOIP, service managed IP, contiguous EIPs), by EIP usage
(associated/unassociated) and by service. CLI: `get-ipam-discovered-public-addresses`. With
an IPAM integrated with an AWS Organization it covers all accounts and Regions.

## 4. Reduce (AWS EC2 guide, "Public IPv4 address optimization")
1. Release unassociated Elastic IPs (`aws ec2 release-address --allocation-id eipalloc-...`)
   after confirming nothing depends on them.
2. Put instances behind an elastic load balancer and disable auto-assign public IP on the
   primary interface; consolidate existing load balancers.
3. Use EC2 Instance Connect Endpoint instead of a NAT gateway solely for SSH to private instances.
4. Move instances to private subnets and use a public NAT gateway, after working out the
   cost with the formula on that page (hourly NAT cost + NAT IPs + NAT transfer against
   your current public IP cost).
5. Use AWS PrivateLink instead of public IPv4 plus internet gateway; use BYOIP; use Global
   Accelerator endpoints for instances in private subnets.
6. Turn off auto-assign on subnets and check network interfaces have it disabled.
7. IPv6: private IPv6 addresses have no charge (page statement for private IPv6 only).

## Gotchas
- Removing a public IP breaks anything still connecting to it, and a new auto-assigned IP
  will differ; confirm nothing depends on it first.
- Dynamic DNS pointing at an auto-assigned IP can take up to 24 hours to propagate; use an
  Elastic IP for a stable address.

## Verify
- [ ] No subnet has auto-assign public IP enabled unless documented.
- [ ] Public IP insights shows no unassociated EIPs you do not intend to keep.

## Checked
Date: 2026-11-07
Method: documentation only; no commands were run.
Read in full: "IP addressing for your VPCs and subnets" (public IPv4 and private IPv6
sections), "View public IP insights", and "Amazon EC2 instance IP addressing" (public IPv4,
optimization). The CLI pages for modify-network-interface-attribute and
describe-network-interfaces were searched for the named flag and filter, not read in full.
The VPC pricing page (aws.amazon.com/vpc/pricing/) was dropped from sources: it is a
marketing page; no rates are quoted.
Removed: all prices and the February 2024 date, the free-tier hours and "BYOIP not charged"
claims, "idle EIPs were always charged", ALB/NLB node-count and EKS statements, Config
rule names, SCP/IAM guardrail, VPC Block Public Access, Session Manager, DNS64/NAT64 and
"IPv6 is free" (only private IPv6 is stated free), PubliclyAccessible advice, CUR usage
types, EIP recovery via allocate-address.
