---
id: computing-software.game-programming.multiplayer-networking.server-browsers-and-discovery
name: server-browsers-and-discovery
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, server-list, server-browser, lan-discovery, game-programming]
level: practitioner
status: draft
description: "Build server browsers: master server registration and heartbeats, query protocols (A2S), filters, LAN broadcast discovery and ping measurement."
sources: ["https://developer.valvesoftware.com/wiki/Server_queries", "https://partner.steamgames.com/doc/api/ISteamMatchmakingServers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Server browsers and discovery

**Goal:** let players find community or dedicated servers with accurate player counts and ping.

## Architecture
1. **Registration:** game servers register with a master server (or platform service) on start,
   then heartbeat every 30-60 s with metadata (map, mode, players, max, version, tags). Master drops
   entries after missed heartbeats.
2. **Listing:** clients fetch the list from the master with filters applied server-side (region,
   version, not full, mode).
3. **Querying:** clients query each server directly for live info and to measure ping (UDP
   request/response), because master data is stale and the client's ping is what matters.

## Valve A2S
Source/Steam servers answer UDP queries: `A2S_INFO` (name, map, players), `A2S_PLAYER`,
`A2S_RULES`, with a challenge number to prevent amplification abuse. Steam's
`ISteamMatchmakingServers::RequestInternetServerList` with filter keys (`gamedir`, `map`,
`notfull`, `gametagsand`) does the master + query part for Steam titles.

## LAN discovery
Broadcast (IPv4 255.255.255.255 or subnet broadcast) or multicast a discovery packet on a fixed port;
servers reply unicast with info. IPv6 needs multicast (ff02::1 link-local).

## Practical details
- Throttle queries (e.g. 50 concurrent, refresh in waves) to avoid looking like a DDoS and
  triggering router limits.
- Version filter by protocol version, not build string.
- Favourites and history stored client-side by address.
- Anti-spoofing: challenge-response so fake servers can't list bogus player counts cheaply;
  rank verified servers higher.

## Verify
- Kill a server: disappears from the list within the heartbeat timeout.
- 2,000 listed servers: browser populates progressively without freezing UI.
