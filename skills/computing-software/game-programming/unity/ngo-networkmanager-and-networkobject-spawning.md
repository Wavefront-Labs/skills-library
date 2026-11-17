---
id: computing-software.game-programming.unity.ngo-networkmanager-and-networkobject-spawning
name: ngo-networkmanager-and-networkobject-spawning
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-netcode, netcode-for-gameobjects, networkobject, networkmanager, network-prefabs, spawning, game-programming]
level: practitioner
status: draft
description: "Set up Netcode for GameObjects: NetworkManager, transport, network prefab lists, server-side spawning and despawning, scene objects and player prefabs."
sources: ["https://docs-multiplayer.unity3d.com/netcode/current/basics/networkobject/", "https://docs-multiplayer.unity3d.com/netcode/current/basics/object-spawning/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NGO NetworkManager and NetworkObject spawning

**Goal:** objects exist on every client exactly when the server says so.

## NetworkManager
- One per game (DontDestroyOnLoad automatically). Assign **Transport** (UnityTransport), **Player Prefab**
  (optional, auto-spawned per client) and a **Network Prefabs List** asset.
- Start: `NetworkManager.Singleton.StartHost()` / `StartServer()` / `StartClient()`; stop with `Shutdown()`.
- Callbacks: `OnClientConnectedCallback`, `OnClientDisconnectCallback`, `OnServerStarted`,
  `ConnectionApprovalCallback` (enable Connection Approval to validate join payloads, pick spawn positions).

## NetworkObject
- Every networked GameObject has one `NetworkObject` at its root; `NetworkBehaviour`s on it or its children.
- Prefabs must be registered in the Network Prefabs List on **all** builds (same list = same hash);
  mismatch = "failed to spawn, prefab hash not found".
- In-scene placed NetworkObjects are spawned automatically when the scene loads via NGO scene management.

## Spawning (server only)
```csharp
public class Spawner : NetworkBehaviour {
    [SerializeField] NetworkObject enemyPrefab;
    public void SpawnEnemy(Vector3 pos) {
        if (!IsServer) return;
        var no = Instantiate(enemyPrefab, pos, Quaternion.identity);
        no.Spawn(destroyWithScene: true);                  // replicate to clients
        // no.SpawnWithOwnership(clientId);  no.SpawnAsPlayerObject(clientId);
    }
    public void Kill(NetworkObject no) => no.Despawn();   // destroys on all; Despawn(false) keeps server copy for pooling
}
```
- Clients never call `Spawn`; they request via an RPC.
- `OnNetworkSpawn()` is the network-aware Awake/Start: `IsServer`, `IsOwner`, NetworkVariables are valid
  there, not in Awake. Mirror with `OnNetworkDespawn()`.
- Pooling: implement `INetworkPrefabInstanceHandler` and register with `NetworkManager.PrefabHandler`.
- Visibility: `CheckObjectVisibility` / `NetworkShow` / `NetworkHide` for interest management.

## Scenes
Use `NetworkManager.SceneManager.LoadScene("Level", LoadSceneMode.Single)` on the server; clients follow
and in-scene objects sync. Don't use `SceneManager.LoadScene` directly while connected.

## Gotchas
- Destroying a spawned object with `Destroy` on a client errors; only the server despawns.
- Nested NetworkObjects in prefabs are not supported; use parenting at runtime (`TrySetParent`).
- Player prefab spawn happens before your scene logic; move to spawn points in OnNetworkSpawn on the server.

## Verify
- [ ] Late-joining client sees all existing objects in their current state.
- [ ] Host + 2 clients (Multiplayer Play Mode) spawn and despawn without errors.
