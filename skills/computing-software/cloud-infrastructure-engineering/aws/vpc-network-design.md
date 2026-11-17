---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-network-design
name: vpc-network-design
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, vpc-design, subnets, cidr, ipam, availability-zones, route-tables, internet-gateway, nat-gateway, egress-only-internet-gateway, ipv6, security-groups, network-acls, nacl, vpc-endpoints, gateway-endpoint, interface-endpoint, privatelink, transit-gateway, vpc-peering, vpc-flow-logs, reachability-analyzer, data-transfer-cost, networking]
level: practitioner
status: docs-checked
description: "Design an AWS VPC: CIDR and IPAM planning, per-AZ subnet tiers, NAT and endpoint egress, security groups vs NACLs, and the data-transfer cost each choice creates."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html", "https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html", "https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/aws-services-privatelink-support.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS VPC network design — one VPC, built so it never has to be renumbered

**Goal:** a VPC whose address space will not collide with anything you later connect
to, whose subnets survive an AZ loss, whose egress is cheap and auditable, and whose
reachability you can prove. Hub-and-spoke across accounts belongs to
`computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-account-landing-zone`;
this skill is the design of each VPC.

## 1. Plan addresses before anything else
- Allocate from **VPC IPAM** pools (org-wide, per region, per environment) so no two VPCs
  overlap — overlap blocks peering and Transit Gateway routing forever.
- VPC IPv4 CIDR block size: /16 to /28 (also the subnet range). A /20 per workload VPC (4,096 addresses) is a common
  middle ground; you can add secondary CIDRs later but not shrink.
- Each IPv4 subnet loses **5 addresses** (the first four and the last: network, VPC router, DNS, future use, broadcast).
- Avoid ranges your on-prem, partners or container runtimes already use.
- Dual-stack: add an Amazon-provided /56 IPv6 block; subnets get /64s. Plan IPv6 now even
  if unused — it is the escape route when IPv4 runs out and cuts public IPv4 address cost.

## 2. Subnet tiers × AZs
Use at least 3 AZs where the region has them. Per AZ:
| Tier | Route to | Holds |
|---|---|---|
| public (small, e.g. /24) | Internet Gateway | ALB/NLB, NAT gateways only |
| private-app (large, e.g. /21) | NAT GW in **same AZ** | EC2, ECS, EKS nodes/pods, Lambda ENIs |
| private-data (e.g. /23) | none / endpoints | RDS, ElastiCache, internal-only |
EKS with the VPC CNI consumes one IP per pod — size app subnets for pods, or use prefix
delegation / a secondary CIDR (100.64.0.0/10 CG-NAT space) for pods.
One route table per tier per AZ (so each AZ routes to its own NAT).

## 3. Egress: NAT vs endpoints
- **NAT gateway**: one per AZ for resilience. A single shared NAT saves per-gateway cost but
  adds cross-AZ transfer cost and an AZ dependency — fine for dev, not prod.
- **Gateway endpoints** for S3 and DynamoDB: add them to every private route
  table. This removes the commonest large NAT bill (check the PrivateLink pricing page).
- **Interface endpoints** (PrivateLink) for ECR (`ecr.api`, `ecr.dkr`, plus S3 gateway for
  layers), STS, SSM (`ssm`, `ssmmessages`, `ec2messages`), Secrets Manager, KMS, CloudWatch Logs.
  Worth it when traffic volume or a no-internet requirement justifies the cost. Enable private DNS so SDKs need no config.
- IPv6 egress: **egress-only internet gateway**, no NAT cost.

## 4. Security groups first, NACLs sparingly
- SGs are stateful and can **reference other SGs**: `db-sg` allows 5432 from `app-sg`, not
  from a CIDR. This survives scaling and IP changes.
- NACLs are stateless, per subnet, evaluated by rule number; returns need the ephemeral port
  range open. Use them only as a coarse blast-radius layer (e.g. data subnets deny
  everything except app subnets).
- Default quota: 5 SGs per ENI and 60 rules per SG (inbound and outbound separately);
  hitting it signals a design problem.

## 5. Observe and prove
- **VPC Flow Logs** to S3 (cheaper) or CloudWatch Logs, with custom format including
  `pkt-srcaddr`, `pkt-dstaddr` and `flow-direction` so NAT-translated traffic is readable.
- **Reachability Analyzer** proves a path (e.g. ALB → instance:8080) and names the
  blocking component; **Network Access Analyzer** finds unintended paths (e.g. anything
  reaching the internet from data subnets).

## Gotchas
- Cross-AZ traffic is charged; chatty services pinned to one AZ's
  NAT or a load balancer without zonal awareness can cost more than compute.
- `enableDnsHostnames` and `enableDnsSupport` must both be true for interface-endpoint
  private DNS and for many managed services.
- A gateway endpoint policy that is too strict silently breaks yum/dnf repos, ECR layer
  pulls or SSM, which all fetch from AWS-owned buckets.
- Lambda in a VPC needs NAT or endpoints to reach AWS APIs — "it timed out" usually means no egress route.
- Check current pricing before modelling endpoint and NAT costs.

## Verify
- [ ] VPC CIDR allocated from IPAM and non-overlapping with every peer and on-prem range.
- [ ] Every tier spans ≥ 2 (prod: 3) AZs; each private route table points to its own AZ's NAT.
- [ ] S3/DynamoDB gateway endpoints attached to all private route tables.
- [ ] Data-tier SGs reference app SGs, not CIDRs; no `0.0.0.0/0` inbound except on public LBs.
- [ ] Flow Logs enabled; Reachability Analyzer confirms the intended path and Network Access Analyzer finds no internet path from data subnets.

## Checked
2026-10-31. Confirmed against the VPC User Guide (CIDR blocks and subnet sizing: /16 to /28, five reserved IPv4 addresses, Amazon-provided IPv6 /56 with /64 subnets), VPC quotas (5 security groups per network interface, 60 rules per security group enforced separately for inbound and outbound), the PrivateLink service list (`ecr.api`, `ecr.dkr`, `ssmmessages`, `ec2messages`), flow log record fields (`pkt-srcaddr`, `pkt-dstaddr`, `flow-direction`) and botocore EC2 ModifyVpcAttribute (`EnableDnsHostnames`, `EnableDnsSupport`). The 100.64.0.0/10 secondary-range remark matches the CIDR restrictions table. Removed: price and hourly-billing statements, the Docker bridge range remark and the ephemeral port range figure (not confirmed).
Method: documentation only; no commands were run.
