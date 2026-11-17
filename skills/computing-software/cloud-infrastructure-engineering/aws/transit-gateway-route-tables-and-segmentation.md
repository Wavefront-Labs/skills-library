---
id: computing-software.cloud-infrastructure-engineering.aws.transit-gateway-route-tables-and-segmentation
name: transit-gateway-route-tables-and-segmentation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transit-gateway, tgw-route-table, tgw-association, tgw-propagation, network-segmentation, blackhole-route]
level: practitioner
status: docs-checked
description: "Segment networks on Transit Gateway with multiple route tables: associations vs propagations, prod/dev/shared isolation, blackhole routes and disabling default tables."
sources: ["https://docs.aws.amazon.com/vpc/latest/tgw/tgw-route-tables.html", "https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-isolated-shared.html", "https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transit Gateway route tables and segmentation

## 1. Two verbs
- **Association**: which route table an attachment *uses to look up* destinations
  (exactly one per attachment).
- **Propagation**: which route tables *learn* the attachment's CIDRs (any number).
Segmentation = choosing who propagates where.

## 2. Create the TGW without defaults
```bash
aws ec2 create-transit-gateway --description core --options \
  DefaultRouteTableAssociation=disable,DefaultRouteTablePropagation=disable,AutoAcceptSharedAttachments=disable,AmazonSideAsn=64512
```
With the defaults the TGW has one default route table that is both the default association and propagation table, so
every attachment can reach every other. If you disable both default association and propagation, no default route table is created.

## 3. Prod / dev / shared-services pattern
| Route table | Associated attachments | Propagations into it |
|---|---|---|
| `rt-prod` | prod VPCs | prod VPCs, shared, on-prem (VPN/DX) |
| `rt-dev` | dev VPCs | dev VPCs, shared |
| `rt-shared` | shared-services VPC, VPN/DX | prod, dev, shared |
```bash
aws ec2 associate-transit-gateway-route-table --transit-gateway-route-table-id rt-prod --transit-gateway-attachment-id att-prod1
aws ec2 enable-transit-gateway-route-table-propagation --transit-gateway-route-table-id rt-prod --transit-gateway-attachment-id att-shared
```
Prod and dev never learn each other's routes → no path. Remember the return direction: shared
must have routes back to both.

## 4. Static and blackhole routes
```bash
aws ec2 create-transit-gateway-route --transit-gateway-route-table-id rt-prod \
  --destination-cidr-block 0.0.0.0/0 --transit-gateway-attachment-id att-egress
aws ec2 create-transit-gateway-route --transit-gateway-route-table-id rt-prod \
  --destination-cidr-block 10.64.0.0/12 --blackhole     # dev supernet: explicit deny
```
The most specific route wins; for equal prefixes a static route beats a propagated one (the documented order is static, system, prefix-list, then VPC-, Direct Connect gateway-, Connect-, VPN-propagated routes).

## 5. Inspect
```bash
aws ec2 search-transit-gateway-routes --transit-gateway-route-table-id rt-prod \
  --filters Name=type,Values=static,propagated --query 'Routes[].[DestinationCidrBlock,Type,State,TransitGatewayAttachments[0].ResourceId]' --output table
```

## Gotchas
- VPC route tables still need routes to the TGW for remote CIDRs; TGW routes alone do nothing.
- Quotas (read 2026-10-27): 10,000 combined routes (static and dynamic) across all route tables of a TGW, 20 route tables per TGW (adjustable), one static route per prefix per attachment.
- Propagation from a VPC attachment advertises the VPC CIDR blocks; on-prem prefixes come from VPN or Direct Connect gateway attachments.

## Verify
- [ ] Route Analyzer (Network Manager) prod → dev path: blackholed/no route; prod → shared: connected.
- [ ] Reachability Analyzer from a prod instance to a dev instance shows not reachable at the TGW.
- [ ] `search-transit-gateway-routes` lists only intended CIDRs per table.

## Checked

Checked 2026-10-27 against the AWS Transit Gateway documentation (how transit gateways work: route tables, route evaluation order; quotas) and the botocore ec2 model.
- Corrected: disabling both default association and default propagation means no default route table is created; the documented route priority list (static, system, prefix-list, then propagated types) replaces the "longest prefix, static wins" shorthand; quota wording (10,000 combined routes, 20 route tables, one static route per prefix per attachment).
- Confirmed: one association per attachment, many propagations, blackhole routes drop matching traffic, VPC route tables still need routes to the TGW.

Method: documentation only; no commands were run.
