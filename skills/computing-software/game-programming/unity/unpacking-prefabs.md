---
id: computing-software.game-programming.unity.unpacking-prefabs
name: unpacking-prefabs
category: computing-software
field: game-programming
product: unity
tags: [unity, unpack-prefab, prefabs, prefabutility, game-programming]
level: practitioner
status: docs-checked
description: "Unpack Unity prefab instances (Unpack vs Unpack Completely) deliberately, understand the lost connection and overrides, and re-link or replace them with prefabs."
sources: ["https://docs.unity3d.com/Manual/UnpackingPrefabInstances.html", "https://docs.unity3d.com/ScriptReference/PrefabUtility.UnpackPrefabInstance.html", "https://docs.unity3d.com/ScriptReference/PrefabUtility.ReplacePrefabAssetOfPrefabInstance.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unpacking prefabs

**Goal:** break a prefab link only when you mean to, and recover when someone did it by accident.

## What unpacking does
In the Hierarchy, right-click the prefab instance > Prefab > **Unpack**. Unity converts the instance into a GameObject with no links to the original prefab asset (the asset itself is kept) and saves the instance's overrides into the GameObject. Unpack only affects the selected instance:
- Nested prefabs inside it remain prefab instances inside the new GameObject.
- Unpacking a prefab variant makes the root a new instance of the variant's base prefab; every property of the variant that differs from the base becomes an override.

**Prefab > Unpack Completely** also unpacks nested prefabs, and unpacks a variant down to its base set of GameObjects.

```csharp
PrefabUtility.UnpackPrefabInstance(root, PrefabUnpackMode.OutermostRoot, InteractionMode.UserAction);
PrefabUtility.UnpackPrefabInstance(root, PrefabUnpackMode.Completely, InteractionMode.AutomatedAction);
```
- The object passed must be the root of a prefab instance. `ArgumentException` is thrown if it is not a prefab instance root, or if it is part of a prefab asset (prefab contents opened in prefab editing mode are not excluded).
- `OutermostRoot` replaces the instance with the prefab asset's contents (retaining override values); `Completely` also unpacks nested instances so only regular GameObjects remain.
- `InteractionMode` determines whether the action is undoable.

## When to unpack
- Kitbashing a one-off set piece from prefab parts where future prefab edits must not ripple.
- Using an instance as the start of a new object that should no longer follow the original prefab.

## Re-linking or replacing
`PrefabUtility.ReplacePrefabAssetOfPrefabInstance(instanceRoot, newPrefabAssetRoot, mode)` swaps the prefab asset behind an instance in a Scene (or a nested instance in another prefab):
- Keeps the instance root position, rotation and scale and merges in the new asset's contents, by default keeping as many overrides and references as possible by name-based matching. The root GameObject and its components are always reused, so references to them survive.
- `ObjectMatchMode.ByHierarchy` matches by full hierarchy path (siblings need unique names); `ObjectMatchMode.ByName` only matches when the name is unique. Duplicate names cannot be matched.
- No property overrides are deleted from the serialized state, so replacing back and forth between assets is non-destructive for property overrides; clean unused overrides later from the Hierarchy or Overrides window. Added components are kept only if a name match exists; added GameObjects go to the new instance root if their parent has no match.
- A settings overload takes `PrefabReplacingSettings`. Related: `PrefabUtility.ConvertToPrefabInstance` (turn plain GameObjects into instances of a prefab).

## Checked
Method: 2026-11-09 docs-only read of the Unity manual page on unpacking prefab instances and the script reference pages for PrefabUtility.UnpackPrefabInstance and ReplacePrefabAssetOfPrefabInstance (the latter through its first overload and remarks). Removed unconfirmed claims: Unity version gates, undo-after-save behaviour, IsPartOfAnyPrefab detection, Prefab Mode and scene-reference gotchas, missing-prefab salvage, and the Verify list.
