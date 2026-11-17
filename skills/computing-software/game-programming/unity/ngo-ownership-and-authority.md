---
id: computing-software.game-programming.unity.ngo-ownership-and-authority
name: ngo-ownership-and-authority
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-netcode, netcode-for-gameobjects, ngo-ownership, authority, client-network-transform, distributed-authority, game-programming]
level: advanced
status: draft
description: "Manage ownership in Netcode for GameObjects: server vs owner authority, ChangeOwnership, owner-authoritative NetworkTransform, IsOwner checks and distributed authority."
sources: ["https://docs-multiplayer.unity3d.com/netcode/current/basics/networkobject/#ownership", "https://docs-multiplayer.unity3d.com/netcode/current/terms-concepts/authority/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NGO ownership and authority

**Goal:** know who is allowed to change what, so movement feels responsive and cheating stays contained.

## Concepts
- **Ownership**: every spawned NetworkObject has `OwnerClientId` (server by default). `IsOwner` is true on
  that client. Ownership gates owner-write NetworkVariables and default RPC permissions.
- **Authority**: who simulates the object. Client-server topology: the server has authority unless a
  component (owner-authoritative NetworkTransform) delegates. Distributed authority topology (NGO 2.x
  with Multiplayer Services): the owner is the authority and there is no host simulation.

## Changing ownership (server)
```csharp
no.ChangeOwnership(clientId);   // e.g. player picks up a ball
no.RemoveOwnership();           // back to server
public override void OnGainedOwnership() => EnableLocalControl(true);
public override void OnLostOwnership()  => EnableLocalControl(false);
```
`OnOwnershipChanged(previous, current)` fires on all peers.

## Movement authority choice
| Mode | Feel | Cheating |
|---|---|---|
| Server-authoritative NetworkTransform + client sends input RPCs | input lag = RTT unless you predict | safest |
| **Owner-authoritative** (NetworkTransform with Authority Mode = Owner, or subclass overriding `OnIsServerAuthoritative() => false`) | instant for owner | client can teleport; validate on server |
| Client prediction + reconciliation (custom) | instant + safe | most work; NGO doesn't do it for you |

Co-op and casual games commonly use owner authority with server-side sanity checks (max speed, no
clipping into walls); competitive games need server authority with prediction.

## Patterns
```csharp
public override void OnNetworkSpawn() {
    if (!IsOwner) { GetComponent<PlayerInput>().enabled = false; cam.gameObject.SetActive(false); }
}
void Update() { if (!IsOwner) return; ReadInputAndMove(); }
```
- Only the owner reads local input; others just render replicated state.
- Rigidbody on non-authority instances should be kinematic (NetworkRigidbody handles this).
- Ownership changes are not instant on the client; buffer input until `OnGainedOwnership`.
- `NetworkObject.DontDestroyWithOwner` decides whether objects survive their owner's disconnect.

## Verify
- [ ] Each client controls only its own player; ownership hand-off of a held item has no snap.
- [ ] Server rejects impossible movement from an owner-authoritative client.
