---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.data-transfer-costs
name: data-transfer-costs
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-aware-architecture, data-transfer-costs, egress, cross-az-traffic, inter-region-transfer, nat-gateway-costs, vpc-endpoints, private-service-connect, cdn-offload]
level: practitioner
status: draft
description: "Find and cut data transfer cost: internet egress, cross-AZ and inter-region traffic, NAT processing, endpoints for cloud services, CDN offload and topology-aware routing."
sources: ["https://aws.amazon.com/blogs/architecture/overview-of-data-transfer-costs-for-common-architectures/", "https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview#pricing", "https://cloud.google.com/vpc/network-pricing", "https://www.finops.org/framework/capabilities/architecting-for-cloud/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data transfer and egress cost design

## Where the money goes (typical)
| Path | Billed? |
|---|---|
| Inbound from internet | usually free |
| Out to internet | per GB, tiered |
| Between AZs in a region | AWS: per GB **each direction**; GCP: per GB between zones; Azure: inter-AZ charges announced then waived — check current pricing |
| Between regions | per GB, higher |
| Through NAT gateway | per-GB processing on top of transfer |
| To provider services (object storage, APIs) via NAT | NAT processing charges avoidable with endpoints |
| Peering / transit gateway | per-GB attachment processing (TGW) |

## Find it
Group billing by usage type: AWS `DataTransfer-Regional-Bytes` (cross-AZ), `*-AWS-Out-Bytes`,
`NatGateway-Bytes`, `TransitGateway-Bytes`; Azure "Bandwidth" meters; GCP SKUs "Network Inter
Zone/Region Data Transfer Out". VPC flow logs to find talkers.

## Reduce
1. **Gateway/private endpoints** for object storage and DynamoDB (AWS gateway endpoints are free);
   interface endpoints / Private Link / Private Service Connect for other services where cheaper than NAT.
2. **Keep chatty traffic in-zone**: Kubernetes topology-aware routing / `trafficDistribution:
   PreferClose`, zone-aware load balancing, read replicas per AZ, Kafka rack-aware consumers
   (`client.rack`) fetching from the nearest replica.
3. **CDN** in front of public downloads/APIs (CDN egress often cheaper; origin shield cuts origin fetches).
4. Compress payloads; avoid cross-region replication you don't need for DR.
5. Co-locate compute with data (analytics jobs in the data's region).
6. For big egress, provider interconnect egress rates are lower than internet rates.

## Gotchas
- HA across AZs is worth the cross-AZ cost; optimise chattiness, not redundancy.
- Logs/metrics shipped cross-region to a central account are a hidden transfer line.

## Verify
- [ ] Top 5 transfer usage types identified with owners.
- [ ] Endpoints in place for object storage from private subnets.
