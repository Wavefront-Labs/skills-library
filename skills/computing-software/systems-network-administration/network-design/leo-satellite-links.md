---
id: computing-software.systems-network-administration.network-design.leo-satellite-links
name: leo-satellite-links
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, leo-satellite, starlink, satellite-wan, cgnat, wan-backup]
level: practitioner
status: draft
description: "Use LEO satellite (Starlink, OneWeb) for sites and backup: latency and throughput expectations, obstructions, CGNAT and inbound access, outages during handovers, and SD-WAN use."
sources:
  - https://www.starlink.com/business
  - https://www.starlink.com/support
  - https://oneweb.net/resources
  - https://www.rfc-editor.org/rfc/rfc6598
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LEO satellite links

## Characteristics
- Latency 25-60 ms (vs ~600 ms GEO), jitter higher than terrestrial; brief drops (sub-second to
  seconds) during satellite handovers and obstructions.
- Throughput tens to hundreds of Mbps down, lower up; varies with cell congestion and plan.
- Addressing: Starlink residential/business standard uses **CGNAT** (100.64.0.0/10) for IPv4 with
  native IPv6 prefix delegation; public IPv4 only on some business plans. Inbound IPv4 services
  and site-to-site VPN responders need workarounds (initiate tunnels outbound, use IPv6, or get a
  public IP plan).

## Site design
- Dish placement with clear sky view; use the app's obstruction map; mounts on roofs/poles; heater
  power use in snow regions.
- Power: dish + router 50-150 W; on UPS if it is the backup path.
- Bypass the provider router (bypass mode) to put your firewall/SD-WAN edge directly on the link.
- Pair with another transport (fibre/DSL/5G) under SD-WAN: steer real-time traffic away during
  measured loss, use FEC/packet duplication.

## Typical uses
Remote sites with no fibre, construction and events, maritime/aviation, and diverse backup for
branches (different failure modes from terrestrial cuts).

## Operating
Monitor with the provider API/app plus your own probes (loss, latency, jitter); expect monthly
data caps/priority data on some plans; check terms for fixed-site vs mobile use.

## Verify
- [ ] Obstruction stats near zero, SD-WAN SLA probes show loss within policy, VPN tunnels re-establish automatically after outages.
