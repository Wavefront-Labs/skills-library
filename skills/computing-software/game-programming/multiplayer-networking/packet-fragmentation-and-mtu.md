---
id: computing-software.game-programming.multiplayer-networking.packet-fragmentation-and-mtu
name: packet-fragmentation-and-mtu
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, mtu, packet-fragmentation, fragment-reassembly, path-mtu, ip-fragmentation, udp, game-programming]
level: advanced
status: verified
description: "Keep game packets under path MTU and fragment large ones yourself: safe payload sizes, fragment headers, bounded reassembly, and why IP fragmentation fails."
sources: ["https://gafferongames.com/post/packet_fragmentation_and_reassembly/", "https://datatracker.ietf.org/doc/html/rfc8085#section-3.2", "https://datatracker.ietf.org/doc/html/rfc8900"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packet fragmentation and MTU

**Goal:** packets that arrive on every network path, and a safe way to send the occasional large
payload (initial world state, map data).

## Size budget
- Ethernet MTU 1500 minus IPv4 (20) / IPv6 (40) and UDP (8) headers; tunnels, VPNs, PPPoE and mobile
  networks reduce it further. IPv6 guarantees only 1280 bytes.
- Practical game payload cap: **~1200 bytes** per UDP datagram (QUIC uses 1200 for the same reason).
  Relays and encryption headers eat into this: subtract them.
- Rely on your own fragmentation, not the IP layer: IP fragments are dropped by many NATs/firewalls,
  one lost fragment loses the whole datagram, and fragment floods are a DoS vector (RFC 8900).
  Set DF where possible (`IP_DONTFRAGMENT`/`IP_MTU_DISCOVER`) to fail fast during testing.

## Application-level fragmentation
Fragment header (Gaffer):
```
[packet header with type = FRAGMENT] [sequence 2B] [fragment id 1B] [num fragments 1B] [fragment data]
```
Gaffer's version uses a 16-bit sequence, a 2-bit packet type, an 8-bit fragment id in [0,255] and an 8-bit count representing [1,256] (so store `num fragments - 1`), padded to a byte boundary before the data, with 1024-byte fragments and a 1200-byte conservative MTU.
- Split payload into `ceil(size / FRAGMENT_SIZE)` pieces (e.g. 1024 bytes); cap `num fragments` (e.g. 256).
- Receiver: reassembly buffer keyed by sequence (sequence buffer of ~256 entries), bitmask of
  received fragments; deliver when all present; discard entries older than the window or after a
  timeout (1-2 s).
- **Validate:** `fragment id < num fragments`, `num fragments ≤ max`, consistent `num fragments` across
  fragments of one sequence, last fragment size ≤ FRAGMENT_SIZE, and a byte limit for all pending
  reassembly memory per connection.
- Fragmented packets fail if any fragment is lost, so loss rates multiply: 1% loss per packet ->
  9.6% (1 - 0.99^10, computed) for a 10-fragment payload. For large reliable data, use a **chunk/slice system** with
  per-slice acks and resend (Gaffer "Sending Large Blocks of Data") instead of fragments alone.

## Discovering smaller paths
Measure with probes of decreasing size during connection (send 1200, 1000, ... with DF and see what
arrives), or simply stay at a conservative cap. Log the negotiated size in telemetry.

## Verify
- [ ] Packets above the cap are impossible to send (assert in the send path).
- [ ] Reassembly survives random fragment order, duplicates and drops; memory stays bounded under a
  flood of first-fragments.
- [ ] Test over a VPN and a mobile hotspot: no silent drops of large packets.
