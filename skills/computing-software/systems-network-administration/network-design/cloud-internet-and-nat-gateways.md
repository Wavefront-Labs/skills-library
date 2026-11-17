---
id: computing-software.systems-network-administration.network-design.cloud-internet-and-nat-gateways
name: cloud-internet-and-nat-gateways
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cloud-networking, nat-gateway, internet-gateway, egress, aws-vpc, azure-nat-gateway, route-table]
level: practitioner
status: docs-checked
description: "Give cloud subnets internet access correctly: internet gateway for public subnets, NAT gateway per AZ for private ones, route tables, costs, SNAT port limits and egress control."
sources:
  - https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html
  - https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html
  - https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Internet and NAT gateways

## AWS model
- **Internet gateway (IGW):** attached to the VPC; a subnet is "public" because its route table
  has `0.0.0.0/0 -> igw-...` and instances have public IPs/EIPs. Two-way.
- **NAT gateway:** lives in a public subnet with an EIP; private subnets route
  `0.0.0.0/0 -> nat-...`. Outbound only.

```
public-a route table:  10.0.0.0/16 local ; 0.0.0.0/0 igw-123
private-a route table: 10.0.0.0/16 local ; 0.0.0.0/0 nat-a (NAT GW in public-a)
private-b route table: 10.0.0.0/16 local ; 0.0.0.0/0 nat-b (NAT GW in public-b)
```
Design judgement (not stated on the cited pages): place a NAT gateway in each AZ you use, with
per-AZ route tables, so one AZ failing does not remove egress for the others.

## Azure model
Use **Azure NAT Gateway** on the subnet (it allocates SNAT ports dynamically to reduce the risk of
port exhaustion) or firewall/load balancer outbound rules. Public IP on a
NIC gives direct inbound/outbound.

## Cost and limits
- NAT gateways are billed by usage (see the vendor pricing pages); consider VPC endpoints for
  traffic to AWS services so it does not need to cross the NAT gateway.
- SNAT port exhaustion: many connections to one destination IP:port (an API) from one NAT IP;
  watch the provider's NAT/SNAT metrics and add addresses.
- Egress filtering: a NAT gateway translates addresses; use a firewall or proxy for FQDN allowlists.

## Verify
- [ ] Private instance reaches the internet via its own AZ's NAT (check source IP), public subnets via IGW; endpoints in place for AWS service traffic; NAT metrics alarmed.

## Checked

- Date: 2026-10-28
- Confirmed: an IGW route to 0.0.0.0/0 and a public IPv4 or IPv6 address make a subnet public; a public NAT gateway sits in a public subnet with an Elastic IP; Azure NAT Gateway allocates SNAT ports dynamically (AWS and Azure NAT pages).
- Removed: egress-only IGW remark, per-AZ failure and cross-AZ charge claims (kept only as marked design judgement), 16 IP / 64k port figures, default-outbound retirement, per-GB billing, ErrorPortAllocation, gateway-endpoint pricing.

Method: documentation only; no commands were run.
