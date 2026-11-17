---
id: computing-software.game-programming.unreal-engine.uactorcomponent-and-scene-component-attachment
name: uactorcomponent-and-scene-component-attachment
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, uactorcomponent, uscenecomponent, component-attachment, setupattachment, attachtocomponent, game-programming]
level: practitioner
status: draft
description: "Choose UActorComponent vs USceneComponent in Unreal C++, create and attach components in constructors and at runtime, sockets, and attachment rules that bite."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/components-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Components/USceneComponent/AttachToComponent", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Components/UActorComponent"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UActorComponent vs USceneComponent and attachment

| Class | Has transform | Use for |
|---|---|---|
| `UActorComponent` | no | Logic: health, inventory, ability hooks |
| `USceneComponent` | yes, can attach | Pivots, spring arms, sockets for logic |
| `UPrimitiveComponent` | yes + render/collision | Meshes, shapes |

Prefer `UActorComponent` for pure logic: no transform update cost.

## Constructor (default subobjects)
```cpp
AMyPawn::AMyPawn() {
    Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
    SetRootComponent(Root);
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    Mesh->SetupAttachment(Root);                         // constructor: SetupAttachment only
    Muzzle = CreateDefaultSubobject<USceneComponent>(TEXT("Muzzle"));
    Muzzle->SetupAttachment(Mesh, TEXT("MuzzleSocket"));
    Health = CreateDefaultSubobject<UHealthComponent>(TEXT("Health"));   // no attachment
}
```

## Runtime
```cpp
UStaticMeshComponent* C = NewObject<UStaticMeshComponent>(this, TEXT("Attachment"));
C->SetStaticMesh(Mesh);
C->SetupAttachment(GetRootComponent());
C->RegisterComponent();                                  // required for runtime-created components
AddInstanceComponent(C);                                 // shows in details panel, survives copy
// or attach an existing component/actor:
Weapon->AttachToComponent(GetMesh(), FAttachmentTransformRules::SnapToTargetNotIncludingScale, TEXT("hand_r"));
```

## Component lifecycle hooks
`OnRegister` -> `InitializeComponent` (only with `bWantsInitializeComponent = true`) -> `BeginPlay`
-> `TickComponent` (`PrimaryComponentTick.bCanEverTick = true` in constructor) -> `EndPlay` ->
`OnUnregister`. Find components with `FindComponentByClass<T>()` or `GetComponents<T>(Array)`.

## Gotchas
- `AttachToComponent` in a constructor breaks CDO/Blueprint inheritance: use `SetupAttachment`.
- Changing a default subobject's name or removing it orphans Blueprint overrides; keep names stable.
- `KeepWorldTransform` vs `SnapToTarget` rules: wrong choice makes attached items jump or keep scale.
- Mobility: a child should not be less mobile than its parent (Static under Movable logs a warning);
  set Movable on anything you move at runtime.
- Destroying components: `DestroyComponent()`; never `delete`.
- Replicated components need `SetIsReplicatedByDefault(true)` (constructor) or `SetIsReplicated(true)`.

## Verify
- [ ] Blueprint child shows inherited components with editable properties.
- [ ] Runtime-added component renders/collides (registered) and is listed in the actor's details.
