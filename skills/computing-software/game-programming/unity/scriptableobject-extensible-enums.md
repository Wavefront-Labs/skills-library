---
id: computing-software.game-programming.unity.scriptableobject-extensible-enums
name: scriptableobject-extensible-enums
category: computing-software
field: game-programming
product: unity
tags: [unity, scriptableobject, so-enum, extensible-enum, type-object, game-programming]
level: practitioner
status: draft
description: "Replace C# enums with ScriptableObject assets in Unity so designers add item types, damage types or teams without code changes; compare by reference, serialize safely."
sources: ["https://docs.unity3d.com/Manual/class-ScriptableObject.html", "https://unity.com/resources/create-modular-game-architecture-with-scriptable-objects-ebook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ScriptableObjects as extensible enums

**Goal:** categories (damage types, factions, item rarities) that designers extend by creating an
asset, with data attached, and no fragile integer reordering.

## Why not enums
- Serialized enums store the integer: inserting a value in the middle silently remaps every asset.
- Adding a value needs a programmer and a recompile.
- Behaviour/data per value ends up in `switch` statements across the codebase.

## Pattern
```csharp
[CreateAssetMenu(menuName = "Game/Damage Type")]
public class DamageType : ScriptableObject {
    public Color uiColor;
    public DamageType[] strongAgainst;
    public bool IsStrongAgainst(DamageType other) => System.Array.IndexOf(strongAgainst, other) >= 0;
}
public class Weapon : MonoBehaviour { [SerializeField] DamageType damageType; }
// comparison is reference equality:
if (hit.weakness == weapon.damageType) dmg *= 2;
```
Assets serialize by GUID, so renaming or moving them never breaks references.

## Use as dictionary keys
`Dictionary<DamageType, float> resist` works (reference hashing). For serialized lookups use a list of
`{DamageType type; float value;}` and build the dictionary in `OnEnable`.

## Saving to disk / network
References cannot go into JSON saves directly. Give each asset a stable id:
```csharp
[SerializeField, HideInInspector] string id;
void OnValidate() { if (string.IsNullOrEmpty(id)) id = System.Guid.NewGuid().ToString("N"); }
```
and resolve via a registry ScriptableObject listing all instances (built by an editor script or
Addressables label).

## Gotchas
- `null` is a valid "none" — decide whether to allow it or create an explicit `None` asset.
- Duplicating an asset with Ctrl+D copies the id field; regenerate on duplicate (check uniqueness in
  the registry's OnValidate).
- Do not put mutable runtime state in these assets (shared by every user, persists in editor).

## Verify
- [ ] Designer adds a new type asset and it appears in all dropdowns without code changes.
- [ ] Save/load round-trips via id after renaming the asset file.
