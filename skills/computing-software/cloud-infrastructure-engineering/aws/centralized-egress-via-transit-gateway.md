---
id: computing-software.cloud-infrastructure-engineering.aws.centralized-egress-via-transit-gateway
name: centralized-egress-via-transit-gateway
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transit-gateway, centralized-egress, egress-vpc, inspection-vpc, appliance-mode, nat-gateway, network-firewall]
level: practitioner
status: docs-checked
description: "Centralise internet egress for many VPCs through an egress/inspection VPC behind Transit Gateway: route tables, appliance mode, blackhole routes and the cost trade-off."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/centralized-egress-to-internet.html", "https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-appliance-scenario.html", "https://docs.aws.amazon.com/network-firewall/latest/developerguide/arch-two-zone-igw.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centralised egress via Transit Gateway

**Goal:** spoke VPCs have no IGW or NAT; all internet-bound traffic exits through one
egress VPC (optionally inspected by Network Firewall), giving fixed egress IPs and one
place for controls.

## 1. Topology
```
spoke VPCs --(TGW attachments)--> TGW --> egress VPC: TGW subnets -> [firewall endpoints] -> NAT GW (public subnets) -> IGW
```
TGW route tables:
- **spoke RT** (associated with spoke attachments): `0.0.0.0/0 → egress attachment`;
  blackhole routes for `10.0.0.0/8` etc. if spokes must not talk to each other.
- **egress RT** (associated with egress attachment): propagations from all spokes (return path).
Spoke VPC route tables: `0.0.0.0/0 → tgw-...`.
Egress VPC: TGW-subnet RT `0.0.0.0/0 → firewall endpoint (same AZ)` or NAT; public subnet RT
`10.0.0.0/8 → tgw` (return) and `0.0.0.0/0 → igw`.

## 2. Appliance mode
With inspection in the egress VPC, enable it on that attachment so both directions of a flow
use the same AZ:
```bash
aws ec2 modify-transit-gateway-vpc-attachment --transit-gateway-attachment-id tgw-attach-egress \
  --options ApplianceModeSupport=enable
```
Without it, return traffic can land in a different AZ's firewall and stateful inspection drops it.

## 3. Cost reality
You pay TGW per-attachment-hour + **TGW data processing per GB** on top of NAT processing.
Centralising saves NAT hourly charges across many VPCs but adds TGW data processing; for high-volume
egress (e.g. pulling container images, S3) put **VPC endpoints in spokes** so that traffic never crosses the TGW.
See the Transit Gateway and NAT gateway pricing pages for rates.

## Gotchas
- NAT gateways per AZ in the egress VPC, and TGW attachment subnets in every AZ spokes use.
- Blackhole the spokes' supernet in the spoke RT, or spoke-to-spoke traffic hairpins through
  the egress VPC (and its firewall) unintentionally — or is allowed when it shouldn't be.

## Verify
- [ ] From a spoke instance, `curl https://checkip.amazonaws.com` returns an egress-VPC NAT EIP.
- [ ] TGW route analyzer: spoke → 0.0.0.0/0 resolves to the egress attachment; spoke → other spoke is blackholed (if intended).
- [ ] Firewall flow logs show both directions of sample flows in the same AZ.

## Checked

2026-10-28

Confirmed: appliance mode via --options ApplianceModeSupport=enable on create/modify-transit-gateway-vpc-attachment, stateful appliance flow symmetry (Transit Gateway appliance scenario page); centralized egress to internet pattern (multi-VPC whitepaper); two-AZ Network Firewall routing (Network Firewall guide).

Removed: per-GB price figure, 'gateway endpoints are free' price claim, Route 53 Resolver sentence.

Method: documentation only; no commands were run.
