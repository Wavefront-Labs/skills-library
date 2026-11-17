---
id: computing-software.networking-hardware-and-wireless.frrouting.ospf-process-and-areas
name: ospf-process-and-areas
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, ospfd, ospf, areas, stub, nssa, virtual-link, area-range, spf-throttle]
level: practitioner
status: docs-checked
description: "Configure the FRR ospfd process and areas: router-id, network area, stub and NSSA, area ranges, virtual links, reference bandwidth, SPF throttle timers and show commands."
sources:
  - https://docs.frrouting.org/en/latest/ospfd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPFv2 process and areas
Process:
- `router ospf [(1-65535)|vrf NAME]` (multiple instances do not support vrf); `ospf router-id A.B.C.D` (from zebra if unset).
- `network A.B.C.D/M area AREA` (cannot mix with `ip ospf area`); `passive-interface default`.
- `auto-cost reference-bandwidth (1-4294967)` Mbit/s, default 100; must match domain-wide.
- `timers throttle spf DELAY INIT-HOLD MAX-HOLD` (0-600000 ms each); `timers throttle lsa all (0-5000)` default 5000; `timers lsa min-arrival (0-5000)` default 1000.
- `maximum-paths (1-64)` default 64; `max-metric router-lsa [on-startup (5-86400)|on-shutdown (5-100)|administrative]`.
- `shutdown` keeps config; `log-adjacency-changes [detail]`; `ospf abr-type cisco|ibm|shortcut|standard`.

Areas (`AREA` is dotted or 0-4294967295):
- `area AREA stub [no-summary]`, `area AREA nssa [suppress-fa]`, `area AREA default-cost (0-16777215)`.
- `area AREA range A.B.C.D/M [advertise [cost N]|not-advertise|substitute A.B.C.D/M]`.
- `area AREA virtual-link A.B.C.D`.
- `area AREA import-list|export-list NAME`, `area AREA filter-list prefix NAME in|out`.

Show: `show ip ospf [vrf NAME|all] [json]`, `show ip ospf interface`, `show ip ospf neighbor [detail]`, `show ip ospf database`, `show ip ospf route`, `show ip ospf border-routers`.

## Checked

2026-11-08. Read the area, process and show sections of the FRR OSPFv2 page: router ospf forms, router-id, network and interface-area mixing rule, reference bandwidth, throttle and LSA timers with defaults, maximum-paths, max-metric, abr-type, stub, NSSA, range, virtual-link, filter lists, show commands. Nothing changed.
Method: docs-only read of cited pages, 2026-11-08
