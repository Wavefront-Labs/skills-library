---
id: computing-software.systems-network-administration.network-design.local-internet-breakout-vs-backhaul
name: local-internet-breakout-vs-backhaul
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, local-internet-breakout, backhaul, sase, sd-wan, direct-internet-access, wan-design]
level: practitioner
status: docs-checked
description: "Decide whether branches send internet and SaaS traffic out locally or backhaul it to a hub, and how to secure local breakout with SASE/SSE or branch firewalls."
sources:
  - https://learn.microsoft.com/en-us/microsoft-365/enterprise/microsoft-365-network-connectivity-principles
  - https://www.cisco.com/c/en/us/td/docs/solutions/CVD/SDWAN/cisco-sdwan-design-guide.html
  - https://www.gartner.com/en/information-technology/glossary/secure-access-service-edge-sase
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local internet breakout vs backhaul

## Backhaul (centralised internet)
All branch internet traffic rides MPLS/VPN to a hub with the central firewall/proxy.
- Pros: one security stack, simple logging, one set of public IPs.
- Cons: hub bandwidth and latency added to every SaaS session (SaaS sessions degrade); hub
  outage = everyone's internet down; MPLS bandwidth spent on internet traffic.

## Local breakout
Branch sends internet/SaaS straight out its local link.
- Pros: lowest latency to SaaS front doors (Microsoft's Microsoft 365 connectivity principles say to egress connections locally, with local DNS, to reduce latency), offloads WAN.
- Cons: security must exist at each branch: branch NGFW, or SSE/SASE cloud proxy (tunnel or
  agent), DNS security; more public egress IPs to allow-list at SaaS vendors.

## Hybrid (common)
- Trusted SaaS (for example Microsoft 365) -> local breakout direct, using vendor endpoint feeds
  for app-aware routing in SD-WAN.
- General web -> SSE cloud via IPsec/GRE from the branch edge.
- Internal apps -> overlay to DC or ZTNA.
- Fallback to backhaul if the local link fails.

## Checks
- Tenant restrictions/egress IP allow-listing for SaaS that pin to known IPs.
- Logging and DLP coverage in the chosen model.
- Split DNS: resolve SaaS via a local/nearby resolver so geo-DNS picks the nearest front door.

## Verify
- [ ] Per-application path documented; latency to SaaS front doors from branches measured before and after.

## Checked

- Date: 2026-10-28
- Confirmed: Microsoft 365 network connectivity principles: local DNS and internet egress reduce connection latency; Cisco SD-WAN design guide: backhauling internet/SaaS traffic has bandwidth and latency issues, and Secure Direct Internet Access offloads internet traffic locally.
- Removed: vendor lists (Zoom, Webex, Optimize category wording) and the Gartner SASE reference (page blocked).
Method: documentation only; no commands were run.
