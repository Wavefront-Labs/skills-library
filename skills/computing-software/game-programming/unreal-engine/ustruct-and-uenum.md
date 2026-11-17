---
id: computing-software.game-programming.unreal-engine.ustruct-and-uenum
name: ustruct-and-uenum
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, cpp, ustruct, uenum, reflection, blueprinttype, uenum-class, game-programming]
level: practitioner
status: draft
description: "Declare reflected USTRUCTs and UENUMs: BlueprintType, GENERATED_BODY, struct ops (equality, NetSerialize), enum class with UMETA display names, bitflags and string conversion."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/structs-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/enumerations-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USTRUCT and UENUM

**Goal:** value types and enums that work in Blueprint, Details panels, data tables, saving and replication.

## USTRUCT
```cpp
USTRUCT(BlueprintType)
struct FWeaponStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite) float Damage = 10.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float FireRate = 0.1f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) TSoftObjectPtr<USoundBase> FireSound;

    bool operator==(const FWeaponStats& O) const { return Damage == O.Damage && FireRate == O.FireRate; }
};
```
- `F` prefix; `GENERATED_BODY()` required. Only `UPROPERTY` members are reflected (saved, replicated,
  visible to Blueprint, kept alive by GC).
- USTRUCTs can't have UFUNCTIONs. Put helpers in a Blueprint function library.
- Data table rows derive from `FTableRowBase`.
- Opt-in behaviours with `TStructOpsTypeTraits`:
```cpp
template<> struct TStructOpsTypeTraits<FWeaponStats> : TStructOpsTypeTraitsBase2<FWeaponStats>
{ enum { WithIdenticalViaEquality = true }; };          // also WithNetSerializer, WithSerializer, WithCopy
```
- Custom compact replication: implement `bool NetSerialize(FArchive&, UPackageMap*, bool& bOutSuccess)`
  and set `WithNetSerializer = true`.
- Blueprint auto-generates Make/Break nodes; `meta = (HasNativeMake = "...")` for custom ones.

## UENUM
```cpp
UENUM(BlueprintType)
enum class EWeaponState : uint8
{
    Idle       UMETA(DisplayName = "Idle"),
    Firing,
    Reloading,
    MAX        UMETA(Hidden)
};
```
- Blueprint-exposed enums must be `uint8`. Prefer `enum class`.
- To string: `UEnum::GetValueAsString(EWeaponState::Firing)` ("EWeaponState::Firing"),
  `StaticEnum<EWeaponState>()->GetDisplayNameTextByValue((int64)State)` for UI.
- Bitflags:
```cpp
UENUM(BlueprintType, meta = (Bitflags, UseEnumValuesAsMaskValuesInEditor = "true"))
enum class EDamageFlags : uint8 { None = 0 UMETA(Hidden), Fire = 1 << 0, Ice = 1 << 1, Crit = 1 << 2 };
ENUM_CLASS_FLAGS(EDamageFlags)
UPROPERTY(EditAnywhere, meta = (Bitmask, BitmaskEnum = "/Script/MyGame.EDamageFlags")) uint8 Flags;
```
  (`BitmaskEnum` takes the enum's path name in UE 5.1+.)

## Gotchas
- Reordering enum values changes saved/serialized numbers in assets; append new values, use redirects
  (`+EnumRedirects`) for renames.
- Large structs passed by value to Blueprint functions copy; use `const F...&`.
- Struct default values in Blueprint are captured when nodes are placed; changing C++ defaults
  doesn't update existing pins.

## Verify
- [ ] Struct round-trips through a SaveGame and a data table import.
- [ ] Enum display names show in Details dropdowns; hidden values don't.
