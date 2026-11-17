---
id: computing-software.game-programming.multiplayer-networking.choosing-a-game-transport-library
name: choosing-a-game-transport-library
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, gamenetworkingsockets, enet, transport-library, game-programming]
level: practitioner
status: draft
description: "Pick a game transport: GameNetworkingSockets, ENet, yojimbo, KCP, QUIC or WebRTC compared on reliability, encryption, NAT traversal and platforms."
sources: ["https://github.com/ValveSoftware/GameNetworkingSockets", "http://enet.bespin.org/", "https://github.com/mas-bandwidth/yojimbo"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a transport library

**Goal:** don't write reliability, fragmentation, encryption and NAT traversal yourself unless you must.

## Candidates
| Library | What you get | Notes |
|---|---|---|
| **GameNetworkingSockets** (Valve, BSD-3) | Messages (reliable/unreliable), fragmentation, encryption (AES-GCM), congestion control, P2P via ICE, Steam Datagram Relay when used through Steamworks | Same API as `ISteamNetworkingSockets` in Steamworks |
| **ENet** (MIT) | Reliable/unreliable channels over UDP, sequencing, fragmentation | No encryption; small and battle-tested |
| **yojimbo / netcode** (Glenn Fiedler, BSD) | Connect tokens, encryption via libsodium, reliable-ordered messages | Designed for dedicated servers + matchmaker |
| **KCP** | ARQ protocol trading bandwidth for latency | Common in Asian mobile games, bring your own encryption |
| **QUIC** (msquic, quiche) | Encrypted streams + datagrams (RFC 9221), connection migration | Heavier; good for web-adjacent stacks |
| **WebRTC data channels** | Browser support, unreliable/unordered SCTP channels, ICE/STUN/TURN | Only option for browser UDP-like traffic (plus WebTransport) |
| **Engine stacks** | Unity Transport, Unreal NetDriver, Godot ENet/WebRTC | Use if staying in-engine |

## Decision questions
- Browser clients? WebRTC or WebTransport.
- Peer-to-peer? GNS with ICE, or a platform relay (Steam SDR, EOS P2P).
- Dedicated servers with matchmaker tokens? netcode/yojimbo or GNS.
- Need encryption? Almost always; ENet needs DTLS or your own layer.
- Console platforms: check the library's platform ports and certification needs (encryption is often mandatory).

## Example (GNS)
```cpp
SteamNetworkingIPAddr addr; addr.ParseString("203.0.113.5:27015");
HSteamNetConnection c = SteamNetworkingSockets()->ConnectByIPAddress(addr, 0, nullptr);
SteamNetworkingSockets()->SendMessageToConnection(c, data, len, k_nSteamNetworkingSend_Unreliable, nullptr);
```

## Verify
- Run your target loss/latency profile through a link emulator with each shortlisted library.
