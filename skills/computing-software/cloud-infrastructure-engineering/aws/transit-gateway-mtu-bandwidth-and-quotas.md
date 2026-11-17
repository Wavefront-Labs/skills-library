---
id: computing-software.cloud-infrastructure-engineering.aws.transit-gateway-mtu-bandwidth-and-quotas
name: transit-gateway-mtu-bandwidth-and-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transit-gateway, tgw-mtu, tgw-bandwidth, tgw-quotas, ecmp]
level: advanced
status: docs-checked
description: "Design within Transit Gateway MTU (8500 vs 1500 for VPN), per-attachment bandwidth and packet limits, ECMP for VPN throughput and key quotas."
sources: ["https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-quotas.html", "https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-cloudwatch-metrics.html", "https://docs.aws.amazon.com/vpc/latest/tgw/tgw-best-design-practices.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transit Gateway MTU, bandwidth and quotas

## 1. MTU
| Path | Max MTU |
|---|---|
| VPC, Direct Connect, TGW Connect, peering attachments (intra-Region, inter-Region, Cloud WAN) | 8,500 bytes |
| Site-to-Site VPN attachment | 1,500 bytes |
The transit gateway enforces MSS clamping for all packets. Jumbo frames (9,001) from instances need the path
MTU at 8,500 or lower. PMTUD is supported for traffic ingressing on VPC and Connect attachments (the gateway
generates FRAG_NEEDED for ICMPv4 and Packet Too Big for ICMPv6) but not on Site-to-Site VPN, Direct Connect or
peering attachments, so set the instance MTU explicitly on those paths. When migrating from VPC peering, update
both VPCs together: an MTU mismatch can drop jumbo packets asymmetrically.

## 2. Bandwidth and packets
- VPC attachment: up to 100 Gbps each direction per Availability Zone; up to 7,500,000 packets per second per
  VPC attachment per AZ.
- Direct Connect gateway and peering attachments: up to 100 Gbps each direction per available AZ in the Region,
  up to 7,500,000 packets per second.
- Connect peer (GRE tunnel): up to 5 Gbps and 300,000 packets per second; up to 4 peers per Connect attachment
  (up to 20 Gbps per attachment).
- VPN tunnel limits are on the Site-to-Site VPN bandwidth page. Use **ECMP** across multiple VPN tunnels for
  more bandwidth; the VPN connection must use dynamic routing (ECMP is not supported with static routing).

## 3. Quotas worth tracking
| Item | Default |
|---|---|
| Transit gateways per account per Region | 5 |
| Attachments per TGW | 5,000 |
| Route tables per TGW | 20 |
| Total routes across route tables | 10,000 |
| Peering attachments per TGW | 50 |
| Transit gateways per VPC | 5 (not adjustable) |
Read live values in the Service Quotas console (or `aws service-quotas list-services` to find the service code, then
`list-service-quotas`); some quotas, such as total routes (10,000), need your account team to raise.

## 4. Monitoring
CloudWatch `AWS/TransitGateway` includes `BytesIn`, `PacketDropCountBlackhole`, `PacketDropCountNoRoute`,
`PacketDropCountNoPolicy` and `PacketDropCountTTLExpired`, with per-attachment dimensions. Drops with no route
usually mean a missing propagation, association or route.

## Verify
- [ ] `ping -M do -s 8472 <remote>` (Linux) succeeds across a VPC attachment; `-s 1472` is the max over VPN.
- [ ] Alarm on `PacketDropCountNoRoute` > 0.

## Checked

Date: 2026-10-27. Sources: Amazon VPC Transit Gateways Guide pages "AWS Transit Gateway Quotas" and "Amazon CloudWatch metrics for Transit Gateway".
Confirmed: MTU 8500 for VPC, Direct Connect, Connect and peering attachments and 1500 for VPN; MSS clamping; PMTUD support limited to VPC and Connect attachments; 100 Gbps and 7,500,000 pps per AZ; ECMP requires dynamic routing; quotas of 5 gateways per account, 20 route tables, 10,000 total routes, 5,000 attachments, 50 peering attachments; metric names in AWS/TransitGateway.
Corrected: "Attachments per VPC 5" is documented as 5 transit gateways per VPC; the 100 Gbps figure is per direction, not "burst".
Removed: the 1.25 Gbps single-tunnel figure (the page defers to the VPN guide), the single-flow hashing claim and the hard-coded service code ec2.

Method: documentation only; no commands were run.
