---
id: computing-software.cloud-infrastructure-engineering.aws.ipv6-only-egress-with-dns64-and-nat64
name: ipv6-only-egress-with-dns64-and-nat64
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ipv6, nat64, dns64, egress-only-internet-gateway, ipv6-only-subnets]
level: advanced
status: docs-checked
description: "Run IPv6-only subnets that still reach IPv4 services using DNS64 on the subnet and NAT64 through a NAT gateway, plus egress-only internet gateways for IPv6."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-nat64-dns64.html", "https://docs.aws.amazon.com/vpc/latest/userguide/egress-only-internet-gateway.html", "https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6-only egress with DNS64 and NAT64

## 1. Build the subnet
```bash
aws ec2 create-subnet --vpc-id vpc-0abc --ipv6-native --ipv6-cidr-block 2600:1f18:abcd:1200::/64 --availability-zone <AZ>
aws ec2 modify-subnet-attribute --subnet-id subnet-0v6 --enable-dns64
```
Resources in an IPv6-only subnet must communicate over IPv6.

## 2. Routes
```bash
EIGW=$(aws ec2 create-egress-only-internet-gateway --vpc-id vpc-0abc --query EgressOnlyInternetGateway.EgressOnlyInternetGatewayId --output text)
aws ec2 create-route --route-table-id rtb-v6 --destination-ipv6-cidr-block ::/0 --egress-only-internet-gateway-id $EIGW
aws ec2 create-route --route-table-id rtb-v6 --destination-ipv6-cidr-block 64:ff9b::/96 --nat-gateway-id nat-0abc
```
- Native IPv6 destinations go out the egress-only IGW (stateful, no inbound initiation).
- IPv4-only destinations: the Route 53 Resolver (DNS64) synthesises an AAAA `64:ff9b::<ipv4>`; traffic to
  `64:ff9b::/96` hits the public NAT gateway, which translates to IPv4 (NAT64).

## 3. Things that break
- Hard-coded IPv4 literals (no DNS lookup, no synthesis): fix the config to use names.
- Software that only opens AF_INET sockets.
- Custom DNS servers bypass DNS64 unless they implement it.
- AWS service endpoints: use dual-stack endpoints or interface endpoints with IPv6 (confirm per service).

## Verify
- [ ] A lookup of an IPv4-only name from the instance returns an AAAA record inside `64:ff9b::/96`.
- [ ] A connection to an IPv4-only site works through NAT64; the NAT gateway's byte metrics rise.

## Checked
2026-10-31. Confirmed in the NAT64/DNS64, egress-only internet gateway and subnet configuration pages: DNS64 is enabled per subnet and Route 53 Resolver synthesizes AAAA records with 64:ff9b::/96; the `64:ff9b::/96` route to a NAT gateway placed in a separate public subnet; the egress-only internet gateway is stateful; IPv6-only subnets must use IPv6. CLI flags (`--ipv6-native`, `--enable-dns64`, egress-only route flags) were checked with check_commands against the botocore model. Removed as unconfirmed: the Nitro requirement, `*.api.aws` endpoint naming, the ipv4only.arpa answer and the NAT metric name.
Method: documentation only; no commands were run.
