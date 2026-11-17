---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-graceful-restart-and-shutdown
name: bgp-graceful-restart-and-shutdown
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, graceful-restart, graceful-shutdown, llgr, rfc8203, admin-shutdown]
level: advanced
status: docs-checked
description: "Configure FRR BGP graceful restart and timers, long-lived graceful restart, RFC 8326 graceful shutdown and administrative shutdown."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP graceful restart and shutdown
Graceful restart timers: `bgp graceful-restart restart-time (0-4095)` (default 120), `select-defer-time (0-3600)`, `rib-stale-time (1-3600)`, `stalepath-time (1-4095)`.
- `bgp graceful-restart notification` signals GR support for NOTIFICATION messages (N-bit); reset peers after changing it, otherwise GR is not activated on CEASE or hold-timer-expire notifications.
- Per-peer: `neighbor A.B.C.D graceful-restart`, `graceful-restart-helper`, `graceful-restart-disable`.
- `show bgp [<ipv4|ipv6>] [<view|vrf> VRF] neighbors [peer] graceful-restart [json]`; `show bgp router`.
- Long-lived GR: `bgp long-lived-graceful-restart stale-time (1-16777215)`; off by default (0); only restarter mode is supported. Communities `llgr-stale` (65535:6) and `no-llgr` (65535:7).

Shutdown:
- `neighbor PEER shutdown [message MSG...] [rtt (1-65535) [count (1-255)]]` drops the peer and keeps its configuration.
- `bgp shutdown [message MSG...]` shuts all peers in the instance, sending Cease/Administrative Shutdown (RFC 8203).
- `bgp shutdown no-notify` does the same without notifications; intended for active/standby HA so graceful restart state is preserved on peers.
- `bgp graceful-shutdown` (RFC 8326) per instance or global (mutually exclusive); `no` stops it; if saved to startup configuration it stays in effect across bgpd restarts until disabled. It re-announces routes to eBGP peers with the GRACEFUL_SHUTDOWN community (65535:0). `neighbor PEER graceful-shutdown` per peer sets the community and local-preference 0.

## Checked
2026-11-09. Partial read of docs.frrouting.org bgp.html (one large page): the graceful restart commands and timers, show neighbors graceful-restart, show bgp router, Long-lived Graceful Restart, bgp shutdown and no-notify, bgp graceful-shutdown, neighbor shutdown and graceful-shutdown, and the well-known community list. Removed: the enabled-by-default claim for GR notification (not stated).
Method: documentation only; no commands were run.
