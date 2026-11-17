---
id: computing-software.systems-network-administration.network-design.dedicated-internet-access-vs-broadband
name: dedicated-internet-access-vs-broadband
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wan-design, dedicated-internet-access, broadband, sla, contention-ratio]
level: practitioner
status: draft
description: "Choose between dedicated internet access and business broadband per site: symmetry, contention, SLA and MTTR, static IPs, BGP, lead times and cost."
sources:
  - https://www.mef.net/service-standards/
  - https://www.ofcom.org.uk/phones-and-broadband/coverage-and-speeds
  - https://www.cisco.com/c/en/us/td/docs/solutions/CVD/SDWAN/cisco-sdwan-design-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dedicated internet access vs broadband

| | DIA (leased line, Ethernet access) | Business broadband (FTTP, cable, DSL, FWA) |
|---|---|---|
| Bandwidth | symmetric, uncontended, committed | asymmetric often, contended (shared) |
| SLA | availability (99.9-99.99 %), latency, fix time (4-8 h) | best effort, next business day |
| Static IPs / BGP | yes, IP blocks, BGP with full/default routes | few statics, no BGP usually |
| Lead time | 30-90+ days (excess construction) | days to weeks |
| Cost | high per Mbps | low |
| Handoff | Ethernet on NTU/demarc, SFP | CPE router, PPPoE/DHCP |

## Decide per site
- Hosting inbound services, VPN head-end, many users, voice-critical -> DIA (two for HQ/DC, diverse).
- Small branch with SaaS traffic, SD-WAN steering -> two broadband links from different carriers and
  media (FTTP + 5G) often beat one DIA on availability and cost.
- Need BGP/PI announcements -> DIA.

## Questions for the carrier
Port speed vs CIR, burst; diverse entry and separate exchange; MTTR and SLA credits; IPv6; static
block size; who manages the CPE; DDoS protection option; contract term and early termination.

## Verify
- [ ] Site sheet records circuit type, CIR, SLA, diverse path evidence and support contacts; a monitoring probe measures latency/loss per circuit.
