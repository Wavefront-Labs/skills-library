---
id: computing-software.game-programming.unity.scriptableobject-createinstance-and-cloning
name: scriptableobject-createinstance-and-cloning
category: computing-software
field: game-programming
product: unity
tags: [unity, scriptableobject, createinstance, instantiate, assetdatabase, createasset, game-programming]
level: practitioner
status: docs-checked
description: "Create ScriptableObjects at runtime with CreateInstance, clone authored assets with Instantiate, and save them as .asset files with AssetDatabase.CreateAsset."
sources: ["https://docs.unity3d.com/ScriptReference/ScriptableObject.CreateInstance.html", "https://docs.unity3d.com/ScriptReference/Object.Instantiate.html", "https://docs.unity3d.com/ScriptReference/AssetDatabase.CreateAsset.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ScriptableObject CreateInstance and cloning

**Goal:** runtime-created or per-player copies of ScriptableObject (SO) data without corrupting authored assets.

## Create from scratch
```csharp
var cfg = ScriptableObject.CreateInstance<WeaponConfig>();
cfg.damage = 12;
```
`ScriptableObject.CreateInstance` has three overloads: by type name (`string`), by `System.Type`, and the generic
`CreateInstance<T>()`. To make an SO bound to a `.asset` file from the
Editor UI, the Script Reference points to `CreateAssetMenuAttribute`.

## Clone an authored asset
```csharp
[SerializeField] CharacterStats baseStats;   // authored asset
CharacterStats runtime;
void Awake() { runtime = Instantiate(baseStats); }   // independent copy
```
`Object.Instantiate` makes a copy of an object, similar to the Editor's Duplicate command, and returns the clone. Mutate
the clone (`runtime`), not the authored `baseStats`, so every user does not share the change.

## Save as asset (editor tools only)
```csharp
#if UNITY_EDITOR
var so = ScriptableObject.CreateInstance<LevelData>();
AssetDatabase.CreateAsset(so, "Assets/Data/Levels/Level_03.asset");
AssetDatabase.AddObjectToAsset(subSo, so);   // extra object in the same asset file
#endif
```
Rules from the `AssetDatabase.CreateAsset` reference:
- The path is project relative and must use a native asset extension (`.asset` for arbitrary assets, `.mat` for
  materials, `.anim` for animations); otherwise Unity reports an error.
- An existing asset at that path is overwritten.
- You cannot create assets in `Assets/StreamingAssets`, and you cannot create a prefab with it (use `PrefabUtility`).
- It cannot create non-native assets such as text or image files.
- Do not call it during import (for example from a ScriptedImporter or Postprocessor): it can make import non-deterministic
  and logs a warning.
- After creating an asset file, `AssetDatabase.AddObjectToAsset` adds more objects to the file; order does not matter and
  no object is the root asset.

## Verify
- [ ] Exiting Play Mode leaves authored assets unchanged (check the version control diff).
- [ ] Editor tool paths end in `.asset` and are outside `StreamingAssets`.

## Checked
Date: 2026-11-09. Read in full: Script Reference pages ScriptableObject.CreateInstance, AssetDatabase.CreateAsset and
Object.Instantiate (the clone-with-no-position overload and remarks). Removed as not on those pages: the warning for
`new` on an SO, `OnEnable`/`OnDisable` timing, `Destroy(runtime)` and Memory Profiler lifetime advice,
`EditorUtility.SetDirty`, `AssetDatabase.SaveAssets`, and the shallow-copy and non-serialized-field gotchas.
Method: docs-checked 2026-11-09 against the three Unity Script Reference pages named above.
