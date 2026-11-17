---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.private-endpoints
name: private-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, private-endpoints, private-link, vpc-endpoints, gateway-endpoints, private-service-connect, service-endpoints, disable-public-network-access, endpoint-policies]
level: practitioner
status: draft
description: "Reach PaaS privately: gateway vs interface endpoints, Private Link and Private Service Connect, central vs per-VPC endpoints, DNS, policies, public access off."
sources: ["https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html", "https://learn.microsoft.com/azure/private-link/private-endpoint-overview", "https://cloud.google.com/vpc/docs/private-service-connect"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Private access to PaaS services

## Mechanisms
| Cloud | Options |
|---|---|
| AWS | **Gateway endpoints** (S3, DynamoDB; free, route-table based); **interface endpoints** (PrivateLink ENIs, hourly + per-GB) for most other services and your own services |
| Azure | **Private endpoints** (NIC with private IP per resource); service endpoints (keep public IP, restrict by subnet — older, simpler) |
| GCP | **Private Google Access** (subnet setting), **Private Service Connect** endpoints for Google APIs and published services; Private services access for Cloud SQL etc. |

## Design steps
1. List PaaS dependencies per workload and whether they support private access.
2. Choose central vs distributed: AWS interface endpoints can be centralised in a shared-services
   VPC with Route 53 private hosted zones shared to spokes (cuts per-VPC endpoint cost at scale);
   Azure private endpoints are per resource; GCP PSC endpoints in hub VPCs.
3. DNS so the public service name resolves to the private IP (see DNS architecture).
4. **Endpoint policies** (AWS) to restrict which buckets/resources are reachable — part of the data perimeter.
5. **Disable public network access** on the resource once private access works
   (`publicNetworkAccess: Disabled` in Azure; bucket policies with `aws:SourceVpce`; VPC-SC on GCP).

## Gotchas
- Costs: interface endpoints per AZ per hour × number of services × VPCs adds up — centralise.
- Some management operations still use public endpoints (portal access to data plane, CI runners) — plan where they run.

## Verify
- [ ] Access from the internet to the PaaS resource is denied.
- [ ] Workloads resolve service names to private IPs.
