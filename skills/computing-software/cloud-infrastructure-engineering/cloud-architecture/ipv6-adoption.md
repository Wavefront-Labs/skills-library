---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.ipv6-adoption
name: ipv6-adoption
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, ipv6-adoption, dual-stack, ipv6-only, nat64, dns64, public-ipv4-exhaustion]
level: advanced
status: draft
description: "Plan IPv6 adoption in cloud networks: dual-stack vs IPv6-only subnets, address allocation, NAT64/DNS64, security groups, service support gaps and IPv4 cost reduction."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html", "https://learn.microsoft.com/azure/virtual-network/ip-services/ipv6-overview", "https://cloud.google.com/vpc/docs/subnets#ipv6-ranges", "https://datatracker.ietf.org/doc/html/rfc6146"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IPv6 adoption in cloud networks

## Why now
Public IPv4 addresses are charged (AWS charges per public IPv4 per hour since Feb 2024), private
RFC 1918 space runs out in large estates, and mobile/consumer clients are increasingly IPv6.

## Options
- **Dual-stack**: resources get IPv4 + IPv6; easiest migration path.
- **IPv6-only subnets** (AWS supports IPv6-only subnets and instances on Nitro): reach IPv4-only
  destinations via **NAT64 + DNS64** (NAT gateway with DNS64 on the Route 53 Resolver).
- **Ingress only**: dual-stack load balancers/CDN in front of IPv4 backends.

## Steps
1. Get provider-assigned /56 per VPC (AWS) or BYOIP IPv6; plan /64 per subnet (subnet size fixed).
2. Update route tables (`::/0` to internet gateway for public, egress-only IGW for outbound-only).
3. Security groups/NSGs/firewall rules need explicit IPv6 entries - IPv4 rules do not cover IPv6.
4. Check service support matrix (some managed services, endpoints, VPN types are IPv4-only).
5. Applications: no IPv4 literals, parse/log IPv6 addresses, socket binding to `::`.
6. Start with load balancers and new workloads; measure.

## Gotchas
- IPv6 addresses are globally routable; "private" means no inbound route (egress-only IGW), not
  non-routable space.
- Logging pipelines and WAF rules with IPv4-only regexes.
- Overlooking IPv6 in firewall rules creates an open path.

## Verify
- [ ] Inbound IPv6 blocked except via intended ingress (scan).
- [ ] Public IPv4 count and cost trending down.
