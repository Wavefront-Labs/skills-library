---
id: computing-software.game-programming.unreal-engine.replication-rpcs-and-network-relevancy
name: replication-rpcs-and-network-relevancy
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, replication, rpc, repnotify, multicast, server-rpc, client-rpc, network-relevancy, net-cull-distance, variable-replication, reliable, unreliable, net-dormancy, replication-graph, game-programming]
level: advanced
status: draft
description: "Replicate Unreal gameplay state correctly: which RPC type to use, RepNotify patterns, relevancy/culling, and the bandwidth mistakes that don't show up until many clients connect."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-and-multiplayer-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-replication-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unreal replication, RPCs, and network relevancy

**Goal:** make gameplay state appear correctly on every client without flooding
the network — know which of the three RPC types to use, how `RepNotify` should
and shouldn't be used, and what breaks only once relevancy and dormancy enter
the picture at scale.

## Variable replication basics
```cpp
UPROPERTY(ReplicatedUsing = OnRep_Health)
float Health;

void AMyCharacter::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const {
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(AMyCharacter, Health);
    DOREPLIFETIME_CONDITION(AMyCharacter, Ammo, COND_OwnerOnly);   // bandwidth: only replicate to owning client
}
```
- Only the **server** can write a replicated property meaningfully — a client
  write is local-only and gets stomped on the next server update. Treat the
  server as the sole source of truth; this is the #1 source of "works for host,
  breaks for clients" bugs.
- `OnRep_Health` fires only on **clients**, only when the value actually changes
  across the wire, and never on the server (the server already knows). Don't put
  gameplay logic that must also run on the server inside a RepNotify — call a
  shared function from both the setter (server) and the RepNotify (client).
- `COND_OwnerOnly`, `COND_SkipOwner`, `COND_InitialOnly` cut bandwidth
  dramatically on anything the owning client already knows or doesn't need
  (ammo count to everyone, local-only predicted state).

## The three RPC types — pick deliberately
| Type | Runs on | Use for |
|---|---|---|
| `Server` | Executed on the server, called from an owning client | Client telling the server "I want to do X" (fire, interact). Validate every input — a client calling this can lie. |
| `Client` | Executed on the owning client, called from the server | Server telling one specific client something (a private message, "you were hit"). |
| `NetMulticast` | Executed on the server AND all clients, called from the server | Cosmetic effects everyone should see (muzzle flash, death ragdoll trigger) — never gameplay-authoritative state, since a late-joining client simply misses past multicasts. |

Add `Reliable` only for events that must arrive (death, a one-time pickup);
default to `Unreliable` for high-frequency cosmetic calls — reliable RPCs queue
and can stall subsequent reliable traffic on packet loss ("reliable RPC backup").
`WithValidation` on Server RPCs lets you reject malformed calls before they run
(`Server_Fire_Validate` returning false silently drops the call and can
soft-disconnect a persistently-cheating client).

## Relevancy, culling, and dormancy
An Actor only replicates to a client if it's **relevant** to them — by default,
roughly "on screen or within NetCullDistanceSquared." Setting
`bAlwaysRelevant` or a huge cull distance on something that doesn't need it
(a global weather manager, fine; every pickup in a large open world, not fine)
multiplies server CPU and bandwidth per connected client. `bNetUseOwnerRelevancy`
and `SetNetDormancy(DORM_DormantAll)` matter at scale: a dormant actor stops
being checked for replication entirely until explicitly flushed
(`FlushNetDormancy`) — used for static-until-interacted-with actors (a chest, a
door) so the server isn't re-evaluating thousands of inert actors every tick.
For hundreds of players, the default per-actor relevancy check doesn't scale —
that's what the **Replication Graph** plugin exists to replace (spatial-grid-
based relevancy), used in Fortnite-scale projects; don't reach for it below
~50 concurrent actors-of-interest without profiling first.

## Verify
- [ ] Every replicated variable with gameplay consequence is written only on the
      server; client-side prediction (if any) reconciles against the server value,
      not the other way around.
- [ ] Gameplay-critical events use `Server`/`Client` RPCs (or replicated
      variables), never rely solely on an unreliable `NetMulticast` a late joiner
      could miss.
- [ ] Tested with "Number of Players" ≥ 2 in PIE and at least one instance running
      as a pure client (not listen-server host) — catches owner-only and
      authority bugs the single-player/host case hides.
- [ ] Bandwidth checked with `stat net` under real gameplay load, not just idle.
