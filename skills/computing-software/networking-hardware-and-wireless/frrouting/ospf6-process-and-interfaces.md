---
id: computing-software.networking-hardware-and-wireless.frrouting.ospf6-process-and-interfaces
name: ospf6-process-and-interfaces
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, ospf6d, ospfv3, ipv6, authentication-trailer, redistribute, graceful-restart]
level: practitioner
status: docs-checked
description: "Configure FRR ospf6d for OSPFv3: process and interface area assignment, timers, network type, authentication trailer, redistribution, graceful restart and show commands."
sources:
  - https://docs.frrouting.org/en/latest/ospf6d.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPFv3 (ospf6d)
Process: `router ospf6 [vrf NAME]`, `ospf6 router-id A.B.C.D`, `auto-cost reference-bandwidth COST` (default 100 Mbit/s), `timers throttle spf DELAY INIT-HOLD MAX-HOLD` (0-600000 ms).

Interface:
- `ipv6 ospf6 area AREA` enables OSPFv3 and sets the area.
- `ipv6 ospf6 cost`, `hello-interval` (default 10), `dead-interval` (default 40), `retransmit-interval` (default 5), `priority` (default 1), `transmit-delay` (default 1).
- `ipv6 ospf6 network broadcast|point-to-point|point-to-multipoint`; `passive`; `mtu-ignore`; `ifmtu (1-65535)`.
- `ipv6 ospf6 neighbor X:X::X:X` (link-local), with `poll-interval` or `cost (1-65535)`.
- `ipv6 ospf6 p2p-p2mp disable-multicast-hello|config-neighbors-only|connected-prefixes include|exclude`.

Authentication trailer (RFC 7166):
- `ipv6 ospf6 authentication key-id (1-65535) hash-algo md5|hmac-sha-256 key WORD` (more algorithms with OpenSSL), or `authentication keychain NAME`. Manual key and keychain are mutually exclusive.
- `clear ipv6 ospf6 auth-counters interface [IFNAME]`.

Redistribute and graceful restart:
- `redistribute PROTO [metric-type (1-2)] [metric N] [route-map WORD]`; `default-information originate [always]`.
- `graceful-restart [grace-period (1-1800)]` default 120 s; helper disabled by default; `graceful-restart prepare ipv6 ospf` (EXEC).

Show: `show ipv6 ospf6 [interface|neighbor|database|route|spf tree|redistribute]`.

## Checked

2026-11-08. Read the FRR OSPFv3 page: process commands and SPF throttle range, reference bandwidth default, interface timers and their defaults, network types, p2p-p2mp options, neighbor poll-interval and cost, authentication trailer commands and algorithms, redistribute, default-information originate, graceful restart defaults and show commands. Nothing changed.
Method: docs-only read of cited pages, 2026-11-08
