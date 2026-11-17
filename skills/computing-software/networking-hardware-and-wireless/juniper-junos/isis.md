---
id: computing-software.networking-hardware-and-wireless.juniper-junos.isis
name: isis
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, isis, is-is, isis-levels, iso-address]
level: practitioner
status: draft
description: "Configure Junos IS-IS with ISO NET, levels, wide metrics and verify adjacencies and the link-state database."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IS-IS configuration
Goal: run IS-IS as the IGP.

```
set interfaces lo0 unit 0 family iso address 49.0001.0100.2550.0001.00
set interfaces xe-0/0/3 unit 0 family iso
set protocols isis interface xe-0/0/3.0 point-to-point
set protocols isis interface lo0.0 passive
set protocols isis level 1 disable
set protocols isis level 2 wide-metrics-only
set protocols isis reference-bandwidth 100g
```

```
user@host> show isis adjacency
user@host> show isis database detail
user@host> show isis interface
```

- Each router needs `family iso` on the interfaces and a NET on lo0 (area.systemid.sel).
- Level 1 and Level 2 behave like intra- and inter-area; many networks run L2 only.
- Use `wide-metrics-only` for TE and large metrics.

Gotcha: forgetting `family iso` on the link means no adjacency but no error message. Also a `family mpls` is needed separately for LDP/RSVP.

Operational tip: set `overload` on a router during maintenance (`set protocols isis overload timeout 300`) so other routers avoid transit through it while it converges.

## Verify
- `show isis adjacency` is `Up` for the expected Level; `show route protocol isis` is populated.
