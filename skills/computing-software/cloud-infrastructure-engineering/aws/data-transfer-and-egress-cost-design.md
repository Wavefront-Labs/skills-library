---
id: computing-software.cloud-infrastructure-engineering.aws.data-transfer-and-egress-cost-design
name: data-transfer-and-egress-cost-design
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, data-transfer, egress-cost, egress-costs, transfer-costs, nat-gateway-cost, cross-az-transfer, cross-region-transfer, vpc-endpoints, gateway-endpoint, cloudfront-egress, privatelink-cost, direct-connect-egress, internet-egress, az-affinity, usage-types, data-transfer-pricing, dx-data-transfer]
level: practitioner
status: draft
description: "Design AWS architectures that avoid data transfer charges: cross-AZ and cross-region traffic, NAT processing fees, gateway endpoints, CloudFront as cheap egress, and finding transfer costs in the CUR."
sources: ["AWS Blog - Overview of Data Transfer Costs for Common Architectures", "Amazon EC2 Pricing - Data transfer section", "Amazon VPC Pricing - NAT gateway and PrivateLink", "Amazon CloudFront Pricing and origin transfer rules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data transfer and egress cost design — the line item nobody budgeted for

**Goal:** know which flows are free, which are metered, and shape the architecture so the
metered ones are rare: same-AZ where possible, gateway endpoints instead of NAT, CloudFront
in front of anything public, and the CUR telling you when you got it wrong.

## 1. The rules of thumb (prices vary by region; order of magnitude)
| Flow | Cost |
|---|---|
| Internet **in** | free |
| Internet **out** from EC2/ELB/NAT | ~$0.09/GB first 10 TB (first 100 GB/month free per account) |
| Out via **CloudFront** | often cheaper per GB, and **origin → CloudFront is free** for AWS origins |
| **Same AZ**, private IP | free |
| **Cross-AZ** in a region | ~$0.01/GB **each direction** (so $0.02/GB round trip) |
| **Cross-region** | ~$0.02/GB (varies; some pairs higher) |
| **NAT gateway** | hourly + ~$0.045/GB *processed* — on top of any internet egress |
| **PrivateLink / interface endpoint** | hourly per AZ + ~$0.01/GB processed |
| **Gateway endpoints** (S3, DynamoDB) | free |
| **Transit Gateway** | hourly attachment + ~$0.02/GB processed |
| Direct Connect out | lower per GB than internet (~$0.02), port hourly |
| Public IP (IPv4) | hourly per address |
Elastic/public IP traffic between instances in the same region uses the regional rate even if they are in the same AZ — use private IPs.

## 2. The usual culprits
1. **NAT for S3/DynamoDB traffic** — backups, logs, Firehose, ECR layers all go S3. Fix: **gateway
   endpoints** in every route table (free), interface endpoints for ECR/Logs/SSM/STS where
   the volume justifies the hourly fee (break-even is a few hundred GB/month per AZ).
2. **Cross-AZ chatter**: app → DB replica in another AZ, Kafka consumers reading from
   brokers in other AZs, EKS pods talking across AZs, ALB → targets (cross-zone load
   balancing is free for ALB but the traffic ALB→target across AZ is *charged*; NLB cross-zone is charged).
   Fix: **AZ affinity** (topology-aware routing in EKS, rack-aware Kafka `client.rack`,
   read replicas per AZ), one-AZ-per-cell designs; accept it for HA paths (writer in other AZ).
3. **Serving static/media straight from S3/ALB**: put **CloudFront** in front — cheaper egress, free origin fetch, caching cuts origin bytes.
4. **Cross-region replication/log shipping**: S3 CRR, DynamoDB global tables, central logging
   accounts in another region. Fix: keep the logging/tooling region = workload region;
   compress before shipping; replicate only prefixes that need DR.
5. **Egress to the office/data centre over the internet**: Direct Connect pays for itself above a few TB/month.
6. **Public IPv4 everywhere**: per-IP hourly charge; use private subnets + NAT/endpoints or IPv6.
7. **Multi-account via Transit Gateway** for high-volume east-west (e.g. 100 TB/month ≈ $2 k in TGW processing): VPC peering is free for same-AZ, and cross-AZ only at the standard rate; PrivateLink for one-to-many services.

## 3. Find it in the bill
Cost Explorer → group by **Usage Type**, filter service EC2-Other/VPC/CloudFront:
- `DataTransfer-Out-Bytes` (internet egress), `DataTransfer-Regional-Bytes` (cross-AZ, both directions),
  `<region>-<region>-AWS-Out-Bytes` (cross-region), `NatGateway-Bytes`, `VpcEndpoint-Bytes`,
  `TransitGateway-Bytes`, `PublicIPv4:InUseAddress`, `CloudFront` `DataTransfer-Out-Bytes` by edge class.
- CUR query:
  ```sql
  SELECT line_item_usage_type, line_item_resource_id, SUM(line_item_usage_amount) gb, SUM(line_item_unblended_cost) cost
  FROM cur WHERE line_item_usage_type LIKE '%Bytes%' AND bill_billing_period_start_date = DATE '2026-10-01'
  GROUP BY 1,2 ORDER BY cost DESC LIMIT 50;
  ```
- Attribute cross-AZ traffic with **VPC Flow Logs** (fields `az-id`, `flow-direction`,
  `pkt-src-aws-service`, `traffic-path`): Athena query summing bytes where `src az-id != dst az-id`
  by ENI/security group → the chatty pair.
- **Cost Explorer "Data transfer" view** and Trusted Advisor's NAT/idle checks give a first pass.

## 4. Design checklist for a new workload
- Gateway endpoints for S3/DynamoDB in every VPC (module default).
- NAT per AZ (avoid cross-AZ NAT hop + single point of failure) — the hourly cost is worth it.
- CloudFront for all public HTTP; S3 origin via OAC; ALB origin with origin shield if many POPs.
- Logging, metrics, backups and CI in the **same region** as the workload.
- Replica/consumer placement per AZ; EKS `topologySpreadConstraints` + topology-aware hints.
- IPv6/dual-stack where clients support it; minimise public IPv4 addresses.
- Big batch moves: S3 Batch Operations / DataSync within region; Snow devices or Direct Connect for off-cloud.
- Budget: a **Usage budget** on `DataTransfer-Regional-Bytes` and `NatGateway-Bytes` GB/month.

## Gotchas
- Cross-AZ is billed on *both* ENIs, so a 1 TB conversation costs 2 TB of regional transfer.
- S3 → internet via a presigned URL is S3 egress (~$0.09/GB); through CloudFront it is CloudFront egress (cheaper, cacheable).
- Interface endpoints are per AZ: attaching in one AZ makes other AZs' traffic cross-AZ to reach it (and a SPOF); deploy per AZ.
- NAT processing applies to *all* bytes through it, including S3 traffic that could have been free.
- Inter-region VPC peering and TGW peering are charged at cross-region rates; "peering is free" is only true within a region/AZ.
- Unconfirmed: current per-GB prices and free-tier amounts — read the pricing pages for your regions before quoting numbers.

## Verify
- [ ] Every VPC route table has S3 and DynamoDB gateway endpoints (`describe-vpc-endpoints`, type Gateway).
- [ ] `NatGateway-Bytes` dropped after endpoints were added (before/after in Cost Explorer).
- [ ] Flow-log Athena query shows the top cross-AZ pairs and each has an owner/decision.
- [ ] Public assets return `x-cache: Hit from cloudfront` and S3 `DataTransfer-Out-Bytes` is near zero.
- [ ] Usage budgets on regional and NAT bytes alert the platform team.
