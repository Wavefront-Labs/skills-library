---
id: computing-software.cloud-infrastructure-engineering.aws.nat-gateway-per-az-zonal-design
name: nat-gateway-per-az-zonal-design
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, nat-gateway, nat-per-az, zonal-nat, az-independent-egress, static-stability, route-table, egress]
level: practitioner
status: docs-checked
description: "Lay out NAT gateways one per AZ with per-AZ private route tables so an AZ failure cannot cut egress elsewhere, and weigh that against single-NAT cost and regional NAT."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html", "https://docs.aws.amazon.com/whitepapers/latest/advanced-multi-az-resilience-patterns/advanced-multi-az-resilience-patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT gateway per AZ (zonal egress)

**Goal:** losing one Availability Zone never takes away internet egress from instances in the
other AZs, and no traffic pays cross-AZ charges just to reach a NAT gateway.

## 1. Layout
```
AZ a: public-a (NAT-a, EIP-a)   private-a  -> rtb-private-a: 0.0.0.0/0 -> NAT-a
AZ b: public-b (NAT-b, EIP-b)   private-b  -> rtb-private-b: 0.0.0.0/0 -> NAT-b
AZ c: public-c (NAT-c, EIP-c)   private-c  -> rtb-private-c: 0.0.0.0/0 -> NAT-c
```
One route table **per AZ** for private subnets; never one shared private route table pointing
at a single NAT.
```bash
for az in a b c; do
  NAT=$(aws ec2 create-nat-gateway --subnet-id ${PUB[$az]} --allocation-id ${EIP[$az]} --query NatGateway.NatGatewayId --output text)
  aws ec2 wait nat-gateway-available --nat-gateway-ids $NAT
  aws ec2 create-route --route-table-id ${RTB[$az]} --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT
done
```

## 2. Trade-off
| | Single NAT | NAT per AZ |
|---|---|---|
| Number of NAT gateways billed | 1 | N (one per AZ) |
| AZ failure of the NAT's AZ | resources in other AZs lose internet access | only that AZ |
| Cross-AZ data | cross-AZ traffic to reach the NAT adds data transfer charges | none for NAT access |
AWS recommends a NAT gateway in each AZ; its pricing guidance is to keep resources in the same AZ as the NAT gateway, or create one per AZ.
Use a single NAT gateway only where an outage of its AZ is acceptable, such as dev or sandbox.

## 3. Regional NAT gateway option
A regional NAT gateway (`aws ec2 create-nat-gateway --vpc-id <VPC_ID> --availability-mode regional`) expands and contracts across AZs with your workload, needs no public subnet and has one NAT ID for every AZ.
It supports up to 32 IP addresses per AZ (8 for zonal). It can take up to 60 minutes to expand into a new AZ; traffic is processed from another AZ until then. It has automatic and manual modes,
does not support private NAT (use a zonal NAT gateway for that), and is not available in constrained AZs. Converting resets existing connections. Check that it fits your IP allow-listing needs before redesigning.

## Gotchas
- Partner allow-lists must include every NAT EIP (3 IPs, not 1).
- A NAT gateway in AZ a serving subnets in AZ b breaks static stability silently — audit:
  `describe-route-tables` and compare each route table's subnet AZ with its NAT's subnet AZ.
- Deleting a NAT gateway leaves routes that point to it in a blackhole status until you delete or update them; recreate before deleting in migrations.

## Verify
- [ ] For every private route table, the NAT gateway's subnet AZ equals the associated subnets' AZ.
- [ ] Simulate AZ loss (remove the NAT route in AZ a in a test VPC): instances in b and c still reach the internet.
- [ ] No cross-AZ data transfer growth attributable to NAT traffic in your cost reports.

## Checked

Checked 2026-10-27 against the Amazon VPC User Guide (NAT gateway basics, NAT gateway pricing guidance, regional NAT gateways, working with NAT gateways) and the botocore EC2 model.
- One NAT gateway per AZ with a same-AZ route (including loss of internet access in other AZs when a shared NAT's AZ fails) confirmed on the basics page; `create-nat-gateway` for zonal use confirmed in the model and the `nat-gateway-available` waiter in the waiters file.
- Regional NAT gateway facts (availability mode, 32 addresses per AZ versus 8, up to 60 minutes to expand, no private NAT, connection reset on conversion, constrained AZ exclusion) confirmed on the regional NAT page.
- Blackhole routes after deletion confirmed. No prices are stated.
- Removed the CDK `natGateways` remark and the Cost Explorer usage type name, which no page read confirms.

Method: documentation only; no commands were run.
