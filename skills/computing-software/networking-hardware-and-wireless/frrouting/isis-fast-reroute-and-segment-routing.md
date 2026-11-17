---
id: computing-software.networking-hardware-and-wireless.frrouting.isis-fast-reroute-and-segment-routing
name: isis-fast-reroute-and-segment-routing
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, isisd, isis, lfa, ti-lfa, segment-routing, srv6, flex-algo, mpls-te]
level: sme
status: docs-checked
description: "Enable IS-IS fast reroute (LFA, remote LFA, TI-LFA), segment routing with SRGB and prefix SIDs, SRv6 locators, Flex-Algo definitions and MPLS-TE in FRR isisd."
sources:
  - https://docs.frrouting.org/en/latest/isisd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IS-IS fast reroute and segment routing
Fast reroute (global, optional `level-1|level-2`):
- `spf prefix-priority critical|high|medium WORD`; `fast-reroute priority-limit critical|high|medium`.
- `fast-reroute lfa tiebreaker downstream|lowest-backup-metric|node-protecting index (1-255)` (lower index first); `fast-reroute load-sharing disable`; `fast-reroute remote-lfa prefix-list WORD`.
- Interface: `isis fast-reroute lfa [exclude interface IFNAME]`, `isis fast-reroute remote-lfa tunnel mpls-ldp`, `isis fast-reroute remote-lfa maximum-metric (1-16777215)`, `isis fast-reroute ti-lfa [node-protection [link-fallback]]`.
- `show isis fast-reroute summary`, `show isis route backup`.

Segment routing (experimental, MPLS, RFC 8667):
- `segment-routing on`; `segment-routing global-block LOW HIGH [local-block LOW HIGH]` (16-1048575); `segment-routing node-msd (1-16)`.
- `segment-routing prefix PREFIX [algorithm (128-255)] absolute N|index N [no-php-flag|explicit-null] [n-flag-clear]`.
- `show isis segment-routing node`.

SRv6 (RFC 9352): `segment-routing srv6`, `locator NAME` (must exist in zebra), `interface NAME` (default sr0 dummy). `show isis segment-routing srv6 node`.

Flex-Algo (RFC 9350): `flex-algo (128-255)` with `advertise-definition`, `priority (0-255)`, `metric-type igp|te|delay` (`igp` is the default; `te` and `delay` are advertised but the algorithm is disabled locally), `affinity include-any|include-all|exclude-any NAME`; `affinity-map NAME bit-position (0-255)`; interface `isis affinity flex-algo NAME`. Up to 128 FADs per area.

MPLS-TE: `mpls-te on`, `mpls-te router-address A.B.C.D`, `mpls-te export`.

## Checked

2026-11-08. Read the FRR isisd page: fast-reroute global and interface commands, show commands, segment routing commands and ranges, experimental status, SRv6 locator and sr0 interface, Flex-Algo commands and limits, MPLS-TE commands. Added the page's statement that te and delay metric types are not supported locally.
Method: docs-only read of cited pages, 2026-11-08
