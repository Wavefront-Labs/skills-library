---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-conditional-advertisement
name: bgp-conditional-advertisement
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, conditional-advertisement, advertise-map, exist-map, non-exist-map, add-path]
level: advanced
status: docs-checked
description: "Advertise BGP prefixes in FRR only if another prefix exists or not (advertise-map with exist-map or non-exist-map), and send Add-Path paths."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP conditional advertisement and Add-Path
Conditional advertisement:
- `neighbor A.B.C.D advertise-map NAME [exist-map|non-exist-map] NAME` advertises based on the presence of prefixes in another table.
- `bgp conditional-advertisement timer (5-240)` sets the scanner interval (default 60 s).
- `neighbor PEER advertisement-interval` is ignored during conditional advertisement.
- `debug bgp conditional-advertisement`.

Add-Path (per neighbor):
- `addpath-tx-all-paths` sends all known paths.
- `addpath-tx-bestpath-per-AS` sends the best path per AS.
- `addpath-tx-best-selected (1-6)` calculates and sends N best paths.
- `disable-addpath-rx` stops accepting additional paths.
- `addpath-rx-paths-limit (1-65535)` caps paths received via the PATHS-LIMIT capability (both peers must support it).

Default-originate is a related, simpler condition: with a route-map containing `match` clauses it is originated only when they hold (see the route-origination skill).

## Checked
2026-11-09. Partial read of docs.frrouting.org bgp.html (one large page): the conditional advertisement section (advertise-map, exist-map, non-exist-map, scanner timer 5 to 240 default 60 s), the advertisement-interval note, the Add-Path neighbor commands and debug bgp conditional-advertisement. Nothing removed.
Method: documentation only; no commands were run.
