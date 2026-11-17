---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-stacking-vs-mlag-vs-chassis
name: sw-stacking-vs-mlag-vs-chassis
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [switch-stacking, mlag-vpc, virtual-chassis, sw-stacking-mlag]
level: advanced
status: draft
description: "Choose between stacking, MLAG, virtual chassis and chassis with redundant supervisors by failure domain and upgrade impact."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Redundancy models

- Stacking: members act as one logical switch with one control plane (single management IP). Simple, but the whole stack is one failure/upgrade domain.
- MLAG / vPC: two independent switches present a single LAG to downstream devices; each keeps its own control plane, so upgrades can be staggered. Needs a peer link and keepalive; design for peer-link failure behaviour.
- Virtual chassis (Junos) and VSS (Cisco) merge two chassis into one logical switch.
- Chassis with dual supervisors gives in-service upgrade options on some platforms.
- Decide by: failure blast radius, upgrade windows, cabling distance, licensing, and operational familiarity.

## Verify
- [ ] Failover test: pull a member/peer and measure traffic loss and recovery; document expected values.
