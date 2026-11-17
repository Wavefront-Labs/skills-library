---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-show-and-debug-commands
name: bgp-show-and-debug-commands
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, show-bgp, debug-bgp, clear-bgp, troubleshooting, update-groups]
level: practitioner
status: docs-checked
description: "Inspect and troubleshoot FRR BGP with show bgp summary, neighbors, advertised and received routes, nexthop, update-groups, clear bgp and the debug bgp variants."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP show, clear and debug commands
Show:
- `show [ip] bgp [all] summary [wide] [json]`; the afi/safi form accepts filters `failed`, `established`, `neighbor`, `remote-as`, `terse`.
- `show [ip] bgp [afi] [safi] [all] neighbors A.B.C.D [advertised-routes|received-routes|filtered-routes]`; `show bgp neighbors ADDR json`.
- `show bgp ipv4|ipv6 unicast PREFIX` for one prefix.
- `show [ip] bgp [vrf NAME] nexthop [ipv4|ipv6] [ADDR] [detail] [json]`.
- `show bgp update-groups [advertise-queue|advertised-routes|packet-queue]`.
- `show bgp ipv4|ipv6 flowspec [detail]`, `show bgp [ipv4|ipv6] unreachability [PREFIX] [detail] [summary]`.
- `show debug` lists enabled debugs.

Clear:
- `clear bgp *`, `clear bgp ipv4|ipv6 ASNUM`.
- `clear bgp ipv4|ipv6 PEER [soft|in|out]`.
- `clear bgp [ipv4|ipv6] [unicast] PEER|* message-stats|capabilities`.

Debug:
- `debug bgp neighbor-events [detail]`, `debug bgp keepalives [PEER]`.
- `debug bgp updates [detail]` or `debug bgp updates in|out [PEER [prefix-list WORD]]`.
- `debug bgp bestpath PREFIX`, `debug bgp nht`, `debug bgp update-groups`, `debug bgp zebra`, `debug bgp bfd`.
- `debug bgp conditional-advertisement`, `debug bgp aggregate [prefix PREFIX]`, `debug bgp flowspec`, `debug bgp pbr [error]`, `debug bgp linkstate`.

`(Policy)` in the PfxRcd or PfxSnt column of `show bgp summary` means the eBGP default policy is on and no filter is applied in that direction. The `show ip bgp` form may be removed; prefer `show bgp [afi] [safi]`.

## Checked

2026-11-09. Read the FRR BGP page "Displaying BGP Information" (summary, neighbors, routes, nexthop, update-groups), "Other BGP Commands" (clear bgp), the debug command list and the flowspec, linkstate and unreachability sections via a local text copy; every command and filter above matches. Added the `(Policy)` and deprecation notes.
Method: documentation only; no commands were run.
