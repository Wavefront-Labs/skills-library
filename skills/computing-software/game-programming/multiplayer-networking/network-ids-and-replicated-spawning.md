---
id: computing-software.game-programming.multiplayer-networking.network-ids-and-replicated-spawning
name: network-ids-and-replicated-spawning
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, state-synchronization, network-id, replicated-spawning, entity-ids, despawn, game-programming]
level: practitioner
status: draft
description: "Assign network ids and replicate spawning: server-allocated ids, spawn/despawn messages with prefab type, id reuse safety, scene-placed objects and late-join state."
sources: ["https://gafferongames.com/post/state_synchronization/", "https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking", "https://docs-multiplayer.unity3d.com/netcode/current/basics/object-spawning/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network ids and replicated spawning

**Goal:** every peer agrees which local object a network message refers to, through spawn,
despawn, packet loss and late joins.

## Ids
- The **server allocates** ids (a uint16/uint32 counter or slot+generation). Clients never invent
  ids for authoritative objects.
- Use **slot index + generation** (e.g. 12 bits slot, 4 bits generation) so a stale message for a
  despawned entity doesn't hit the new entity that reused the slot. Or delay reusing an id until all
  clients have acked the despawn.
- Map `netId -> local object` in a dictionary on each peer; never send pointers or engine instance ids.

## Spawn message
```
Spawn { netId, prefabTypeId (hash or index into a shared registry), ownerClientId,
        initial state (position, rotation, key fields) }
Despawn { netId }
```
- The prefab registry must be identical on all builds (stable hashes of asset paths, not list order).
- Send spawn **reliably** (or embed in snapshots: an entity appearing in a snapshot with an unknown id
  plus its type is a spawn; disappearing for N acked snapshots is a despawn). Snapshot-embedded
  spawning removes ordering problems between a reliable spawn and unreliable state.
- Include enough initial state that the object is correct on its first frame (no pop from origin).

## Ordering hazards
- State for an id that hasn't spawned yet: buffer briefly or drop; never create a default object.
- RPC referencing an object despawned on the client: ignore gracefully (log at debug level).
- Despawn racing with in-flight effects: keep a short "dying" period for visuals.

## Scene-placed objects
Objects authored in the level exist on every peer at load; give them deterministic ids (scene GUID
hash) so the server can refer to them without spawning, and send destroyed/changed ones to late joiners.

## Late join
On connect, the server sends the full spawn list + current state (or the first full snapshot), then
deltas. Owned objects (player character) include ownership so the client starts predicting.

## Engines
Unity NGO: `NetworkObject.Spawn()`, `NetworkObjectId`, prefab list with GlobalObjectIdHash. Unreal:
actor channels with `NetGUID`s, `bNetLoadOnClient` for level actors. Godot: `MultiplayerSpawner`
with spawnable scenes list.

## Verify
- [ ] Spawn/despawn spam under 10% packet loss leaves client and server entity sets identical.
- [ ] Late joiner sees destroyed scene objects as destroyed.
