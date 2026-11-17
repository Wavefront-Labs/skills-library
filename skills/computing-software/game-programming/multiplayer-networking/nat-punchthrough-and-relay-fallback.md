---
id: computing-software.game-programming.multiplayer-networking.nat-punchthrough-and-relay-fallback
name: nat-punchthrough-and-relay-fallback
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, nat-punchthrough, nat-traversal, stun, turn, ice, relay-server, peer-to-peer, game-programming, relay-servers]
level: advanced
status: draft
description: "Connect peers behind NATs: STUN address discovery, UDP hole punching via a rendezvous server, NAT types that defeat it, and relay fallback (TURN, Steam Datagram Relay, Unity/EOS)."
sources: ["https://datatracker.ietf.org/doc/html/rfc8445", "https://bford.info/pub/net/p2pnat/", "https://partner.steamgames.com/doc/features/multiplayer/steamdatagramrelay"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT punch-through and relay fallback

**Goal:** players on home or mobile networks can host or join peer-to-peer/listen-server games
without port forwarding, and the ones who cannot punch still connect via a relay.

## How UDP hole punching works
1. Both peers send a packet to a **rendezvous / STUN** server; it sees each peer's public
   `ip:port` (server-reflexive address) and tells each about the other (plus their LAN addresses).
2. Both peers simultaneously send packets to each other's public and LAN candidates. Each outgoing
   packet creates a mapping in its own NAT that admits the other's incoming packets.
3. The first candidate pair that receives a reply wins; keep the mapping alive with keep-alives
   every ~15-20 s (NAT UDP timeouts can be as short as 30 s).
ICE (RFC 8445) formalises candidate gathering (host, server-reflexive, relayed), pair checks and
nomination; libraries: libjuice/libnice, WebRTC data channels.

## When it fails
- **Symmetric NAT / endpoint-dependent mapping** (common on carrier-grade NAT and corporate networks):
  the external port differs per destination, so the address learned via STUN is wrong for the peer.
  Port prediction sometimes helps; usually fall back to a relay.
- Firewalls blocking unsolicited UDP; hairpinning unsupported (two players behind the same NAT:
  try LAN candidates first).
- Expect roughly 10-20% of pairs to need a relay; measure in telemetry.

## Relay fallback
- **TURN** servers (coturn) relay UDP between peers; costs bandwidth, adds a hop.
- Platform relays: **Steam Datagram Relay** via `ISteamNetworkingSockets` (also hides IPs, which
  prevents DDoS of hosts), **Epic Online Services** P2P (automatic NAT + relay), **Unity Relay**
  (see unity `unity-transport-and-relay`).
- Pick relay regions near players; for competitive games prefer dedicated servers (no host advantage,
  no host IP exposure).

## Privacy and security
Direct P2P reveals peers' IPs to each other (DDoS/harassment risk on streamers). Relays or
platform networking avoid it; consider relay-only for matchmaking with strangers.

## Verify
- [ ] Test matrix: full-cone home router, symmetric NAT (mobile hotspot), same-LAN pair, IPv6-only.
- [ ] Telemetry records direct vs relayed connection share and connection time.
- [ ] Connections survive 2 minutes idle (keep-alives hold NAT mappings).
