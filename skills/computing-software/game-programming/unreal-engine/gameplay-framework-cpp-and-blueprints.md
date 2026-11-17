---
id: computing-software.game-programming.unreal-engine.gameplay-framework-cpp-and-blueprints
name: gameplay-framework-cpp-and-blueprints
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal, cpp, blueprints, gameplay-framework, gamemode, gamestate, playercontroller, playerstate, pawn, character, actor, actorcomponent, uclass, uproperty, ufunction, blueprintimplementableevent, garbage-collection, replication, enhanced-input, live-coding, unreal-insights, game-programming]
level: practitioner
status: draft
description: "Use Unreal's gameplay framework correctly: which class owns what (GameMode, PlayerController, Pawn...), splitting C++ and Blueprints, UPROPERTY/UFUNCTION rules, and GC gotchas."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-reflection-system"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unreal gameplay framework: C++ and Blueprints

**Goal:** put each piece of game logic in the class Unreal expects, so it works in
multiplayer and with the engine's tooling; build the systems in C++ and the content and
tuning in Blueprints.

## Who owns what
| Class | Exists on | Put here |
|---|---|---|
| `AGameModeBase` / `AGameMode` | **Server only** | Rules: spawning, scoring rules, win conditions, which Pawn/Controller classes to use. |
| `AGameStateBase` | Server + all clients (replicated) | Match state everyone sees: time remaining, team scores. |
| `APlayerController` | Server + the owning client | Input handling, UI ownership, camera; persists across Pawn deaths. |
| `APlayerState` | Server + all clients | Per-player public data: name, score, team. Survives respawn. |
| `APawn` / `ACharacter` | Server + relevant clients | The body: movement, health, abilities. `ACharacter` adds capsule + `UCharacterMovementComponent` with built-in network prediction. |
| `UActorComponent` / `USceneComponent` | Wherever its owner is | Reusable behaviour (health, inventory, interaction). |
| `UGameInstance` | Each process, whole session | Data that survives level loads (settings, session info). |

Classic mistakes: storing score on the Pawn (lost on death), reading GameMode on a
client (it's `nullptr` there), putting input on the Pawn when it should survive
possession changes.

## C++ / Blueprint split
- C++: base classes, systems, performance-sensitive loops, anything replicated or
  complex. Blueprints: subclasses that set meshes, tuning values, VFX/SFX, one-off level
  scripting. Designers iterate in BP without recompiling.
- Expose hooks:
```cpp
UCLASS()
class MYGAME_API AMyCharacter : public ACharacter {
    GENERATED_BODY()
public:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Combat")
    float MaxHealth = 100.f;

    UFUNCTION(BlueprintCallable, Category="Combat")
    void ApplyDamageSimple(float Amount);

    UFUNCTION(BlueprintImplementableEvent, Category="Combat")
    void OnDied();                       // implemented in BP (play montage, ragdoll)

    UFUNCTION(BlueprintNativeEvent, Category="Combat")
    bool CanBeDamaged() const;           // C++ default in CanBeDamaged_Implementation, BP may override
protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
    TObjectPtr<class UHealthComponent> Health;
};
```
- Specifier meanings: `EditDefaultsOnly` = editable on the class defaults, `EditAnywhere`
  = also per-instance in levels, `VisibleAnywhere` = shown, not editable (use for
  component pointers).
- Create components in the constructor with `CreateDefaultSubobject<T>(TEXT("Name"))`;
  find other actors' components at runtime (`BeginPlay`), not in the constructor —
  constructors run on the Class Default Object at editor load too.

## Garbage collection gotchas
- Any `UObject*` member that must stay alive **must** be a `UPROPERTY()` (or held via
  `TObjectPtr` in a UPROPERTY / `TStrongObjectPtr`). A raw pointer member is invisible
  to GC and becomes dangling after a collection — the classic "random crash after a
  minute".
- Use `TWeakObjectPtr` for references you don't own; check `IsValid()` before use
  (actors can be pending kill).
- Never `new`/`delete` UObjects; use `NewObject<T>()` / `SpawnActor<T>()` / `Destroy()`.

## Workflow notes
- Live Coding (Ctrl+Alt+F11) is fine for function bodies; after changing headers
  (new UPROPERTYs, class layout), close the editor and build from the IDE to avoid
  corrupted Blueprints.
- Use Enhanced Input (Input Actions + Mapping Contexts) — the legacy input system is
  deprecated in UE5.
- Tick is expensive at scale: disable it (`PrimaryActorTick.bCanEverTick = false`)
  unless needed; use timers or events instead.
- Profile with `stat unit`, `stat game`, and **Unreal Insights** (`-trace=default`).

## Verify
- [ ] Rules in GameMode, shared state in GameState/PlayerState, input in PlayerController.
- [ ] Every UObject pointer member is a UPROPERTY or a weak pointer.
- [ ] Designers can tune key values in BP defaults without touching C++.
- [ ] Works in PIE with "Play As Client" and 2 players (catches server-only assumptions).
- [ ] No unnecessary ticking actors in `stat game` / Insights.
