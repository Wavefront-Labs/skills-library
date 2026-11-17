---
id: computing-software.game-programming.unreal-engine.uproperty-specifiers
name: uproperty-specifiers
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, cpp, uproperty-specifiers, uproperty, reflection, blueprint-exposure, meta-specifiers, game-programming]
level: practitioner
status: draft
description: "Pick UPROPERTY specifiers: edit/visible scope, Blueprint access, replication, SaveGame, Transient, Instanced, and meta like ClampMin, EditCondition, AllowPrivateAccess."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-uproperties", "https://dev.epicgames.com/documentation/en-us/unreal-engine/property-specifiers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UPROPERTY specifiers

**Goal:** every C++ property is visible where designers need it, protected where they don't, and
correctly handled by GC, serialization and replication.

## Edit and visibility (pick one)
| Specifier | Archetype (class defaults) | Instance (placed in level) |
|---|---|---|
| `EditAnywhere` | edit | edit |
| `EditDefaultsOnly` | edit | - |
| `EditInstanceOnly` | - | edit |
| `VisibleAnywhere` / `VisibleDefaultsOnly` / `VisibleInstanceOnly` | read-only | read-only |

Component pointers created in the constructor: `VisibleAnywhere` (you edit the component's *properties*,
not the pointer). `EditAnywhere` on a component pointer lets designers null it out.

## Blueprint access
- `BlueprintReadOnly` / `BlueprintReadWrite`; private/protected members need
  `meta = (AllowPrivateAccess = "true")`.
- `BlueprintAssignable` (multicast delegates), `BlueprintCallable` (delegate call), `BlueprintGetter=Fn`/`BlueprintSetter=Fn`.
- `Category = "Combat|Damage"` (required for Blueprint-exposed properties in engine-style code; `|` nests).

## Serialization, GC and networking
- Any `UPROPERTY()` UObject pointer is a GC reference (use `TObjectPtr<UType>`). Raw UObject* without
  UPROPERTY can dangle.
- `Transient`: not saved; zero-filled on load (runtime caches).
- `SaveGame`: included when serializing with `FArchive::ArIsSaveGame` (save systems).
- `Replicated` / `ReplicatedUsing = OnRep_Health` + `DOREPLIFETIME` in `GetLifetimeReplicatedProps`.
- `Instanced` / `EditInlineNew` (on the class): per-owner subobject instances editable inline.
- `Config` / `GlobalConfig` with `UCLASS(config=Game)`: read from ini.
- `AdvancedDisplay`, `Interp` (Sequencer-animatable), `NoClear`, `SimpleDisplay`.

## Common meta specifiers
```cpp
UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Movement",
          meta = (ClampMin = "0.0", UIMin = "0.0", UIMax = "2000.0", Units = "cm/s"))
float MaxSpeed = 600.f;

UPROPERTY(EditAnywhere, Category = "AI", meta = (EditCondition = "bUsePatrol", EditConditionHides))
TObjectPtr<AActor> PatrolStart;

UPROPERTY(EditAnywhere, Category = "Loot", meta = (AllowedClasses = "/Script/Engine.StaticMesh"))
FSoftObjectPath Mesh;

UPROPERTY(EditAnywhere, meta = (GetOptions = "GetSocketNames"))   // dropdown from a UFUNCTION returning TArray<FString>
FName Socket;

UPROPERTY(EditAnywhere, meta = (MakeEditWidget = "true"))          // 3D widget in viewport for FVector/FTransform
FVector Target;
```
Also: `DisplayName`, `ToolTip` (or a `//` comment above the property), `InlineEditConditionToggle`,
`TitleProperty` for arrays of structs, `Bitmask`/`BitmaskEnum`.

## Gotchas
- Initialise defaults in the declaration or constructor; changing a C++ default doesn't update
  Blueprint children that already overrode it.
- Renaming a property loses saved values: add a CoreRedirect (`+PropertyRedirects=(OldName=...,NewName=...)`).
- Bitfield `uint8 bFlag : 1` works with UPROPERTY; `bool` is simpler.

## Verify
- [ ] Details panel shows each property only where intended (defaults vs instance).
- [ ] No UObject pointer members lack UPROPERTY (search the header).
