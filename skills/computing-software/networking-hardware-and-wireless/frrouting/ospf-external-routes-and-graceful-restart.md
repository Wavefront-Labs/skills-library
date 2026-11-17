---
id: computing-software.networking-hardware-and-wireless.frrouting.ospf-external-routes-and-graceful-restart
name: ospf-external-routes-and-graceful-restart
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, ospfd, ospf, redistribute, default-information, summary-address, graceful-restart, helper]
level: advanced
status: docs-checked
description: "Redistribute routes into FRR OSPFv2, originate a default route, summarise externals, set distance, and configure graceful restart as restarter and helper."
sources:
  - https://docs.frrouting.org/en/latest/ospfd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPFv2 external routes and graceful restart
Redistribution:
- `redistribute <babel|bgp|connected|eigrp|isis|kernel|openfabric|ospf|rip|sharp|static|table> [metric-type (1-2)] [metric (0-16777214)] [route-map WORD]`.
- `default-information originate [always] [metric (0-16777214)] [metric-type (1|2)] [route-map WORD]`; `always` advertises even with no default route.
- `default-metric (0-16777214)`; `distribute-list NAME out PROTOCOL`.
- `distance (1-255)` or `distance ospf intra-area|inter-area|external (1-255)`.
- `summary-address A.B.C.D/M [tag N]` or `... no-advertise`; `aggregation timer (5-1800)` default 5 s; `show ip ospf summary-address [detail]`.
- `set metric [+|-]N` is a route-map action.

Graceful restart:
- Restarter: `graceful-restart [grace-period (1-1800)]` default 120 s; run `graceful-restart prepare ip ospf` in EXEC mode before a planned restart.
- Helper (default disabled): `graceful-restart helper enable [A.B.C.D]`, `helper strict-lsa-checking` (default on), `helper supported-grace-time (10-1800)`, `helper planned-only` (default is planned and unplanned).
- `ip ospf graceful-restart hello-delay (1-1800)` default 10 s.

## Checked

2026-11-04. Confirmed against the FRR OSPFv2 page: redistribute, default-information, default-metric, distribute-list, distance, summary-address, aggregation timer, graceful-restart restarter and helper options and defaults, hello-delay. Removed the graceful-restart helper show command, which is not on the page.
Method: documentation only; no commands were run.
