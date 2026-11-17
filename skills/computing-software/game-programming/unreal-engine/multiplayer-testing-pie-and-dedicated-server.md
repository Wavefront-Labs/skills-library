---
id: computing-software.game-programming.unreal-engine.multiplayer-testing-pie-and-dedicated-server
name: multiplayer-testing-pie-and-dedicated-server
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-replication, pie-multiplayer, unreal-dedicated-server, server-target, network-emulation, latency-simulation, netprofiler, net-profiler, multiplayer-testing, game-programming]
level: practitioner
status: draft
description: "Test Unreal multiplayer: PIE net modes, network emulation, launching standalone server and clients, building a dedicated server target and reading net logs."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/testing-multiplayer-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-dedicated-servers-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/using-network-emulation-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing multiplayer: PIE and dedicated servers

**Goal:** catch replication bugs before they ship by testing under the same conditions as players:
separate processes, a dedicated server, real latency and loss.

## PIE first
Play dropdown > Multiplayer Options: Number of Players, **Net Mode** (Play Standalone / As Listen
Server / As Client). "Run Under One Process" off gives separate processes (closer to reality,
slower). As Client starts a dedicated server in the background.

## Network emulation
Editor Preferences > Level Editor > Play > Multiplayer Options > Enable Network Emulation with
profiles (Average, Bad) or custom: incoming/outgoing latency min/max, packet loss %. Console
equivalents per process: `Net PktLag=150`, `Net PktLagVariance=30`, `Net PktLoss=5`,
`Net PktOrder=1`, `Net PktDup=1`. Packaged builds: same commands or `-PktLag=150` on the command line
(not in Shipping).

## Standalone processes from the command line
```
UnrealEditor.exe "<ProjectDir>/MyGame.uproject" /Game/Maps/Arena -server -log -port=7777
UnrealEditor.exe "<ProjectDir>/MyGame.uproject" 127.0.0.1:7777 -game -log -windowed -ResX=1280 -ResY=720
```
`-game` runs uncooked content without the editor UI; useful for multiple clients on one machine.

## Dedicated server target
Requires a source-built engine. Add `Source/MyGameServer.Target.cs`:
```csharp
public class MyGameServerTarget : TargetRules
{
    public MyGameServerTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Server;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("MyGame");
    }
}
```
Package with Platforms > (platform) > Build Target: MyGameServer, or
`RunUAT BuildCookRun -project=... -server -serverplatform=Linux -noclient -cook -build -stage -pak -archive`.
Server binaries strip rendering; guard client-only code with `#if !UE_SERVER` or runtime NetMode checks.

## What to watch
- Log categories: `LogNet`, `LogNetTraffic` (verbose), `LogRep`. Raise with
  `log LogNet Verbose`.
- `stat net` for bandwidth, packets, channels per second.
- Networking Insights: launch with `-trace=net,default -NetTrace=1`, open the trace in Unreal Insights
  to see bytes per property/RPC per frame.
- `p.NetShowCorrections 1` for movement corrections.

## Typical bugs this catches
Things that only work on the listen-server host (RepNotify not called on server), client spawns, missing
ownership for RPCs, uninitialised replicated state at join-in-progress, cosmetics executing on a
dedicated server (crash on missing rendering).

## Verify
- [ ] Test plan run in: Standalone, Listen Server (2 players), Client with dedicated server (3 players).
- [ ] Same plan under the Bad emulation profile.
- [ ] Packaged dedicated server boots, accepts a packaged client, and its log has no warnings in LogNet.
