---
id: computing-software.networking-hardware-and-wireless.frrouting.pim-igmp-multicast
name: pim-igmp-multicast
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, pimd, pim, igmp, multicast, rendezvous-point, bsr, msdp, ssm]
level: advanced
status: docs-checked
description: "Configure FRR pimd for multicast: PIM sparse mode on interfaces, static RP, BSR and AutoRP, SSM ranges, IGMP settings, static mroutes, MSDP peers and show commands."
sources:
  - https://docs.frrouting.org/en/latest/pim.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PIM, IGMP and MSDP
Instance (`router pim [vrf NAME]`; does not enable PIM by itself):
- `rp A.B.C.D A.B.C.D/M` static RP, one per range; `rp keep-alive-timer (1-65535)`.
- `bsr candidate-bsr [priority (0-255)]`, `bsr candidate-rp [interval]`, `bsr candidate-rp group A.B.C.D/M`; AutoRP discovery is on by default (`no autorp discovery` disables it).
- `ssm prefix-list WORD`; `spt-switchover infinity-and-beyond [prefix-list PLIST]`; `join-filter route-map NAME`.
- `rpf-lookup-mode urib-only|mrib-only|mrib-then-urib|lower-distance|longer-prefix` (default mrib-then-urib).
- `join-prune-interval (1-65535)` default 60 s; `ecmp [rebalance]`.

Interface:
- `ip pim [sm|dm|sm-dm]` default sm; `ip pim drpriority`, `ip pim hello`, `ip pim passive`, `ip pim bfd`, `ip pim use-source A.B.C.D`.
- `ip pim ssm prefix-list NAME` (default 232.0.0.0/8).
- IGMP: `ip igmp` (default version 3), `ip igmp version (2-3)`, `query-interval`, `query-max-response-time`, `immediate-leave`, `join-group`, `static-group`, `max-groups`, `robustness (1-255)` default 2, `access-list`, `route-map`.

Static mroute: `ip mroute PREFIX NEXTHOP [DISTANCE]` (RPF only, not installed in the kernel); interface-level `ip mroute INTERFACE A.B.C.D [A.B.C.D]` forwards matching group (and optional source) traffic arriving on that interface out of the named interface.

MSDP: `msdp peer A.B.C.D source A.B.C.D [as N]`, `msdp mesh-group WORD member|source`, `msdp timers` (keep-alive 60, hold 75, retry 30), `msdp originator-id`.

Show: `show ip pim interface|neighbor|rp-info|upstream|state|join`, `show ip igmp groups|sources|join`, `show ip mroute [summary|count]`, `show ip msdp peer`.

## Checked

2026-11-04. Confirmed against the FRR PIM page: router pim instance commands, rpf-lookup-mode values, interface PIM and IGMP commands and defaults, mroute, MSDP commands and timers, show commands. Fixed the candidate-RP command forms and the interface mroute syntax.
Method: documentation only; no commands were run.
