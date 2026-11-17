---
id: computing-software.game-programming.unity.multiplayer-play-mode-testing
name: multiplayer-play-mode-testing
category: computing-software
field: game-programming
product: unity
tags: [unity, multiplayer-play-mode, netcode-for-gameobjects, network-simulator, testing, game-programming]
level: practitioner
status: draft
description: "Test Unity multiplayer locally with Multiplayer Play Mode virtual players and tags, plus the Network Simulator for latency, jitter and packet loss presets."
sources: ["https://docs.unity3d.com/Packages/com.unity.multiplayer.playmode@1.3/manual/index.html", "https://docs-multiplayer.unity3d.com/netcode/current/tutorials/testing/testing_locally/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiplayer Play Mode and network simulator

**Goal:** run host plus clients from one editor and test under realistic bad networks.

## Multiplayer Play Mode (MPPM)
1. Install `com.unity.multiplayer.playmode` (Unity 6 / 2023.1+). Window > Multiplayer > **Multiplayer
   Play Mode**.
2. Activate up to 3 **Virtual Players** (separate editor processes sharing the project, no cloning).
   Entering play mode starts all of them.
3. **Tags**: assign tags per player (Server, Client, Bot) and branch startup code:
```csharp
var tags = Unity.Multiplayer.Playmode.CurrentPlayer.ReadOnlyTags();
if (tags.Contains("Server")) NetworkManager.Singleton.StartServer();
else NetworkManager.Singleton.StartClient();
```
Unity 6 also supports Play Mode Scenarios to launch local builds and remote instances together.

## Network Simulator
Install `com.unity.multiplayer.tools`. Add **Network Simulator** component next to NetworkManager
(works with Unity Transport). Presets (Home Broadband, Mobile 4G, Mobile 2.5G) or custom: packet delay,
jitter, loss %. Change at runtime via `NetworkSimulator.ChangeConnectionPreset(...)` and trigger
scenarios (connection lost, lag spike) for testing reconnection.

## What to test
- Prediction/interpolation visibly smooth at 150 ms + 30 ms jitter.
- Late join, host migration or disconnect handling with packet loss 5%.
- Ownership changes and RPC ordering under delay.

## Gotchas
- Virtual players consume RAM; close them when not needed.
- Simulator affects only Unity Transport in development builds/editor; it does nothing in release
  builds by design.
- Clone-based tools (ParrelSync) and MPPM should not both be used on a project.

## Verify
- [ ] One button starts host + 2 clients; a test checklist is run at Mobile 4G preset before release.
