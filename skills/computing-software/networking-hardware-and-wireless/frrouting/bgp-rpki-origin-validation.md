---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-rpki-origin-validation
name: bgp-rpki-origin-validation
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, rpki, origin-validation, rtr, aspa, route-map-match-rpki]
level: advanced
status: docs-checked
description: "Configure RPKI prefix origin validation in FRR bgpd with cache servers, timers, strict mode and route-map match rpki, plus ASPA path verification and show commands."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP RPKI origin validation
Requires the `frr-rpki-rtrlib` package and `-M rpki` in `bgpd_options`.
- `rpki` enters RPKI config mode (global or per-VRF).
- `rpki polling_period (1-3600)` default 300 s; `rpki expire_interval (600-172800)` default 7200; `rpki retry_interval (1-7200)` default 600.
- `rpki cache tcp HOST PORT [source A.B.C.D] preference (1-255)`. Each RPKI/RTR context maps to a VRF with its own cache-server list; `rpki` alone does not activate validation, at least one reachable cache server is needed.
- `rpki cache ssh HOST PORT SSH_USERNAME SSH_PRIVKEY_PATH [KNOWN_HOSTS_PATH] [source A.B.C.D] preference (1-255)`.
- `neighbor PEER rpki strict` blocks session establishment until the cache is connected (default disabled).
- Route-map: `match rpki notfound|invalid|valid`; `match rpki-extcommunity notfound|invalid|valid` (non-transitive OVS extended community, iBGP only).
- Show: `show rpki configuration`, `show rpki prefix <prefix> [ASN]`, `show rpki as-number ASN`, `show rpki prefix-table`, `show rpki cache-server`, `show rpki cache-connection` (all accept `[vrf NAME] [json]`); `show bgp [vrf NAME] [afi] [safi] rpki <valid|invalid|notfound>`.
- `debug rpki` toggles debugging.

ASPA: needs a librtr build with ASPA support, otherwise `match aspa` parses but never matches. `match aspa <upstream|downstream> <valid|invalid|unknown>`; direction is set only by the route-map, not by `local-role`. `show rpki aspa [ASNUM]`, `show bgp [afi] [safi] aspa <upstream|downstream> <state>`. Revalidation after ASPA updates needs `soft-reconfiguration inbound`.

## Checked

2026-11-09. Read the FRR BGP page sections "Enabling RPKI", "Configuring RPKI/RTR Cache Servers", "Configuring RPKI neighbors", "Validating BGP Updates", the RPKI show commands and "ASPA AS_PATH Verification" via a local text copy; every command, range and default above matches. Removed: the claim that a lower cache-server preference is preferred (the page does not say which way).
Method: documentation only; no commands were run.
