---
id: computing-software.game-programming.unity.ngo-network-scene-manager
name: ngo-network-scene-manager
category: computing-software
field: game-programming
product: unity
tags: [unity, netcode-for-gameobjects, ngo, network-scene-manager, scene-loading, scene-synchronization, game-programming]
level: practitioner
status: draft
description: "Load scenes in Netcode for GameObjects with NetworkSceneManager: server-driven LoadScene, scene events, late-join synchronization, additive scenes and common errors."
sources: ["https://docs-multiplayer.unity3d.com/netcode/current/basics/scenemanagement/using-networkscenemanager/", "https://docs-multiplayer.unity3d.com/netcode/current/basics/scenemanagement/scene-events/", "https://docs-multiplayer.unity3d.com/netcode/current/basics/scenemanagement/client-synchronization-mode/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NetworkSceneManager scene loading

**Goal:** move every connected client into the same scene and keep late joiners in sync.

## Basics
- Keep **Enable Scene Management** on in the NetworkManager (default). Only the server (or session
  owner in distributed authority) loads scenes; clients follow automatically.
- Every networked scene must be in the build scene list.

```csharp
public void StartMatch() {
    if (!NetworkManager.Singleton.IsServer) return;
    var status = NetworkManager.Singleton.SceneManager.LoadScene("Arena", LoadSceneMode.Single);
    if (status != SceneEventProgressStatus.Started) Debug.LogWarning($"Load failed: {status}");
}

void OnEnable() => NetworkManager.Singleton.SceneManager.OnSceneEvent += OnSceneEvent;
void OnSceneEvent(SceneEvent e) {
    if (e.SceneEventType == SceneEventType.LoadEventCompleted && IsServer)
        SpawnPlayers(e.ClientsThatCompleted);          // everyone finished loading
}
```
Never call `UnityEngine.SceneManagement.SceneManager.LoadScene` for networked scenes while scene
management is on; clients desync.

## Useful events
| `SceneEventType` | Meaning |
|---|---|
| `Load` / `LoadComplete` | per-client start and finish |
| `LoadEventCompleted` | all clients done (or timed out: `ClientsThatTimedOut`) |
| `Synchronize` / `SynchronizeComplete` | late joiner received current scenes and objects |
| `Unload` / `UnloadEventCompleted` | additive scene unloaded |

## Late join and additive
- On connect, NGO synchronizes the client: loads the active scene and additive scenes, then spawns
  NetworkObjects. `ClientSynchronizationMode` `Single` (default) or `Additive` (keep already-loaded
  scenes, useful with a persistent bootstrap scene).
- In-scene placed NetworkObjects are matched by a GlobalObjectIdHash: don't instantiate copies of
  them at runtime, and don't change their scene after spawn.
- `VerifySceneBeforeLoading` callback lets the server/client veto scenes (e.g. client-only UI scenes).
- Additive unload with `UnloadScene(scene)` must pass the `Scene` struct from the load event.

## Gotchas
- Spawning NetworkObjects before `LoadEventCompleted` puts them in the wrong scene or spawns them
  on clients that have not loaded yet.
- Loading while a previous scene event is in progress returns `SceneEventInProgress`.
- DontDestroyOnLoad NetworkObjects survive Single loads; destroy or despawn them deliberately.

## Verify
- [ ] Two clients plus host transition together; a late joiner lands in the same scene with all objects.
- [ ] Log of scene events shows no timeouts on a throttled connection (Network Simulator).
