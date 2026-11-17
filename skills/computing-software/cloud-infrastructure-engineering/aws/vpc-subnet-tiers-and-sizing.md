---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-subnet-tiers-and-sizing
name: vpc-subnet-tiers-and-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, subnet-tiers, isolated-subnets, subnet-sizing, reserved-ip-addresses, cidr-allocation, multi-az]
level: practitioner
status: docs-checked
description: "Lay out VPC subnets: public, private and isolated tiers per AZ, sizing for EKS/Lambda/endpoint IP demand, the 5 reserved IPs per subnet, and room for growth."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html", "https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html", "https://docs.aws.amazon.com/vpc/latest/userguide/subnet-public-ip.html", "https://docs.aws.amazon.com/eks/latest/best-practices/ip-opt.html", "https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subnet tiers and sizing

## 1. Tiers (one subnet per tier per AZ, at least 2 AZs, 3 for production)
| Tier | Route to internet | What lives there |
|---|---|---|
| **Public** | `0.0.0.0/0` to an internet gateway | ALB/NLB (internet-facing), NAT gateways, bastions if any |
| **Private (egress)** | `0.0.0.0/0` to the NAT gateway **in the same AZ** | app instances, ECS tasks, EKS nodes/pods, Lambda ENIs |
| **Isolated (data)** | no default route; only local + gateway endpoints + TGW for internal | RDS, ElastiCache, internal-only workloads |
| Optional: TGW/attachment | small dedicated subnets for TGW attachments and GWLB endpoints | keeps attachment ENIs and NACLs separate |
"Public" is purely the route table, not a subnet flag; `MapPublicIpOnLaunch` only decides
whether instances get a public IPv4 automatically (turn it off unless needed).

## 2. Reserved addresses
Each IPv4 subnet loses 5 IPs: network address (.0), VPC router (.1), DNS (.2), reserved for
future use (.3), and broadcast (last). The allowed IPv4 subnet sizes run from `/28` to `/16`; a `/28`
gives 11 usable addresses and a `/24` gives 251.

## 3. Sizing by consumer
Count IPs, not instances:
- **EKS with VPC CNI**: every pod takes a VPC IP; the CNI keeps warm IPs (`WARM_IP_TARGET`, with `MINIMUM_IP_TARGET` on large clusters to avoid EC2 API throttling),
  and prefix delegation assigns prefixes to ENIs to raise pod density. A 50-node cluster at 30 pods/node needs about
  1,500+ IPs plus the warm pool. EKS also creates up to 4 cross-account ENIs for the control plane and recommends at least a `/28` for cluster subnets. For pods you can use custom networking with a secondary CIDR;
  AWS recommends CIDRs from `100.64.0.0/10` for it.
- **Lambda in VPC**: Lambda creates Hyperplane ENIs in the subnets and security groups you choose; see the Lambda VPC guide before sizing.
- **Interface endpoints**: one endpoint network interface for each subnet you specify, so 20 endpoints in 3 AZs use 20 IPs per AZ.
- **ALB**: AWS requires a `/27` or larger subnet with at least 8 free IP addresses per subnet.
- **ECS awsvpc**: each task has its own ENI, so subnet IPs scale with task count.
Leave headroom (a 30-50% margin is a sensible planning figure). Plan a VPC CIDR large enough to add a
tier later (`/16` for big accounts, smaller ones with IPAM).

## 4. A worked /16 layout (3 AZs)
```
10.20.0.0/16
  public    10.20.0.0/24, 10.20.1.0/24, 10.20.2.0/24
  private   10.20.32.0/19, 10.20.64.0/19, 10.20.96.0/19
  isolated  10.20.8.0/22, 10.20.12.0/22, 10.20.16.0/22
  tgw       10.20.3.0/28, 10.20.3.16/28, 10.20.3.32/28
  spare     10.20.128.0/17   (future tier or second EKS cluster)
```
Create with IPAM (`--ipv4-ipam-pool-id` on `create-vpc`) so CIDRs never overlap across
accounts. Tag subnets with tier names (`tier=private`) and, for EKS load balancers,
`kubernetes.io/role/elb=1` (public) and `kubernetes.io/role/internal-elb=1` (private).

## 5. Checking remaining capacity
```bash
aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-0abc \
  --query 'Subnets[].{id:SubnetId,az:AvailabilityZone,cidr:CidrBlock,free:AvailableIpAddressCount,tier:Tags[?Key==`tier`]|[0].Value}' \
  --output table
```
Alarm when `AvailableIpAddressCount` drops below a threshold (publish it as a custom metric from a scheduled job).

## Gotchas
- AZ names map to different physical AZs per account; align with AZ IDs (`use1-az1`)
  when sharing subnets or peering latency-sensitive tiers.
- Some services need subnets in specific AZs (instance type availability, Local Zones).
- A secondary CIDR can be added later but is subject to the IPv4 CIDR block association restrictions, and peered VPCs cannot have overlapping CIDR blocks.

## Verify
- [ ] Each tier exists in every AZ used, with the expected route table (IGW / same-AZ NAT / none).
- [ ] `AvailableIpAddressCount` leaves at least 30% headroom on EKS and endpoint subnets.
- [ ] VPC CIDR allocated from IPAM; no overlap with on-prem or other VPCs.

## Checked

Checked 2026-10-27 against the Amazon VPC User Guide (subnet CIDR blocks, VPC basics, subnet IP addressing attributes), the Application Load Balancer guide, the Amazon EKS best practices (IP optimization) and user guide, the PrivateLink concepts page, the Amazon ECS awsvpc networking page and the botocore EC2 model.
- Five reserved IPv4 addresses per subnet, allowed IPv4 sizes (/28 to /16) and the 11 and 251 usable counts confirmed.
- ALB `/27` with eight free IPs, endpoint ENI per enabled subnet, ECS awsvpc ENI per task, EKS `WARM_IP_TARGET`, `MINIMUM_IP_TARGET`, `100.64.0.0/10` recommendation, `/28` minimum for EKS subnets and `kubernetes.io/role/elb` and `internal-elb` tags confirmed.
- `create-vpc --ipv4-ipam-pool-id` confirmed in the service model.
- Removed the `/19`-`/18` EKS recommendation, the Lambda sharing explanation, the RDS remark, the claim that subnets cannot be resized and the IPAM utilisation metrics mention, none of which a page read confirms.

Method: documentation only; no commands were run.
