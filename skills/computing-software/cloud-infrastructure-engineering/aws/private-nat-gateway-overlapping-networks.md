---
id: computing-software.cloud-infrastructure-engineering.aws.private-nat-gateway-overlapping-networks
name: private-nat-gateway-overlapping-networks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, nat-gateway, private-nat-gateway, private-nat, overlapping-cidr, transit-gateway, hybrid-connectivity]
level: practitioner
status: docs-checked
description: "Use private NAT gateways to connect VPCs with overlapping or non-routable CIDRs to on-prem and other VPCs via TGW, including secondary IPs and the reverse-path limitation."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html", "https://aws.amazon.com/blogs/networking-and-content-delivery/how-to-solve-private-ip-exhaustion-with-private-nat-solution/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private NAT gateway for overlapping networks

**Goal:** workloads in an overlapping or non-routable range (e.g. every VPC reusing
100.64.0.0/16, or an acquired company's 10.0.0.0/16) can initiate connections to shared
services and on-prem through Transit Gateway.

## 1. Create
```bash
aws ec2 create-nat-gateway --subnet-id subnet-routable-a --connectivity-type private \
  --secondary-private-ip-address-count 7      # more IPs = more concurrent connections
```
- Lives in a subnet from the **routable** CIDR; no Elastic IP (a public NAT gateway is the type that
  needs one).
- The quota is 8 private IP addresses per NAT gateway (adjustable): the primary plus up to 7
  secondary. Check the VPC quotas page for per-IP connection limits.

## 2. Routing
Non-routable subnet route table:
```
10.0.0.0/8 (corporate)   -> nat-private-a
0.0.0.0/0                -> nat-public-a    (if internet needed)
```
Routable subnet (where the private NAT lives):
```
10.0.0.0/8 -> tgw-123
```
TGW and on-prem see only the private NAT's routable IP as the source.

## 3. One-way limitation
NAT is outbound-initiated only. For inbound connections to a service in the overlapping
range, put an **internal ALB/NLB in routable subnets** (targets in the non-routable subnets),
or expose it via PrivateLink/VPC Lattice — those also solve overlap without NAT.

## Gotchas
- Traffic to the destination comes from the private NAT gateway's private IP, so the original
  source IP is lost for downstream logging; correlate via flow logs.
- Pricing: see the VPC pricing page.
- A NAT gateway cannot be reached from Site-to-Site VPN or Direct Connect through a virtual private
  gateway; use a transit gateway.
- Don't propagate the overlapping CIDR into TGW route tables (or the duplicate routes collide).

## Verify
- [ ] From a 100.64 subnet host: `curl http://onprem-host:8080` works; the on-prem access log shows the private NAT's IP.
- [ ] `aws ec2 describe-nat-gateways` shows the private gateway `available` with the expected address count.
- [ ] TGW route tables contain only routable CIDRs for the VPC.

## Checked
2026-10-31. Confirmed in the NAT gateway scenarios, NAT gateway basics and VPC quotas pages: private NAT for overlapping CIDRs via a routable subnet and transit gateway, ALB in the routable range for the reverse direction, private IP quota of 8 per NAT gateway (adjustable), source address is the NAT gateway's private IP, no VGW route from VPN/DX. Removed as unconfirmed: the 55,000-connection figure, the claim that a private NAT cannot use an internet gateway, the billing statement, and the describe-nat-gateways filter name.
Method: documentation only; no commands were run.
