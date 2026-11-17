---
id: computing-software.systems-network-administration.network-design.cloud-data-transfer-and-egress-costs
name: cloud-data-transfer-and-egress-costs
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cloud-networking, egress-costs, data-transfer-costs, nat-gateway-costs, finops]
level: practitioner
status: draft
description: "Design cloud networks with data transfer costs in mind: internet egress, inter-AZ and inter-region charges, NAT gateway processing, endpoints and private interconnect."
sources:
  - https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer
  - https://azure.microsoft.com/en-us/pricing/details/bandwidth/
  - https://cloud.google.com/vpc/network-pricing
  - https://docs.aws.amazon.com/whitepapers/latest/aws-overview/networking-services.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data transfer and egress costs

## Where the money goes (pattern common to AWS/Azure/GCP)
| Flow | Charged? |
|---|---|
| Inbound from internet | free |
| Outbound to internet | per GB, tiered (largest single networking cost for many) |
| Within an AZ via private IP | free (AWS) |
| Between AZs in a region | per GB each direction (AWS ~0.01/GB each way) |
| Between regions | per GB |
| NAT gateway | hourly + per GB processed, on top of egress |
| PrivateLink/interface endpoints | hourly per AZ + per GB |
| Direct Connect / ExpressRoute / Interconnect egress | lower per-GB rate than internet |
Check current price pages; numbers change and differ by region.

## Design levers
- Keep chatty tiers in the same AZ where HA allows (zonal affinity in LBs/Kubernetes topology-aware
  routing).
- **S3/DynamoDB gateway endpoints** are free: stop routing S3 traffic through NAT gateways.
- Serve public content through a CDN (cheaper egress, caching).
- Replicate across regions only what needs it; compress.
- Large steady egress to on-prem: private interconnect.
- Watch cross-AZ traffic of managed services (replicas, Kafka, load balancers with cross-zone on).

## Find it
AWS Cost Explorer by usage type (`DataTransfer-Regional-Bytes`, `NatGateway-Bytes`), CUR with
resource IDs, flow logs for top talkers; Azure Cost Management; GCP billing export to BigQuery.

## Verify
- [ ] Monthly report of egress, inter-AZ and NAT bytes per account with owners; S3 traffic bypasses NAT via endpoints.
