---
id: computing-software.networking-hardware-and-wireless.arista-eos.pim-igmp-multicast
name: pim-igmp-multicast
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, multicast, pim, igmp-snooping, rp]
level: practitioner
status: draft
description: "Configure EOS IGMP snooping and PIM sparse mode with a static RP, and check mroute state."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multicast: IGMP snooping and PIM
Goal: forward multicast efficiently.

```
ip igmp snooping vlan 100
ip multicast-routing
router pim sparse-mode
   ip pim rp-address 10.255.0.254
interface Vlan100
   pim ipv4 sparse-mode
```

```
show ip igmp snooping groups
show ip mroute
show ip pim neighbor
show ip pim rp
```

- IGMP snooping is on by default on many platforms; a querier is needed if there is no PIM router in the VLAN (`ip igmp snooping querier`, confirm).
- Multicast over VXLAN depends on platform and design: confirm.

Gotcha: without an IGMP querier, snooping state ages out (about 260 s) and multicast streams stop.

Operational tip: draw out the RP location and group ranges, check `show ip pim rp` consistency across routers, and consider anycast RP with MSDP for resilience in larger designs (confirm support on platform). Verify receivers by joining a test group with a host tool (for example iperf with multicast) and confirm the outgoing interface list changes in `show ip mroute`.

## Verify
- `show ip mroute` shows (S,G) or (*,G) with the right incoming/outgoing interfaces.
