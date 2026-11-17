---
id: computing-software.networking-hardware-and-wireless.frrouting.bfd-peers-and-integration
name: bfd-peers-and-integration
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bfdd, bfd, multihop, echo-mode, profile, authentication, static-route-bfd]
level: practitioner
status: docs-checked
description: "Configure FRR bfdd peers and profiles with timers, echo, passive and demand modes, authentication, and enable BFD from BGP, OSPF, IS-IS, PIM, RIP and static routes."
sources:
  - https://docs.frrouting.org/en/latest/bfd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BFD peers and protocol integration
Peers (`bfd` node): `peer ADDR [multihop|local-address ADDR|interface IFNAME|vrf NAME]` (local address mandatory for IPv6); `profile WORD`; `shutdown`.

Peer or profile settings:
- `detect-multiplier (1-255)` default 3.
- `receive-interval` and `transmit-interval (10-4294967)` default 300 ms.
- `echo-mode` (off by default, not on multihop; without a distributed data plane only works when the peer is also FRR); `echo receive-interval` and `echo transmit-interval` default 50 ms.
- `passive-mode`; `demand-mode` (works with multihop; pair with echo mode); `minimum-ttl (1-254)` multihop only, default 254; `log-session-changes`.
- `authentication key-chain NAME` (cleartext or hmac-sha1) and `authentication algorithm meticulous`.
- Multihop expects TTL below 254 and port 4784.

Enable from protocols:
- BGP: `neighbor X bfd`, `bfd profile`, `bfd strict [hold-time N]`, `bfd check-control-plane-failure`.
- OSPF: `ip ospf bfd [quick]`; OSPFv3 `ipv6 ospf6 bfd`; IS-IS `isis bfd`; PIM `ip pim bfd`; RIP `ip rip bfd`.
- Static: `ip route A.B.C.D/M A.B.C.D bfd [multi-hop|source ADDR|profile NAME]`.

Show: `show bfd [vrf NAME] peers [brief] [json]`, `show bfd peer ADDR`, `show bfd peers counters`, `show bfd static route`; `clear bfd peers counters`.

bfdd options: `--dplaneaddr TYPE:ADDRESS[:PORT]` (default port 50700), `--vrfs LIST`.

## Checked

2026-11-04. Confirmed against the FRR BFD page: peer and profile commands and defaults, echo, demand and passive modes, minimum-ttl, authentication, per-protocol BFD commands, static route BFD, show commands, --dplaneaddr and --vrfs. Nothing changed.
Method: documentation only; no commands were run.
