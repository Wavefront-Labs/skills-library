---
id: computing-software.cloud-infrastructure-engineering.aws.regional-nat-gateway-availability-mode
name: regional-nat-gateway-availability-mode
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, nat-gateway, regional-nat-gateway, availability-mode, egress]
level: advanced
status: gated
description: "Use the regional availability mode of NAT gateway, which spans AZs automatically, and compare it with per-AZ zonal NAT gateways for resilience and routing."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-working-with.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regional NAT gateway availability mode

**What it is:** a NAT gateway created in *regional* availability mode belongs to the VPC rather than one
subnet, and AWS expands it into the AZs where you run workloads. One gateway ID, one route target, AZ
resilience without managing a NAT per AZ.

## 1. Zonal vs regional
| | Zonal (classic) | Regional |
|---|---|---|
| Placement | one public subnet in one AZ | VPC-level, expands across AZs |
| Routes | one route table per AZ pointing at its local NAT | all private tables can point at the same NAT ID (gated: unconfirmed, source is paywalled or blocked) |
| AZ failure | that AZ's egress fails unless you re-route | gateway keeps serving remaining AZs (gated: unconfirmed, source is paywalled or blocked) |
| Egress IPs | one EIP per NAT | IPs per AZ footprint; list them all for allowlists (gated: unconfirmed, source is paywalled or blocked) |

## 2. Create and route
Create the gateway with availability mode `regional` (NatGateway `AvailabilityMode` is `zonal` or `regional`), then:
```bash
aws ec2 describe-nat-gateways --nat-gateway-ids nat-0abc --query 'NatGateways[].{mode:AvailabilityMode,addrs:NatGatewayAddresses}'
aws ec2 create-route --route-table-id rtb-private-a --destination-cidr-block 0.0.0.0/0 --nat-gateway-id nat-0abc
aws ec2 create-route --route-table-id rtb-private-b --destination-cidr-block 0.0.0.0/0 --nat-gateway-id nat-0abc
```

## 3. Decision points
- Fewer moving parts and no per-AZ route table split: regional.
- Strict control of which IP each AZ uses, private NAT for overlapping networks, or existing zonal
  IaC that works: stay zonal.
- See the NAT gateway pricing page for how charges apply.

## Verify
- [ ] Workloads in every AZ reach the internet; `checkip` results match the gateway's listed addresses.
- [ ] Simulated AZ impairment (FIS) leaves other AZs' egress working.

## Checked

2026-10-28

Confirmed: regional NAT gateways expand automatically across AZs (VPC User Guide heading); AvailabilityMode values zonal/regional, ConnectivityType private/public, AutoScalingIps, AutoProvisionZones (botocore ec2); describe-nat-gateways, create-route and flags (check_commands).

Removed: the CLI-help hedge and the cost sentence.

Gated: the route-table, AZ-failure and egress-IP rows of the comparison table: the fetched VPC pages are index-level and do not state them.

Method: documentation only; no commands were run.
