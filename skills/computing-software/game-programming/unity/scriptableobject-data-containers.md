---
id: computing-software.game-programming.unity.scriptableobject-data-containers
name: scriptableobject-data-containers
category: computing-software
field: game-programming
product: unity
tags: [unity, scriptableobject, createassetmenu, so-data-container, data-driven-design, weapon-stats, flyweight, onvalidate, serializefield, game-programming]
level: practitioner
status: docs-checked
description: "Model shared tuning data as ScriptableObject assets with CreateAssetMenu, save edits with EditorUtility.SetDirty, and use OnValidate only for validation, per Unity's docs."
sources: ["https://docs.unity3d.com/Manual/class-ScriptableObject.html", "https://docs.unity3d.com/ScriptReference/CreateAssetMenuAttribute.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnValidate.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ScriptableObject data containers

**Goal:** one asset per design concept (a weapon, an enemy archetype, a spawn table) that prefabs and systems reference, so designers tune in one place and memory holds one copy.

## What a ScriptableObject is
- A serializable Unity type derived from `UnityEngine.Object`. You derive your own class from it and create instances (usually from the Assets menu); the instances are assets, not components on GameObjects.
- Because it inherits `UnityEngine.Object`, instances can be dragged or picked into Inspector fields.
- Main value is as a data store, though it can define behavior. A common use is shared data used by many objects at runtime: a prefab whose MonoBehaviours store unchanging data gets a copy per instance, whereas a ScriptableObject referenced by all prefabs means one copy in memory.
- Quickest way to start: Assets > Create > Scripting > ScriptableObject Script (also via the Project window context menu or plus button).

## CreateAssetMenu
`[CreateAssetMenu(fileName = "Data", menuName = "ScriptableObjects/SpawnManagerScriptableObject", order = 1)]` on the class (the Manual's sample). `fileName` is the default file name of new instances, `menuName` the display name in the Assets/Create menu, `order` the position in that menu. Instances are stored as `.asset` files.

```csharp
[CreateAssetMenu(fileName = "Data", menuName = "ScriptableObjects/SpawnManagerScriptableObject", order = 1)]
public class SpawnManagerScriptableObject : ScriptableObject
{
    public string prefabName;
    public int numberOfPrefabsToCreate;
    public Vector3[] spawnPoints;
}

public class ScriptableObjectManagedSpawner : MonoBehaviour
{
    public GameObject entityToSpawn;
    public SpawnManagerScriptableObject spawnManagerValues; // drag the .asset in
}
```
The script file must have the same name as the class. Double-clicking a ScriptableObject reference field opens its Inspector; you can also write a custom Inspector for the type.

## Saving changes
- In the Editor you can save ScriptableObject data in Edit and Play mode; in a standalone Player you can only read the saved asset data.
- Changes made through the Inspector or Editor authoring tools are written to disk automatically.
- Changes made by script in Edit mode are not saved automatically: call `EditorUtility.SetDirty` on the object, otherwise the change appears in memory but reverts after closing and reopening the Editor. The Manual's sample adds an optional `AssetDatabase.SaveAssets()` to save immediately.

## OnValidate
- Editor-only; called when the script is loaded or a value changes in the Inspector. Intended use: validate serialized fields and enforce constraints in response to Inspector edits.
- It can also run when loading scenes, importing assets, building a Player and entering Play mode, and it can be called from threads other than the main thread, such as the loading thread. Do not create objects or call non-thread-safe Unity API from it.
- It saves nothing itself. Values it assigns are written only when the scene or asset is saved for another reason; during load or import Unity clears the dirty state afterwards, even if you call `EditorUtility.SetDirty`. Do not rely on it to persist computed values, especially in Prefabs (a Prefab Variant stores only explicitly edited values as overrides).
- The documented sample clamps `maxHealth` to at least 1 and `currentHealth` between 0 and `maxHealth` with `Mathf.Clamp`.

## Verify
- [ ] Two prefabs referencing the same asset see the same values when the asset is edited.
- [ ] Script-made edits to an asset use `EditorUtility.SetDirty` and survive an Editor restart.

## Checked
Confirmed against the ScriptableObject Manual page, the CreateAssetMenuAttribute reference and the MonoBehaviour.OnValidate reference. Removed because the pages do not state them: the WeaponData sample and its attributes, dictionary serialization advice, `FormerlySerializedAs`, build stripping of unreferenced assets, Resources/Addressables loading, folder naming, Profiler memory check and the Flyweight pattern label.
Method: docs-only read of cited pages, 2026-11-08
