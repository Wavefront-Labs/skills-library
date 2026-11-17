---
id: computing-software.game-programming.multiplayer-networking.region-and-ping-based-selection
name: region-and-ping-based-selection
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, region-selection, ping-measurement, matchmaking, game-programming]
level: practitioner
status: draft
description: "Pick the right server region: measure ping to regional beacons, combine latency with queue health, handle VPNs and bad measurements, and expose overrides."
sources: ["https://partner.steamgames.com/doc/features/multiplayer/steamdatagramrelay", "https://learn.microsoft.com/en-us/gaming/playfab/features/multiplayer/servers/using-qos-beacons-to-measure-player-latency-to-azure"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Region and ping-based selection

**Goal:** put players on servers with low latency without starving queues.

## Measure, don't geolocate
IP geolocation is wrong for VPNs, mobile carriers and routing. Measure RTT from the client to each
region:
- **QoS beacons:** lightweight UDP echo endpoints per region (PlayFab QoS servers on port 3075;
  AWS GameLift and others offer similar). Send several pings, take a low percentile (median of the
  best few) to filter spikes.
- **Steam Datagram Relay:** `ISteamNetworkingUtils::GetPingToDataCenter` and ping location strings
  let matchmakers estimate ping between any two players or to any data centre without direct pings.

## Matchmaking ticket
Include a latency map `{ "us-east": 32, "eu-west": 110 }` in the ticket. Matchmaker rule:
- Start with regions under a tight limit (e.g. 60 ms), widen over wait time (rule expansion) to 100,
  150 ms.
- Choose the region minimising the max (or a percentile) ping across the match.

## Edge cases
- Measurement failure (firewalls block UDP): fall back to the last good map or to a coarse IP region.
- Re-measure on network change and periodically (every session start).
- Party matchmaking: use the party's worst ping per region.
- Let players set a manual region preference and ping limit, but cap how far that can stall queues.

## Verify
- Telemetry: distribution of in-match ping vs measured pre-match ping; large gaps mean bad measurement.
- Simulate VPN user in another continent: matched to the region they actually ping best.
