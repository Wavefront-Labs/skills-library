---
id: computing-software.game-programming.unreal-engine.push-model-replication
name: push-model-replication
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-replication, push-model, mark-property-dirty, replication-performance, game-programming]
level: practitioner
status: draft
description: "Cut Unreal server CPU on property replication with the push model: enabling it, DOREPLIFETIME_WITH_PARAMS bIsPushBased, MARK_PROPERTY_DIRTY_FROM_NAME and pitfalls."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/property-replication-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Push model replication

**Goal:** the server stops comparing every replicated property every net update; properties are
only considered when code marks them dirty.

## Enable
- Build.cs: `PublicDependencyModuleNames.Add("NetCore");`
- `DefaultEngine.ini`: `[SystemSettings] net.IsPushModelEnabled=1` (default on in recent UE5 versions;
  verify for yours).

## Declare
```cpp
#include "Net/UnrealNetwork.h"
#include "Net/Core/PushModel/PushModel.h"
void AMyChar::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& Out) const {
    Super::GetLifetimeReplicatedProps(Out);
    FDoRepLifetimeParams P; P.bIsPushBased = true;
    DOREPLIFETIME_WITH_PARAMS_FAST(AMyChar, Health, P);
    P.Condition = COND_OwnerOnly;
    DOREPLIFETIME_WITH_PARAMS_FAST(AMyChar, Ammo, P);
}
void AMyChar::SetHealth(float V) {
    Health = V;
    MARK_PROPERTY_DIRTY_FROM_NAME(AMyChar, Health, this);
}
```
Make the replicated fields private with setters so nobody writes them without marking dirty.

## How it behaves
Dirty marking is a hint: the property is compared only when dirty. Not marking = change never
replicates (silently). Marking without a change costs a compare, nothing sent.

## Combine with
- Net update frequency / dormancy: push model reduces per-update cost; dormancy removes actors from
  consideration altogether.
- Replication Graph or Iris for very high actor counts. Iris uses its own dirty tracking but honours
  push-model marks.

## Gotchas
- Properties of structs: marking the struct property dirty is required after member edits.
- Blueprint-set replicated variables are handled by the engine (Blueprint setter marks dirty), but C++
  writes need the macro.
- Arrays modified in place (`Arr[i] = x`) need marking too.

## Verify
- [ ] Insights/Net profiler: replication compare time per frame drops with many actors.
- [ ] Each replicated property has a setter that marks dirty (grep for direct writes).
