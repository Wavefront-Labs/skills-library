---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.network-cost-allocation
name: network-cost-allocation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, allocation, network-cost-allocation, data-transfer, egress, transit-gateway, shared-cost-allocation, vpc-flow-logs]
level: practitioner
status: draft
description: "Allocate network and egress costs fairly: data transfer line items by resource, shared hubs such as transit gateways and NAT, flow-log based splits and proportional fallbacks."
sources: ["https://docs.aws.amazon.com/cur/latest/userguide/cur-data-transfers-charges.html", "https://docs.aws.amazon.com/vpc/latest/tgw/tgw-pricing.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html", "https://www.finops.org/framework/capabilities/allocation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Allocating network and egress costs

Network charges often land on a shared hub account (transit gateway, NAT, firewall, Direct
Connect) or on resources with no useful tags. Left alone they become a big unallocated bucket.

## Classify the charges
| Charge | Where it appears | Allocation approach |
|---|---|---|
| Instance / LB egress to internet | resource in the workload account | direct (resource tags) |
| Cross-AZ / inter-region transfer | resource in the workload account | direct |
| NAT gateway processing | shared networking account | flow logs by source ENI/subnet, else share of egress |
| Transit gateway attachment hours | per attachment | direct to attached VPC owner |
| Transit gateway data processing | account owning the sending attachment (check current AWS metering options) | direct or flow logs |
| Firewall / inspection | hub account | share of traffic processed |
| Direct Connect / ExpressRoute / Interconnect ports | hub | fixed: by bandwidth reservation; transfer: by flow volume |
| CDN | CDN account | by distribution / host owner |

## Steps
1. Pull transfer rows: in CUR, `product_product_family = 'Data Transfer'` or usage types
   containing `DataTransfer`, `NatGateway-Bytes`, `TransitGateway-Bytes`; group by account, usage
   type, resource id.
2. Direct-allocate everything with a resource owner.
3. For shared hubs, enable VPC flow logs (or Azure VNet flow logs / GCP VPC Flow Logs) on the hub
   with source and destination fields; aggregate bytes by source VPC/subnet -> owner per day.
   ```sql
   SELECT src_vpc_owner, SUM(bytes)/POW(1024,3) gib
   FROM flow_logs_enriched WHERE dt = DATE '2026-10-17' GROUP BY 1;
   ```
4. Allocate hub cost by byte share; fixed port costs by reserved bandwidth or agreed split.
5. Fallback where no flow data: proportional to each team's compute spend in the region, labelled
   as an estimate.

## Gotchas
- Flow logs themselves cost money (ingestion and storage); sample or aggregate and keep short
  retention for allocation.
- Cross-AZ charges are billed on both sides of the transfer; do not halve unless you know the split.
- Provider metering of shared network services has changed over time; re-read the pricing page
  before building rules.

## Verify
- [ ] Network unallocated share is reported and under the agreed threshold.
- [ ] Hub allocation sums to the hub's billed network cost each month.
