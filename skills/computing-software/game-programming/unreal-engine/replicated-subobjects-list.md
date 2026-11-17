---
id: computing-software.game-programming.unreal-engine.replicated-subobjects-list
name: replicated-subobjects-list
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, replicated-subobjects, addreplicatedsubobject, replicatesubobjects, uobject-replication, game-programming]
level: advanced
status: draft
description: "Replicate plain UObjects in Unreal with the registered subobjects list: bReplicateUsingRegisteredSubObjectList, AddReplicatedSubObject, lifetime and net conditions."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/replicating-uobjects-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/GameFramework/AActor/AddReplicatedSubObject"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replicated subobjects list

**Goal:** replicate UObjects owned by an actor or component (inventory items, ability instances)
without hand-written `ReplicateSubobjects` overrides.

## Subobject class
```cpp
UCLASS() class UInventoryItem : public UObject {
    GENERATED_BODY()
public:
    virtual bool IsSupportedForNetworking() const override { return true; }
    UPROPERTY(Replicated) int32 Count = 0;
    void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& Out) const override {
        Super::GetLifetimeReplicatedProps(Out);
        DOREPLIFETIME(UInventoryItem, Count);
    }
};
```
RPCs on a plain UObject need `GetFunctionCallspace`/`CallRemoteFunction` forwarding to the owning actor.

## Owner (actor or component)
```cpp
AMyActor::AMyActor() { bReplicates = true; bReplicateUsingRegisteredSubObjectList = true; }

void AMyActor::AddItem() {                                    // server only
    UInventoryItem* Item = NewObject<UInventoryItem>(this);  // outer = owning actor
    Items.Add(Item);
    AddReplicatedSubObject(Item);                             // optional ELifetimeCondition, e.g. COND_OwnerOnly
}
void AMyActor::RemoveItem(UInventoryItem* Item) {
    RemoveReplicatedSubObject(Item);                          // before dropping the last reference
    Items.Remove(Item);
}
```
For components use `UActorComponent::AddReplicatedSubObject` with the component's
`bReplicateUsingRegisteredSubObjectList`.

## Rules
- Also replicate the pointer array (`UPROPERTY(Replicated) TArray<TObjectPtr<UInventoryItem>> Items`)
  so clients know which objects belong where; the list only makes the objects' properties replicate.
- Remove from the list before destroying or the object keeps replicating (and stays referenced).
- Do not mix the legacy `ReplicateSubobjects` override and the list on the same owner; set
  `net.SubObjects.CompareWithLegacy 1` while migrating to catch differences.
- Clients create the subobject on first receipt; outer must be the owning actor (or its component).
- Iris requires the registered list; legacy overrides are unsupported there.

## Verify
- [ ] Item count changes appear on clients; removed items are destroyed client-side after GC.
- [ ] Owner-only condition: other clients never receive the items (check in Network Insights).
