---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-igmp-snooping-and-multicast
name: sw-igmp-snooping-and-multicast
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [igmp-snooping, igmp-querier, pim-sparse-mode, sw-multicast-qos-hw]
level: practitioner
status: draft
description: "Prevent multicast flooding with IGMP snooping and a querier, and understand PIM sparse mode between routers."
sources:
  - https://www.rfc-editor.org/rfc/rfc3376
  - https://www.rfc-editor.org/rfc/rfc7761
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multicast basics

- Without IGMP snooping, switches flood multicast to all ports in the VLAN. Snooping listens to IGMP joins and forwards only to interested ports.
- A VLAN with snooping but no router needs an IGMP querier configured, otherwise memberships time out and streams stop.
- Between VLANs/sites, PIM sparse mode builds trees using a rendezvous point (RP); define the RP statically, via anycast RP or BSR. Source-specific multicast (SSM, 232/8) removes the RP dependency.
- Wi-Fi: multicast is sent at low rates; enable multicast-to-unicast conversion for video where available.

## Verify
- [ ] `show ip igmp snooping groups` lists the expected ports and no stream floods unrelated ports.
