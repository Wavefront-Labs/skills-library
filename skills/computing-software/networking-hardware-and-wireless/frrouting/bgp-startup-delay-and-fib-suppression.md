---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-startup-delay-and-fib-suppression
name: bgp-startup-delay-and-fib-suppression
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, update-delay, advertisement-delay, suppress-fib-pending, end-of-rib]
level: advanced
status: docs-checked
description: "Delay BGP best-path and advertisements after FRR startup with update-delay and advertisement-delay; hold them with suppress-fib-pending."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP startup delay and FIB suppression
- `bgp update-delay MAX-DELAY [ESTABLISH-WAIT]` (global) or `update-delay MAX-DELAY [ESTABLISH-WAIT]` (per instance or VRF) holds best-path and advertisements until peers send End-of-RIB or max-delay expires. Global and per-VRF forms are mutually exclusive. Default 0 (off).
- `bgp advertisement-delay (1-3600)` (global) or `advertisement-delay (1-3600)` (per VRF) holds only advertisements, so local forwarding works immediately. Combined with update-delay, release happens at the later of the two timers. The per-VRF form is also triggered by a peer in another VRF, so enable it only where needed.
- `bgp suppress-fib-pending [(0-10000)]` holds advertisement until the FIB install, for newly learned peer routes; global or per-instance. Default delay 1000 ms; `0` disables batching.
- `bgp send-extra-data zebra` sends AS-path, communities and path-selection reason to zebra (default off).
- `bgp allow-martian-nexthop` accepts martian next hops instead of rejecting and resetting (replaces `debug bgp allow-martian`).
- `bgp conditional-advertisement timer (5-240)` scan interval is covered in the conditional-advertisement skill.

## Checked
2026-11-09. Partial read of docs.frrouting.org bgp.html (one large page): the update-delay and advertisement-delay sections (global and per-VRF), suppress-fib-pending, send-extra-data zebra and allow-martian-nexthop with the deprecated debug bgp allow-martian note. Nothing removed.
Method: documentation only; no commands were run.
