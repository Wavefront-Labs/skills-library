---
id: computing-software.game-programming.unreal-engine.ffastarrayserializer-delta-arrays
name: ffastarrayserializer-delta-arrays
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-replication, fast-array-serializer, ffastarrayserializer, delta-replication, game-programming]
level: practitioner
status: draft
description: "Replicate big Unreal arrays with FFastArraySerializer: item/array structs, MarkItemDirty, PreReplicatedRemove/PostReplicatedAdd callbacks and ordering caveats."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/NetCore/FFastArraySerializer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FFastArraySerializer delta arrays

**Goal:** inventories, buff lists and scoreboards replicate only changed elements, with per-item
add/change/remove callbacks on clients.

## Declaration
```cpp
USTRUCT()
struct FInvEntry : public FFastArraySerializerItem {
    GENERATED_BODY()
    UPROPERTY() FName ItemId; UPROPERTY() int32 Count = 0;
    void PreReplicatedRemove(const struct FInvList& A);
    void PostReplicatedAdd(const struct FInvList& A);
    void PostReplicatedChange(const struct FInvList& A);
};
USTRUCT()
struct FInvList : public FFastArraySerializer {
    GENERATED_BODY()
    UPROPERTY() TArray<FInvEntry> Items;
    UPROPERTY(NotReplicated) TObjectPtr<UInventoryComponent> Owner;
    bool NetDeltaSerialize(FNetDeltaSerializeInfo& P) {
        return FFastArraySerializer::FastArrayDeltaSerialize<FInvEntry, FInvList>(Items, P, *this);
    }
};
template<> struct TStructOpsTypeTraits<FInvList> : TStructOpsTypeTraitsBase2<FInvList> {
    enum { WithNetDeltaSerializer = true };
};
// in component:
UPROPERTY(Replicated) FInvList Inventory;   // DOREPLIFETIME in GetLifetimeReplicatedProps
```

## Server mutations
```cpp
FInvEntry& E = Inventory.Items.AddDefaulted_GetRef(); E.ItemId = Id; E.Count = 1;
Inventory.MarkItemDirty(E);
E.Count += 4; Inventory.MarkItemDirty(E);
Inventory.Items.RemoveAt(i); Inventory.MarkArrayDirty();
```
Forgetting `MarkItemDirty` = the change never replicates.

## Client side
Callbacks run per element; the array-level `PostReplicatedReceive` (optional on the serializer)
fires once after a batch — use it to refresh UI once.

## Caveats
- **Order is not preserved** on clients (removals swap). Don't rely on index; sort client-side or
  store an explicit order field.
- Items are identified by `ReplicationID`; don't copy items between arrays expecting identity.
- Very large arrays still send the full state on initial replication.
- Iris replication system supports fast arrays via its own serializer (UE 5.4+) — keep standard
  declarations; check Iris notes when migrating.

## Verify
- [ ] Network profiler shows small deltas when one item changes in a 200-item inventory.
- [ ] Client callbacks fire once per add/change/remove.
