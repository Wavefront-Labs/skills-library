---
id: computing-software.game-programming.unreal-engine.custom-netserialize-and-quantization
name: custom-netserialize-and-quantization
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, netserialize, quantization, struct-ops-type-traits, fvector-netquantize, replication, bandwidth, game-programming]
level: advanced
status: draft
description: "Write custom NetSerialize for Unreal USTRUCTs: TStructOpsTypeTraits, bit-level FArchive writes, FVector_NetQuantize types, compressed rotators and validating bandwidth."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/CoreUObject/UObject/TStructOpsTypeTraitsBase2", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Engine/FVector_NetQuantize", "https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom NetSerialize and quantization

**Goal:** send a replicated struct (or RPC parameter) in fewer bits than default property-by-property
replication.

## First reach for built-in quantized types
| Type | Precision |
|---|---|
| `FVector_NetQuantize` | whole units (0 decimal places) |
| `FVector_NetQuantize10` / `100` | 1 / 2 decimal places |
| `FVector_NetQuantizeNormal` | unit vectors, 16 bits per component |
| `FRotator::SerializeCompressedShort` | 16 bits per axis |
Swapping `FVector` for `FVector_NetQuantize10` in a struct is often enough.

## Custom NetSerialize
```cpp
USTRUCT()
struct FHitInfo {
    GENERATED_BODY()
    UPROPERTY() FVector_NetQuantize10 Location;
    UPROPERTY() uint8 BoneIndex = 0;
    UPROPERTY() float Damage = 0.f;      // 0..1000
    UPROPERTY() bool bCritical = false;

    bool NetSerialize(FArchive& Ar, UPackageMap* Map, bool& bOutSuccess) {
        bOutSuccess = true;
        Location.NetSerialize(Ar, Map, bOutSuccess);
        Ar << BoneIndex;
        uint32 Q = Ar.IsSaving() ? FMath::Clamp(FMath::RoundToInt(Damage * 4.f), 0, 4000) : 0;
        Ar.SerializeInt(Q, 4001);                          // ~12 bits instead of 32
        if (Ar.IsLoading()) Damage = Q / 4.f;
        uint8 Crit = bCritical; Ar.SerializeBits(&Crit, 1); bCritical = Crit;
        return true;
    }
};
template<> struct TStructOpsTypeTraits<FHitInfo> : TStructOpsTypeTraitsBase2<FHitInfo> {
    enum { WithNetSerializer = true };                    // without this NetSerialize is ignored
};
```

## Rules
- One function both writes and reads: branch on `Ar.IsSaving()/IsLoading()` only for conversions, so
  the bit layout is identical both ways.
- A struct with `NetSerialize` replicates **atomically** (whole struct when any field changes), not
  per property. Good for consistency (location + normal together), costly for large structs.
- Add `WithNetSharedSerialization = true` only when serialization does not depend on the connection
  (no UObject pointers); the server then serializes once for all clients.
- `WithNetDeltaSerializer` is for delta-aware containers (see FFastArraySerializer).
- UObject pointers go through `Map->SerializeObject(Ar, UClass, Obj)`.
- With Iris replication, structs use NetSerializers instead; this pattern applies to the generic
  replication system.

## Verify
- [ ] Network Insights / `stat net` shows the property's bits drop.
- [ ] Round-trip unit test: serialize to `FNetBitWriter`, read with `FNetBitReader`, values within quantization error.
