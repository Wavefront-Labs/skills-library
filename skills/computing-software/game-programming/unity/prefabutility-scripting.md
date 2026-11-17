---
id: computing-software.game-programming.unity.prefabutility-scripting
name: prefabutility-scripting
category: computing-software
field: game-programming
product: unity
tags: [unity, prefab, prefabutility, editor-scripting, loadprefabcontents, instantiateprefab, game-programming]
level: practitioner
status: docs-checked
description: "Edit Unity prefab assets from Editor scripts: LoadPrefabContents then SaveAsPrefabAsset and UnloadPrefabContents, and InstantiatePrefab versus Instantiate."
sources: ["https://docs.unity3d.com/ScriptReference/PrefabUtility.html", "https://docs.unity3d.com/ScriptReference/PrefabUtility.LoadPrefabContents.html", "https://docs.unity3d.com/ScriptReference/PrefabUtility.InstantiatePrefab.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PrefabUtility scripting

**Goal:** automate prefab work (add a component to many prefabs, place linked instances) without breaking prefab links.
All of `PrefabUtility` lives in the `UnityEditor` namespace: use it only in Editor code.

## Edit a prefab asset directly
```csharp
using UnityEditor; using UnityEngine;

public static class PrefabEdit
{
    [MenuItem("Examples/Add BoxCollider to Prefab Asset")]
    static void AddBoxColliderToPrefab()
    {
        GameObject assetRoot = Selection.activeObject as GameObject;
        string assetPath = AssetDatabase.GetAssetPath(assetRoot);
        GameObject contentsRoot = PrefabUtility.LoadPrefabContents(assetPath);  // isolated scene
        contentsRoot.AddComponent<BoxCollider>();
        PrefabUtility.SaveAsPrefabAsset(contentsRoot, assetPath);               // save changes
        PrefabUtility.UnloadPrefabContents(contentsRoot);                       // release memory
    }

    [MenuItem("Examples/Add BoxCollider to Prefab Asset", true)]
    static bool Validate()
    {
        GameObject go = Selection.activeObject as GameObject;
        return go != null && PrefabUtility.IsPartOfPrefabAsset(go);
    }
}
```
- `LoadPrefabContents(assetPath)` loads the prefab asset into an isolated scene and returns the root GameObject, so you
  modify the contents directly instead of going through an instance. The reference says this is useful for batch operations.
- If you modified the contents, call `SaveAsPrefabAsset` to save, then `UnloadPrefabContents` to release the prefab and
  isolated scene from memory.- `SaveAsPrefabAsset(go, path)` creates a prefab asset at the path from the GameObject and its children without modifying
  the input objects. `SaveAsPrefabAssetAndConnect` does the same and also turns the GameObject into an instance of the
  new prefab.
- `PrefabUtility.EditPrefabContentsScope` is listed by Unity as the related scoped helper.

## Placing instances: InstantiatePrefab versus Instantiate
`PrefabUtility.InstantiatePrefab(asset)` is similar to `Instantiate` but creates a prefab connection. Without a scene
handle the prefab goes into the active scene; overloads take a destination `Scene` or a parent `Transform`.
`Object.Instantiate` does not create a prefab connection.

Do not instantiate prefabs from `OnValidate()` or `Awake()`: the order in which GameObjects become awake is not
deterministic, and Unity logs the warning "SendMessage cannot be called during Awake, CheckConsistency, or OnValidate".

## Queries (listed on the PrefabUtility class page)
- `GetPrefabAssetType`: enum such as Regular Prefab, Model Prefab, Prefab Variant.
- `GetPrefabInstanceStatus`: whether an instance is properly connected to its asset.
- `IsPartOfPrefabAsset`, `IsPartOfVariantPrefab`.
- `GetCorrespondingObjectFromSource`: the source prefab asset object for a GameObject or component, or null.
- `GetOutermostPrefabInstanceRoot`, `GetPrefabAssetPathOfNearestInstanceRoot`.

## Verify
- [ ] Every `LoadPrefabContents` call is paired with `UnloadPrefabContents`.
- [ ] Placed instances are created with `InstantiatePrefab` when they must stay linked.

## Checked
Date: 2026-11-09. Read in full: Script Reference PrefabUtility.LoadPrefabContents and PrefabUtility.InstantiatePrefab;
the PrefabUtility class page for the method summaries listed above. Removed as not confirmed on those pages: the
AssetDatabase.FindAssets/StartAssetEditing batching code, the claim that nested prefabs and variants are handled, the
recipe for creating prefab variants, `Undo.RegisterCreatedObjectUndo`, and the Safety and Verify items about version
control, idempotence and Hierarchy icons.
Method: docs-checked 2026-11-09 against the three Unity Script Reference pages named above.
