---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-bmp-monitoring
name: bgp-bmp-monitoring
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, bmp, monitoring, telemetry, route-mirroring, loc-rib]
level: advanced
status: docs-checked
description: "Export BGP state to a collector with the BMP module in FRR bgpd: load with -M bmp, define targets, active connect or passive listener, route monitoring, mirroring and statistics."
sources:
  - https://docs.frrouting.org/en/latest/bmp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP Monitoring Protocol (BMP)
Start `bgpd` with `-M bmp`; BMP cannot be enabled otherwise. All options go inside `router bgp ASN`.

Instance-wide: `bmp mirror buffer-limit (0-4294967294)` caps memory for mirrored messages, shared by all targets.

Per `bmp targets NAME`:
- `bmp connect HOSTNAME port (1-65535) {min-retry MSEC|max-retry MSEC} [source-interface WORD]` opens an active session with exponential backoff.
- `bmp listener ADDR port (1-65535)` is passive; `0.0.0.0` or `::` listens on all addresses.
- `ip access-list NAME` / `ipv6 access-list NAME` restricts allowed session addresses (active and passive).
- `bmp monitor AFI SAFI pre-policy|post-policy|loc-rib`; AFI ipv4 or ipv6, SAFI unicast, multicast, evpn or vpn.
- `bmp mirror` mirrors messages for all BGP neighbors.
- `bmp stats [interval (100-86400000)]` in ms; `bmp stats send-experimental` uses codes 65531-65534.
- `bmp import-vrf-view NAME` monitors another BGP instance.
- `bmp initiation sysDescr|sysName LINE...` up to 255 characters; defaults are the FRR version and the hostname.

The page gives no defaults for retry timers or stats interval, and no show commands.

## Checked

2026-11-04. Confirmed against the FRR BMP page: -M bmp requirement, mirror buffer-limit, targets, connect, listener, access lists, monitor, mirror, stats, import-vrf-view and initiation commands with ranges. Nothing changed.
Method: documentation only; no commands were run.
