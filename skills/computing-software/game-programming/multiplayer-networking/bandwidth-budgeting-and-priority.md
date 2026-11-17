---
id: computing-software.game-programming.multiplayer-networking.bandwidth-budgeting-and-priority
name: bandwidth-budgeting-and-priority
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, snapshot, bandwidth-budget, priority-accumulator, interest-management, packet-budget, net-priority, game-programming]
level: advanced
status: gated
description: "Stay within a per-client bandwidth budget: setting byte budgets per packet, priority accumulators for entity selection, relevancy weighting and measuring bandwidth per entity type."
sources: ["https://gafferongames.com/post/state_synchronization/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-priority-in-unreal-engine", "https://gafferongames.com/post/packet_fragmentation_and_reassembly/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bandwidth budgeting and priority

**Goal:** every client gets the most important state each packet while total bandwidth stays under a
fixed budget, so the game degrades gracefully instead of lagging when the world is busy.

## Set the budget
- Target per-client downstream (e.g. 256 kbps for action games; mobile lower), upstream much lower.
- Bytes per packet = budget / send rate (256 kbps at 30 Hz = 1,066 bytes per packet, computed). Keep packets under
  the safe MTU (~1200 bytes payload) to avoid IP fragmentation.

## Priority accumulator (Gaffer On Games "State Synchronization")
Each entity has an accumulator per client:
```
every packet:
    for each relevant entity e:
        e.acc += priority(e, client) * dt
    sort entities by acc descending
    write entities in that order until the packet byte budget is reached
    for each entity written: e.acc = 0
```
Entities not sent keep accumulating, so they eventually get sent even with low priority: no
starvation, and the budget is always respected. Simulated in Python (300 entities, priorities 10 / 1 / 0.1 for 10 / 90 / 200 entities, 1,000-byte budget, 40-byte entities, 3,000 packets): the budget was never exceeded, the top group went out in 99.98% of packets, the middle group in 13.6% and the low group in 1.4% (about every 72 packets), no entity was never sent, and the longest gap for a low-priority entity was 99 packets. Gaffer's article describes the same accumulator and a 256 kbit/s example limit.

## Priority function
Combine: base priority by type (players > projectiles > props), distance to the client's view
(closer = higher), in view frustum, recently changed/interacting with the player, gameplay importance
(ball in a sports game, objective carrier). Unreal's equivalent: `NetPriority` plus
`GetNetPriority()` considering view distance and time since last replication (gated: unconfirmed, source is paywalled or blocked); Replication Graph for
large counts.

## Combine with relevancy and rates
- **Relevancy** (interest management) removes entities entirely (too far, hidden, other team).
- Per-type update rates (static props rarely, players every packet).
- Delta compression to make each write cheaper.

## Measure
Track bytes per entity type per second and per client; percentiles over a match; worst-case scenes
(all players in one spot). Unreal: Networking Insights; custom engines: counters around serialize
calls. Set alerts when budgets are exceeded in automated bot matches.

## Verify
- [ ] Packet size never exceeds the configured budget (assert in debug).
- [ ] In a crowded stress test, nearby players still update every packet; distant props update less.
- [ ] No entity goes unsent for longer than a configured maximum interval.
