---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dns-architecture
name: dns-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, dns-architecture, hybrid-dns, private-dns-zones, route53-resolver, azure-dns-private-resolver, cloud-dns-forwarding, conditional-forwarding, private-endpoint-dns, split-horizon]
level: advanced
status: draft
description: "Design hybrid and private DNS: central resolver endpoints, conditional forwarding both ways, private zones for private endpoints, split-horizon names and avoiding resolution loops."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver.html", "https://learn.microsoft.com/azure/dns/private-resolver-hybrid-dns", "https://learn.microsoft.com/azure/private-link/private-endpoint-dns", "https://cloud.google.com/dns/docs/best-practices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hybrid and private DNS architecture

## Pattern
1. **Central DNS in the hub/network account**: inbound endpoints (on-prem → cloud) and outbound
   endpoints (cloud → on-prem): Route 53 Resolver endpoints + rules shared via RAM; Azure DNS
   Private Resolver with forwarding rulesets linked to spokes; Cloud DNS inbound server policy and
   forwarding zones in a hub VPC with DNS peering from spokes.
2. **On-prem DNS** conditionally forwards cloud zones (`aws.corp.example`, `privatelink.*` zones)
   to the inbound endpoints. **Cloud** forwards `corp.example` to on-prem DNS.
3. **Private zones** associated with all VPCs/VNets that need them (Route 53 private hosted zone
   associations across accounts; Azure private DNS zones linked to VNets; Cloud DNS private zones
   with network bindings).
4. **Private endpoints**: Azure Private Link needs `privatelink.<service>` zones (e.g.
   `privatelink.blob.core.windows.net`) centralised and linked — one zone per service org-wide,
   otherwise resolution splits. AWS interface endpoints use private DNS on the VPC or shared PHZs.
5. **Split-horizon**: same name resolving to private IPs internally and public externally — keep
   records consistent via IaC.

## Gotchas
- Forwarding loops (on-prem forwards to cloud forwards back) — document zone ownership.
- Per-VPC Resolver query limits (e.g. 1024 packets/s per ENI on AWS) — high-volume DNS needs caching.
- TTLs too high slow failovers; too low raise query load/cost.

## Verify
- [ ] Resolution matrix test: on-prem → private endpoint name; cloud → on-prem name; spoke → spoke.
- [ ] One private DNS zone per privatelink service across the estate.
