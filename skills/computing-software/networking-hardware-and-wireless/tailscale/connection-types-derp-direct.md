---
id: computing-software.networking-hardware-and-wireless.tailscale.connection-types-derp-direct
name: connection-types-derp-direct
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [derp, direct-connection, peer-relay]
level: practitioner
status: docs-checked
description: "Know the sequence Tailscale uses to upgrade from DERP relayed to direct or peer relay connections."
sources: ["https://tailscale.com/kb/1257"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Connection types

Goal: reason about why two devices are direct or relayed.

All connection types are end-to-end encrypted with WireGuard; the difference is performance, not security.

**Negotiation sequence (device-a to device-b)**

1. device-a starts a connection and connects to the DERP server device-b already uses.
2. The connection request goes through DERP.
3. The devices exchange direct-connection details via their DERP servers.
4. Both try NAT traversal strategies to build a direct UDP tunnel.
5. If it works, packets go peer to peer with no relay.
6. If not, they try a Tailscale Peer Relay, which requires at least one peer relay device that both can reach.
7. If no peer relay is available they stay on the DERP relay.

All connections start relayed through DERP, then Tailscale tries to upgrade them to direct, then peer relay. It periodically re-checks whether a direct or peer relay connection is possible.

**Relayed types**

- DERP relayed: Tailscale-operated DERP servers relay packets.
- Peer relay: a device in your own infrastructure relays.

A direct connection is UDP peer to peer and usually gives the lowest latency and highest throughput.

**Checklist**

1. Check whether a path is direct or relayed.
2. Fix NAT or firewall blocks if relayed.
3. Consider a peer relay for restrictive networks.

## Checked

Confirmed against Tailscale kb/1257 (Connection types), read in full: the three connection types, WireGuard encryption on all of them, the device-a to device-b negotiation sequence, the direct then peer relay then DERP fallback order, periodic re-checking, and the peer relay requirement. Nothing was removed.

Method: docs-checked 2026-11-09 against https://tailscale.com/kb/1257
