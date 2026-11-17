---
id: computing-software.game-programming.unreal-engine.gameinstance-lifetime-across-levels
name: gameinstance-lifetime-across-levels
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gameplay-framework, gameinstance, persistent-data, level-transitions, game-programming]
level: practitioner
status: draft
description: "Use Unreal's UGameInstance for state that survives level loads: lifetime, Init/Shutdown, what belongs there vs subsystems, and multiplayer caveats."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Engine/UGameInstance", "https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GameInstance lifetime across levels

**Goal:** keep session-wide state (selected character, settings loaded, online session) alive across
`OpenLevel`, without turning GameInstance into a god object.

## Lifetime
- Created at engine start (one per game process; one per PIE instance), destroyed at shutdown.
- `Init()` runs once after creation (no world yet in standalone at first call); `Shutdown()` on exit.
- `OnStart()` when the first world starts. Survives every level travel — unlike GameMode,
  GameState, PlayerController and Pawns which are recreated per level.
- Set the class in Project Settings > Maps & Modes > Game Instance Class.

## Access
```cpp
UMyGameInstance* GI = GetGameInstance<UMyGameInstance>();      // from actors
UMyGameInstance* GI = Cast<UMyGameInstance>(UGameplayStatics::GetGameInstance(WorldContext));
```

## Prefer UGameInstanceSubsystem
Put each concern (save system, analytics, matchmaking) in its own `UGameInstanceSubsystem`: same
lifetime, auto-created, accessed by `GI->GetSubsystem<USaveSubsystem>()`, no editing of the
GameInstance class. Keep GameInstance itself thin (startup flow, error/network failure handlers).

## Useful hooks
- `HandleNetworkFailure` / `HandleTravelFailure` (via `GEngine->OnNetworkFailure()` /
  `OnTravelFailure()`) to return players to the menu with a message.
- `LoadComplete`, `OnWorldChanged` for level-change awareness.

## Multiplayer caveats
- GameInstance is **local**: never replicated. Each client and the server have their own.
- To carry per-player state across server travel use PlayerState (with seamless travel
  `CopyProperties`) or re-send from client GameInstance after travel.

## Gotchas
- Storing pointers to actors in GameInstance -> dangling after level change (use
  `TWeakObjectPtr` or ids).
- In PIE with multiple players each has its own GameInstance; static singletons would be shared
  and wrong.

## Verify
- [ ] Data set in menu level is readable after `OpenLevel` to gameplay level.
- [ ] Network failure returns to menu with an error rather than a hang.
