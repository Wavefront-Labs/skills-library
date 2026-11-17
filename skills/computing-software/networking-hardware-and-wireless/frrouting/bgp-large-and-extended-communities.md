---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-large-and-extended-communities
name: bgp-large-and-extended-communities
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, large-community, extcommunity, route-target, soo, extcommunity-list]
level: advanced
status: docs-checked
description: "Use BGP large communities and extended communities in FRR: list definitions, route-map match and set for rt, soo, nt, color and bandwidth, and show commands."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP large and extended communities
Large (format `GLOBAL:LOCAL1:LOCAL2`, RFC 8092):
- `bgp large-community-list standard NAME permit|deny LARGE-COMMUNITY`; `expanded NAME permit|deny LINE` matches the whole string.
- `match large-community LINE [exact-match]`; `set large-community LARGE-COMMUNITY [LARGE-COMMUNITY] [additive]`; `set large-comm-list delete NAME`.
- `show bgp large-community-list [NAME detail]`, `show ip bgp large-community-info`, `show [ip] bgp <ipv4|ipv6> large-community [LC [exact-match]]`.

Extended (`AS:VAL` or `IP-Address:VAL`):
- `bgp extcommunity-list standard NAME permit|deny EXTCOMMUNITY` using `rt`, `soo`, `nt` or `color` prefixes; `expanded` takes a regex without rt/soo prefix. Numbered: `(1-99)` standard, `(100-500)` expanded.
- `match extcommunity WORD [exact-match|any]`, `match extcommunity-limit (0-65535)`.
- `set extcommunity none|rt|nt|soo|color|bandwidth ...`; `set extcommunity evpn rmac X:X:X:X:X:X` on type-5 routes; `set extended-comm-list delete NAME`.
- `nt` is installed by the receiver only if it supports NT and the value matches its BGP identifier.
- `color` uses `CO:COLOR` form (RFC 9256); CO is 00, 01 or 10; 11 is reserved.
- `neighbor <peer> soo EXTCOMMUNITY` sets a per-neighbor Site of Origin.
- `neighbor PEER send-community extended rpki` sends RPKI extended communities to iBGP and eBGP-OAD peers only.

Show: `show bgp extcommunity-list [NAME detail]`.

## Checked

2026-11-09. Read the FRR BGP page sections "Extended Community Lists", "BGP Extended Communities in Route Map", "Large Community Lists", "Large Communities in Route Map", `neighbor soo`, `send-community extended rpki` and the large-community show commands via a local text copy; every command, range and rule above matches. Note from the page: expanded large-community lists are used for match only, not for set.
Method: documentation only; no commands were run.
