---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-capacity-and-density-design
name: wifi-capacity-and-density-design
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-capacity-planning, high-density-wifi, cell-sizing]
level: advanced
status: draft
description: "Size AP counts for throughput and client density, shrink cells with power and rates, and plan high-density venues."
sources:
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capacity design

- Coverage design alone is not capacity design. Estimate concurrent clients, per-client throughput, and airtime available per channel.
- Smaller cells with lower power and higher minimum rates allow more channel reuse; fewer SSIDs reduce overhead.
- Rules of thumb from vendors (e.g. 25-50 active clients per radio) vary by traffic; validate with load tests.
- Venue designs: directional or under-seat APs aimed to small zones, 20 MHz channels, strict channel reuse plan, 5 and 6 GHz-first client steering.
- Plan wired uplinks: multigig (2.5/5/10G) for Wi-Fi 6/7 APs, and PoE budget (see cabling/PoE skills).

## Verify
- [ ] Load test with representative clients shows per-client throughput meets the target at design density.
