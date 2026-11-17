---
id: computing-software.game-programming.multiplayer-networking.anti-cheat-and-server-authority-validation
name: anti-cheat-and-server-authority-validation
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, anti-cheat, server-authority, input-validation, rate-limiting, sanity-checks, speedhack, aimbot-detection, wallhack, interest-management, trust-boundary, kernel-anticheat, game-programming, client-trust, wallhack-mitigation]
level: advanced
status: draft
description: "Design server-side validation so the server never trusts a client's claims about position, damage, or inventory, and know what client anti-cheat can and can't add on top."
sources: ["https://www.gdcvault.com/play/1024972/Server-Side-Game-Hacking"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Anti-cheat and server authority validation

**Goal:** the server-side half of multiplayer security — build it so a
modified client (speedhack, aimbot, memory-edited values) *cannot* affect
other players' games no matter what it sends, because the server independently
validates everything rather than trusting client-reported state. Kernel-level
client anti-cheat (Easy Anti-Cheat, BattlEye, Vanguard) is a separate, heavier
layer that detects cheat tools running on the client; it does not substitute
for server-side validation, which is the part actually in a gameplay
programmer's control and the part that matters even if client anti-cheat is
bypassed.

## The rule: the server derives truth, it never imports it
Every value that matters for fairness must be **computed server-side from
raw inputs**, never accepted as a client-reported result. The client should
send "I pressed Fire" (an input), not "I dealt 50 damage to player X" (a
claimed outcome) — the server runs its own hit-detection and damage
calculation from the input and the server's own copy of world state. This is
the same server-authoritative principle underlying
`computing-software.game-programming.multiplayer-networking.client-prediction-and-server-reconciliation`
and
`computing-software.game-programming.unreal-engine.replication-rpcs-and-network-relevancy`'s
RPC-validation note, but it's worth stating as the single governing rule:
anywhere this is violated is an exploit, not just a bug.

## Concrete sanity checks worth writing
- **Movement speed/teleport checks**: compare a player's reported or
  server-tracked position delta per tick against the maximum physically
  possible given their known movement speed and elapsed time; reject or clamp
  anything exceeding it with margin for latency jitter, not zero tolerance
  (too strict and legitimate lag spikes get falsely flagged).
- **Rate limiting on action RPCs**: a Fire RPC arriving faster than the
  weapon's fire rate allows (even if each individual call looks valid) is a
  speedhack or a replayed/spammed packet — track last-action timestamp
  server-side per action type and reject calls inside the cooldown window,
  server-side, regardless of what the client's local cooldown UI shows.
- **Resource/inventory checks**: any action that spends a resource (ammo,
  currency, an item) must check and decrement that resource **on the server**
  at the moment of spend, not trust a client's "I have ammo" flag — a modified
  client reporting infinite ammo should simply fail the server's own ammo
  check and the shot never registers server-side.
- **Range/line-of-sight validation on hits**: a reported hit must pass a
  server-side distance and (for hitscan) a server-side raycast check against
  the server's own collision data — an aimbot that reports impossible-angle
  or through-wall hits should fail this check regardless of how convincing the
  client-side shot looked.

## Interest management as an anti-cheat tool, not just bandwidth
Wallhacks (seeing enemies through walls) are often not a rendering exploit at
all — they're reading network traffic the client was sent but shouldn't have
been. If the server replicates every other player's exact position to every
client regardless of visibility (common when relevancy/interest management
was implemented only for bandwidth, not security), a memory-reading or
packet-sniffing tool trivially extracts positions the player should never see.
Fix by genuinely **not sending** data the client has no legitimate need for —
only replicate enemy position/state to clients with actual line-of-sight or
proximity, the same relevancy mechanism covered for bandwidth reasons in
`computing-software.game-programming.unreal-engine.replication-rpcs-and-network-relevancy`,
but applied here as the actual fix for an entire cheat category, not an
optimization.

## What server validation cannot catch
Aim-assist-level precision improvements (an aimbot that only nudges aim
slightly, staying within human-plausible speed/accuracy bounds) and purely
visual advantages that don't require extra network data (ESP reading the
client's own already-necessary local game state, not wallhacking via network
traffic) are not caught by server-side validation because nothing about them
violates a server-checkable rule — these require client-side detection
(statistical anomaly detection, kernel anti-cheat, replay/report review by
humans) as a genuinely separate layer, not a gap in validation logic to "fix."

## Verify
- [ ] Every damage/economy-affecting action is computed server-side from raw
      input, never accepted as a client-reported outcome — grep RPCs for any
      that take a damage/result value as a parameter from a client caller.
- [ ] Movement, fire-rate, and resource-spend checks exist server-side and were
      tested by attempting to violate them from a modified/test client, not
      just reasoned about.
- [ ] Interest management actually withholds non-visible entities' state from
      clients, verified by inspecting outgoing replication data for a client
      with no line-of-sight to a given enemy.
- [ ] The team has a documented position on what server validation can't
      catch and what layer (kernel anti-cheat, stats-based detection, human
      review) is relied on for those cases, rather than assuming server
      checks are sufficient alone.
