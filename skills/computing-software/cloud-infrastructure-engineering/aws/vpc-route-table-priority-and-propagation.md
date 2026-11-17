---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-route-table-priority-and-propagation
name: vpc-route-table-priority-and-propagation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, route-table, route-propagation, longest-prefix-match, local-route, gateway-route-table, middlebox-routing]
level: practitioner
status: docs-checked
description: "Reason about VPC route selection: longest prefix match, local route rules, static vs propagated VGW routes, prefix list routes, gateway route tables and middlebox insertion."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/route-tables-priority.html", "https://docs.aws.amazon.com/vpc/latest/userguide/route-table-options.html", "https://docs.aws.amazon.com/vpc/latest/userguide/gateway-route-tables.html", "https://docs.aws.amazon.com/vpc/latest/userguide/subnet-route-tables.html", "https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC route table priority and propagation

## 1. How a route is chosen
1. **Longest prefix match** wins: `10.1.2.0/24 → tgw` beats `10.0.0.0/8 → vgw`.
2. Same prefix: static routes (internet gateway, NAT gateway, network interface, gateway endpoint, transit gateway,
   peering, Gateway Load Balancer endpoint) beat routes that reference a prefix list, which beat propagated routes.
   Among propagated VGW routes: Direct Connect BGP beats VPN static beats VPN BGP. Overlapping prefix lists pointing to
   different targets are resolved by a random but then stable choice. IPv4 and IPv6 routes are evaluated independently.
3. The `local` route covers the VPC CIDR(s). You can add a **more specific** route, or replace the target of the local
   route, with a Gateway Load Balancer endpoint, NAT gateway or network interface (middlebox) as the basis of in-VPC inspection.

## 2. Inspect
```bash
aws ec2 describe-route-tables --filters Name=association.subnet-id,Values=subnet-abc \
  --query 'RouteTables[0].Routes[].[DestinationCidrBlock||DestinationPrefixListId,GatewayId||NatGatewayId||TransitGatewayId||VpcPeeringConnectionId||NetworkInterfaceId,Origin,State]' --output table
```
`Origin`: `CreateRouteTable` (local), `CreateRoute` (static), `EnableVgwRoutePropagation`, `Advertisement`.
`State` is `active`, `blackhole` or `filtered`; a route to a pending-acceptance peering or a deleted NAT gateway is a blackhole. A subnet without explicit association uses
the **main** route table — keep the main table minimal (no IGW route) so new subnets are
private by default.

## 3. Route propagation (VGW)
```bash
aws ec2 enable-vgw-route-propagation --route-table-id rtb-123 --gateway-id vgw-456
```
On-prem prefixes learned over VPN/DX appear automatically. Limit: 100 propagated routes per route table, not
adjustable; if you need more prefixes, advertise a default route. A VPC attached to a transit gateway needs a route in
its subnet route tables (a static route or a prefix-list route); enabling or disabling propagation can change which
route wins, since static routes are preferred.

## 4. Gateway route tables (ingress routing)
Associate a route table with the IGW or VGW (`--gateway-id` association) to steer **inbound**
traffic: e.g. `10.0.1.0/24 → vpce-gwlb` sends internet ingress for that subnet through
inspection before it reaches instances. Rules: targets are only `local`, a Gateway Load Balancer endpoint or a network
interface; destinations must be inside your VPC CIDR (the whole VPC CIDR replaces the local target, a subnet CIDR is
more specific); no prefix-list destinations; route propagation must be off; it cannot steer traffic outside the VPC
(for example via a transit gateway). The return traffic must pass through the same appliance (asymmetric routing is not
supported).

## 5. Prefix lists as destinations
`aws ec2 create-route --destination-prefix-list-id pl-123 --transit-gateway-id tgw-...`
keeps one list of corporate ranges across many tables; the list's maximum entries count toward the route quota.
Prefix lists are not allowed as destinations in gateway route tables.

## Gotchas
- Routes per route table default to 500 (adjustable to 1,000, which might affect network performance); propagated
  routes are capped at 100.
- Asymmetric routing through a middlebox is not supported; return traffic must use the same appliance.
- IGW route to an instance in a "private" subnet still does nothing without a public IP.

## Verify
- [ ] Reachability Analyzer from source ENI to destination shows the intended route table entry.
- [ ] No `blackhole` routes: `describe-route-tables --query 'RouteTables[].Routes[?State==\`blackhole\`]'` empty.
- [ ] Propagated route count per table below 100.

## Checked

Date: 2026-10-27. Sources: Amazon VPC User Guide pages "How route priority works", "Route table options (example routing options)", "Gateway route tables", "Subnet route tables" and "Amazon VPC quotas"; Transit Gateways Guide (VPC attachment routing); botocore EC2 model (Route.Origin and Route.State enums, CreateRoute destination and target members).
Corrected: static routes rank above prefix-list routes, which rank above propagated routes; the route limit is 500 (not 50); the Route object has no VpcEndpointId member, so the JMESPath was changed to VpcPeeringConnectionId; route origins also include Advertisement and states include filtered.
Removed: the claim that BGP advertisements beyond 100 are dropped and the word "silently" for asymmetric routing (the documented behaviour is "not supported").

Method: documentation only; no commands were run.
