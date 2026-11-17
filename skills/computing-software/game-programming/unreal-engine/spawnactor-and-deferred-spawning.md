---
id: computing-software.game-programming.unreal-engine.spawnactor-and-deferred-spawning
name: spawnactor-and-deferred-spawning
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, uclass, spawnactor, spawnactordeferred, finishspawning, game-programming]
level: practitioner
status: draft
description: "Spawn Unreal actors correctly with SpawnActor and SpawnActorDeferred/FinishSpawning, collision handling overrides, owners and instigators, and network authority."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/spawning-actors-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Engine/UWorld/SpawnActorDeferred"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SpawnActor and deferred spawning

**Goal:** spawned actors are initialised before BeginPlay sees them, don't silently fail to spawn,
and replicate properly.

## Basic spawn
```cpp
FActorSpawnParameters P;
P.Owner = this;                                  // used for net ownership and relevancy
P.Instigator = GetInstigator();                  // damage attribution
P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;
AProjectile* Proj = GetWorld()->SpawnActor<AProjectile>(ProjectileClass, MuzzleXf, P);
if (!Proj) { UE_LOG(LogTemp, Warning, TEXT("spawn failed")); }
```
`ProjectileClass` should be `TSubclassOf<AProjectile>` exposed as `UPROPERTY(EditDefaultsOnly)` so a
Blueprint subclass is spawned, not the native class.

## Collision handling
Default (from the class) may be `DontSpawnIfColliding`, returning nullptr when overlapping — the
classic "spawn sometimes doesn't happen". Pick explicitly: `AlwaysSpawn`, `AdjustIfPossibleButAlwaysSpawn`,
`AdjustIfPossibleButDontSpawnIfColliding`, `DontSpawnIfColliding`.

## Deferred spawn (set data before BeginPlay/construction)
```cpp
AEnemy* E = GetWorld()->SpawnActorDeferred<AEnemy>(EnemyClass, Xf, this, nullptr,
    ESpawnActorCollisionHandlingMethod::AlwaysSpawn);
E->Init(Archetype, Level);        // runs before construction script and BeginPlay
UGameplayStatics::FinishSpawningActor(E, Xf);   // or E->FinishSpawning(Xf)
```
Blueprint equivalent: "Expose on Spawn" variables on SpawnActor nodes.

## Networking
- Spawn replicated actors **on the server** only (`HasAuthority()`); `bReplicates = true` in the
  constructor. Clients spawning replicated actors creates local-only copies.
- Cosmetic actors (impact VFX) spawn locally on each machine, not replicated.

## Gotchas
- Spawning during another actor's construction or in the CDO crashes/asserts — spawn in BeginPlay or
  later.
- Lots of spawns per frame: pool frequently spawned actors (projectiles) instead.
- `SpawnActor` with a transform scale of zero produces invisible actors with broken collision.

## Verify
- [ ] Spawn inside geometry with each collision mode; behaviour matches expectations.
- [ ] Deferred-spawned actor's BeginPlay logs the initialised data.
