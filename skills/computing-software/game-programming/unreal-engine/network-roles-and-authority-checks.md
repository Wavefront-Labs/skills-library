---
id: computing-software.game-programming.unreal-engine.network-roles-and-authority-checks
name: network-roles-and-authority-checks
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-replication, net-role, has-authority, local-role, remote-role, autonomous-proxy, simulated-proxy, islocallycontrolled, netmode, game-programming]
level: practitioner
status: draft
description: "Gate Unreal gameplay code by network role: HasAuthority, Local/RemoteRole, autonomous vs simulated proxies, NetMode and IsLocallyControlled, with the usual mistakes."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-role-and-remote-role-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network roles and authority checks

**Goal:** every function runs only where it should (server, owning client, everyone), in listen
server, dedicated server and standalone.

## Roles per actor instance
`GetLocalRole()` on the machine you are on:
| Role | Meaning |
|---|---|
| `ROLE_Authority` | This machine owns the truth (server, or standalone, or a client-only spawned actor). |
| `ROLE_AutonomousProxy` | Client copy controlled by this client (its possessed Pawn, its PlayerController). |
| `ROLE_SimulatedProxy` | Client copy of someone else's actor; follows replicated state. |
| `ROLE_None` | Not replicated. |
`GetRemoteRole()` is the role on the other side.

## The common checks
```cpp
if (HasAuthority())                  { /* server-side: apply damage, spawn, award score */ }
if (IsLocallyControlled())           { /* Pawn: owning client or listen-server host's own pawn: camera, HUD, input */ }
if (GetLocalRole() == ROLE_SimulatedProxy) { /* cosmetic interpolation for other players */ }
if (GetNetMode() == NM_DedicatedServer) { /* skip audio, VFX, UI */ }
```
`GetNetMode()`: `NM_Standalone`, `NM_DedicatedServer`, `NM_ListenServer`, `NM_Client`.
`IsNetMode(NM_Client)` is a shortcut. For "should I play cosmetics" use
`!IsRunningDedicatedServer()` or `GetNetMode() != NM_DedicatedServer`.

## Patterns
- **Server-only gameplay, client-predicted feel:** client calls a `Server` RPC, plays local cosmetic
  feedback if `IsLocallyControlled()`, server validates and changes replicated state; RepNotify plays
  effects on simulated proxies.
- **Listen server host** is both `HasAuthority()` and `IsLocallyControlled()`; code that assumes
  "authority means not a player" breaks here. RepNotify does not fire on the server automatically in
  C++; call the OnRep function manually after setting the value on the server.
- **Spawning:** spawn replicated actors only on authority; a client spawn creates a local-only actor
  with `ROLE_Authority` locally (often a bug).
- **BeginPlay** runs on every machine; guard initialisation that must happen once.
- Blueprint: Switch Has Authority node, Is Locally Controlled, Is Server.

## Ownership vs role
RPC routing depends on the **owning connection** (`SetOwner`, possessed pawns are owned by their
PlayerController), not on role. A Server RPC on an actor the client does not own is dropped with a
log warning "No owning connection".

## Testing matrix
PIE Net Mode: Play As Listen Server with 2 players, then Play As Client (dedicated server in
background). Use `Net PktLag=100` in the console. Log role with
`UE_LOG(LogTemp, Log, TEXT("%s role %s"), *GetName(), *UEnum::GetValueAsString(GetLocalRole()))`.

## Verify
- [ ] Feature works in Standalone, Listen Server (host and client) and Dedicated Server modes.
- [ ] No "No owning connection" warnings in the log.
- [ ] Dedicated server log shows no cosmetic spawns (audio/VFX/widgets).
