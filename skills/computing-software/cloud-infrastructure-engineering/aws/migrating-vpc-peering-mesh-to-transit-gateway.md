---
id: computing-software.cloud-infrastructure-engineering.aws.migrating-vpc-peering-mesh-to-transit-gateway
name: migrating-vpc-peering-mesh-to-transit-gateway
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transit-gateway, peering-to-tgw-migration, vpc-peering, longest-prefix-match, network-migration, hub-and-spoke]
level: advanced
status: draft
description: "Move a VPC peering mesh onto Transit Gateway with no outage: attach in parallel, shift routes per VPC using longest-prefix match, verify, then delete peerings."
sources: ["https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html", "https://docs.aws.amazon.com/vpc/latest/tgw/tgw-best-design-practices.html", "https://docs.aws.amazon.com/vpc/latest/userguide/route-tables-priority.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrating from a VPC peering mesh to Transit Gateway

**Why migrate:** peering is non-transitive, needs n(n-1)/2 connections, and each VPC's route
tables fill with per-peer routes (50 routes default, 125 peering connections max). TGW
gives hub-and-spoke routing, central inspection and shared hybrid connectivity.

## 1. Before you start
- Inventory every peering and the routes using it:
  `aws ec2 describe-vpc-peering-connections` and, per VPC, routes with
  `VpcPeeringConnectionId` targets.
- Confirm no overlapping CIDRs across VPCs that will share a TGW route table (peering
  tolerated non-adjacent overlaps; TGW cannot route overlapping prefixes in one table).
- Security groups that reference **peer SG IDs** stop working over TGW (SG referencing
  across TGW is supported only within the same region with the TGW SG-referencing feature
  enabled on the attachment; check `SecurityGroupReferencingSupport`). Otherwise rewrite
  rules as CIDRs or prefix lists first.
- Cost change: TGW charges per attachment-hour and per GB processed; peering within an AZ
  was free and cross-AZ was cheaper. Model it for chatty VPC pairs; you can keep specific
  peerings for heavy flows.

## 2. Build in parallel
1. Create the TGW (`--options DefaultRouteTableAssociation=disable,DefaultRouteTablePropagation=disable`
   so you control segmentation), share via RAM.
2. Create VPC attachments in dedicated small subnets, one per AZ in each VPC.
3. Associate attachments with the right TGW route table; propagate VPC CIDRs.
At this point nothing uses the TGW yet: VPC route tables still point at peerings.

## 3. Shift traffic using route priority
VPC route tables use **longest prefix match**; for equal prefixes, a static route beats
a propagated one and peering routes are static. So:
- Option A (summary first): add a broad route `10.0.0.0/8 -> tgw-...` in every VPC.
  Existing specific `/16` peering routes still win. Then remove peering routes one VPC
  pair at a time; traffic falls through to the `/8` TGW route automatically.
- Option B (per-pair cutover): replace the peer route target with the TGW
  (`aws ec2 replace-route --route-table-id rtb-... --destination-cidr-block 10.30.0.0/16
  --transit-gateway-id tgw-...`) on **both** sides in the same change window, since
  asymmetric routing breaks stateful flows through appliances.
Do both directions per pair; test; move on.

## 4. Validate each step
- Reachability Analyzer between representative ENIs (source in VPC A, destination in VPC B)
  shows the path via the TGW attachment.
- TGW flow logs or VPC flow logs show traffic on attachment ENIs.
- Application health checks and connection error rates stable.
- `aws ec2 search-transit-gateway-routes --transit-gateway-route-table-id tgw-rtb-...
  --filters Name=type,Values=propagated` lists every VPC CIDR.

## 5. Decommission
When a peering has carried no traffic (flow logs filtered to the peering's path) for an
agreed period, delete it: `aws ec2 delete-vpc-peering-connection`. Remove now-unused
specific routes. Update IaC so it does not recreate them.

## Gotchas
- MTU: peering supports 9001 within region; TGW supports 8500. Jumbo-frame workloads see
  fragmentation or PMTUD issues; verify ICMP is allowed.
- DNS: peering "allow DNS resolution from remote VPC" does nothing over TGW; use Route 53
  Resolver rules or PHZ associations instead.
- Inter-region peering replaced by TGW peering needs static routes (TGW peering does not
  propagate).
- Appliance mode must be enabled on inspection VPC attachments to avoid asymmetric drops.

## Verify
- [ ] All VPC pairs reachable via TGW (Reachability Analyzer report saved).
- [ ] No route in any VPC route table targets a peering connection that is scheduled for deletion.
- [ ] SG rules no longer reference peer SG IDs (or TGW SG referencing enabled and tested).
- [ ] Monthly cost estimate for TGW data processing approved.
