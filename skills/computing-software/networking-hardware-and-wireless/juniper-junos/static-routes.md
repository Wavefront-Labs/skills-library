---
id: computing-software.networking-hardware-and-wireless.juniper-junos.static-routes
name: static-routes
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, static-routes, static-route, qualified-next-hop, floating-static]
level: practitioner
status: draft
description: "Configure static, floating static, qualified next-hop and aggregate/generated routes in Junos."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static and aggregate routes
Goal: simple routing with explicit preference.

```
set routing-options static route 0.0.0.0/0 next-hop 198.51.100.2
set routing-options static route 0.0.0.0/0 qualified-next-hop 203.0.113.2 preference 200
set routing-options static route 10.20.0.0/16 next-hop 192.0.2.2 no-readvertise
set routing-options static route 10.99.0.0/16 discard
set routing-options aggregate route 10.0.0.0/8
set routing-options router-id 10.255.0.1
```

- Default preference: static 5, OSPF internal 10, IS-IS L1 15, RIP 100, BGP 170 (lower wins).
- `discard` drops; `reject` drops with ICMP unreachable.
- `static route ... next-hop <if>` on multi-access Ethernet needs an address, not just the interface.
- Add BFD with `bfd-liveness-detection minimum-interval 300` (confirm support for static routes on your platform).

Gotcha: a static route whose next-hop is unresolvable is hidden, not an error. Look in `show route hidden` before assuming the commit failed.

Operational tip: prefer a qualified-next-hop with a higher preference for backups rather than two equal statics, unless you want load sharing, and document why each static exists.

## Verify
- `show route 0.0.0.0/0 exact` shows the active route marked `*` with preference 5.
