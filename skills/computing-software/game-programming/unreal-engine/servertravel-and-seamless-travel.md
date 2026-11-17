---
id: computing-software.game-programming.unreal-engine.servertravel-and-seamless-travel
name: servertravel-and-seamless-travel
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gameplay-framework, seamless-travel, servertravel, transition-map, game-programming]
level: practitioner
status: docs-checked
description: "Move multiplayer sessions between maps in Unreal: Browse vs ServerTravel vs ClientTravel, seamless travel, the transition map, and which actors persist across travel."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/travelling-in-multiplayer-in-unreal-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ServerTravel and seamless travel

**Goal:** change maps mid-session without disconnecting players, keeping the actors that matter.

## Seamless vs non-seamless
Seamless travel is a non-blocking operation; non-seamless is a blocking call. In a non-seamless travel the
client disconnects from the server and reconnects to the same server, which has the new map ready.
Epic recommends seamless travel where possible: a smoother experience, and it avoids problems that can
occur during reconnection.

A non-seamless travel must be used:
- when loading a map for the first time,
- when connecting to a server for the first time as a client,
- when ending a multiplayer game and starting a new one.

## The three travel functions
| Function | Behaviour |
|---|---|
| `UEngine::Browse` | A hard reset when loading a new map. Always non-seamless; the server disconnects current clients first, and clients disconnect from their server. A dedicated server cannot travel to other servers, so the map must be local, not a URL. |
| `UWorld::ServerTravel` | Server only. Jumps the server to a new world/level and all connected clients follow. This is how multiplayer games travel from map to map; the server calls it, and it calls `APlayerController::ClientTravel` for every connected client. |
| `APlayerController::ClientTravel` | Called on a client: travels to a new server. Called on the server: tells that particular client to travel to the new map while staying connected to the current server. |

## Enabling seamless travel
1. Set up a transition map through `UGameMapsSettings::TransitionMap`. It is empty by default; if you leave
   it empty, an empty map is created for you.
2. Set `AGameModeBase::bUseSeamlessTravel` to true.

Why a transition map: a world must always be loaded, so the old map cannot be freed before the new one
loads; holding both big maps in memory is a bad idea, so travel goes current map, then the small transition
map, then the final map.

Flow: mark actors that persist to the transition level, travel to it, mark actors that persist to the
final level, travel to the final level.

## What persists automatically
- The GameMode actor (server only).
- Actors added through `AGameModeBase::GetSeamlessTravelActorList`.
- All Controllers that have a valid PlayerState (server only).
- All PlayerControllers (server only).
- All local PlayerControllers (server and client).
- Actors added through `APlayerController::GetSeamlessTravelActorList`, called on local PlayerControllers.

Add other actors you need (inventory items, for example) through the `GetSeamlessTravelActorList`
functions.

## Verify
- [ ] Clients stay connected across several `ServerTravel` map changes with seamless travel on.
- [ ] A transition map is configured rather than relying on the generated empty one, if you want control of it.

## Checked
Checked 2026-11-08 against the Travelling in Multiplayer page.
Confirmed: seamless vs non-seamless behaviour, the three functions, transition map setup, flow, default
persistence list.
Removed because the page does not state them: `?listen` handling, `net.AllowPIESeamlessTravel`,
`PlayerState::CopyProperties` details, GameMode and PlayerController hook lists, packaging notes, and the
API reference source (unreadable stub).
Method: docs-only read of cited pages, 2026-11-08
