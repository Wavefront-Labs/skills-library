---
id: computing-software.game-programming.unreal-engine.child-actor-components-and-pitfalls
name: child-actor-components-and-pitfalls
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, child-actor-component, components, actors, replication, game-programming]
level: practitioner
status: draft
description: "Use Unreal Child Actor Components with care: spawn timing, class templates, replication and save problems, and safer alternatives like components or spawned attached actors."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/child-actor-components-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/Engine/Components/UChildActorComponent/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/components-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Child Actor components and pitfalls

**Goal:** know when a Child Actor Component (CAC) is acceptable and what to use instead.

## What it does
`UChildActorComponent` spawns an actor of `ChildActorClass` when the component registers and destroys
it when the component unregisters. The child is attached to the component and owned by the parent.
`ChildActorTemplate` (UE4.24+) lets you edit the child's default properties per instance.

```cpp
Turret = CreateDefaultSubobject<UChildActorComponent>(TEXT("Turret"));
Turret->SetChildActorClass(ATurretActor::StaticClass());
Turret->SetupAttachment(RootComponent);
// later
ATurretActor* T = Cast<ATurretActor>(Turret->GetChildActor());
```

## Known problems
- **Construction script re-runs** (moving the parent in editor) destroy and respawn the child; editor
  references to it break and per-instance edits can reset.
- **Replication**: the child spawns locally on each machine as well as replicating if it is
  replicated, leading to duplicates or mismatched net GUIDs unless the child is non-replicated or
  setup carefully. Many teams ban replicated CACs.
- **Save/load and level streaming**: children are transient-ish; references from other actors do not
  survive reliably.
- `GetChildActor()` can be null early (BeginPlay ordering) or after the class changes.
- Nested CAC chains multiply all of the above and cost spawn time.

## Alternatives
1. **Actor components / scene components** when the "child" is really behaviour or visuals.
2. **Spawn and attach in BeginPlay** (server-only for replicated actors) with
   `AttachToComponent(..., FAttachmentTransformRules::SnapToTargetNotIncludingScale, Socket)`, store
   the pointer as a replicated UPROPERTY.
3. Level instances / packed level actors for static prefab-like assemblies.

## Acceptable uses
Cosmetic, non-replicated, non-referenced sub-actors in single-player or client-only visuals.

## Verify
- [ ] No replicated actor class uses CAC with a replicated child; multiplayer test shows no duplicates.
