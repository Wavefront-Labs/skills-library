---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.egress-control
name: egress-control
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, egress-control, centralised-egress, egress-filtering, network-firewall, azure-firewall, cloud-ngfw, fqdn-filtering, inspection-vpc, nat-centralisation]
level: advanced
status: draft
description: "Control outbound traffic: centralised vs distributed egress, FQDN allow-lists on managed firewalls, inspection hub routing, DNS exfiltration and cost trade-offs."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/centralized-egress-to-internet.html", "https://learn.microsoft.com/azure/firewall/overview", "https://cloud.google.com/firewall/docs/about-firewalls"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Centralised egress and inspection

Most attacks need outbound connectivity (C2, exfiltration, downloading tooling). Default-allow
egress to the internet is the common gap.

## Designs
- **Centralised**: spokes route `0.0.0.0/0` to a hub/inspection VPC (Transit Gateway → AWS Network
  Firewall → NAT; Azure hub with Azure Firewall and UDRs; GCP hub with Cloud NGFW / NVAs). One
  policy, one set of egress IPs to allow-list at partners. Costs: TGW/firewall processing per GB.
- **Distributed**: NAT + firewall per VPC. Lower latency and blast radius, more to manage.
- Hybrid: centralise internet egress, keep provider-service traffic on endpoints (not through the firewall).

## Policy
1. Default deny outbound from workload subnets; allow by **FQDN/SNI** (package repos, SaaS APIs) —
   AWS Network Firewall domain lists, Azure Firewall application rules, Cloud NGFW FQDN objects, or an egress proxy.
2. Kubernetes: egress network policies + egress gateways for stable source IPs.
3. Block instance metadata abuse paths and DNS exfiltration (DNS firewall: Route 53 Resolver DNS Firewall, Azure DNS security policy, Cloud DNS response policies).
4. Log all denied and allowed flows to the SIEM.

## Gotchas
- TLS inspection breaks certificate pinning and adds cost; SNI-based filtering is often enough.
- Firewalls are now in the path of everything: deploy per-AZ, monitor throughput, plan failure mode (fail closed vs open).

## Verify
- [ ] `curl https://example.org` from a workload subnet fails unless allow-listed.
- [ ] Egress IPs documented for partners.
