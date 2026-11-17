---
id: computing-software.game-programming.unity.hideflags-and-editor-only-objects
name: hideflags-and-editor-only-objects
category: computing-software
field: game-programming
product: unity
tags: [unity, hideflags-dontsave, hideflags, editoronly, editor-scripting, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity HideFlags (DontSave, HideAndDontSave, NotEditable) and the EditorOnly tag for helper objects that must not be saved, shown or built, and destroy them yourself."
sources: ["https://docs.unity3d.com/ScriptReference/HideFlags.html", "https://docs.unity3d.com/ScriptReference/Object-hideFlags.html", "https://docs.unity3d.com/Manual/Tags.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HideFlags and editor-only objects

**Goal:** preview meshes, helper objects and generated materials that never end up saved in scenes or builds.

## Flags
`HideFlags` is a `[Flags]` enum (bit mask) set through `Object.hideFlags`; it controls destruction, saving and
visibility in inspectors.

| Flag | Effect (script reference wording) |
|---|---|
| `None` | normal, visible object; the default |
| `HideInHierarchy` | object does not appear in the hierarchy |
| `HideInInspector` | not possible to view it in the inspector |
| `NotEditable` | not editable in the Inspector |
| `DontSaveInEditor` | not saved to the Scene in the editor |
| `DontSaveInBuild` | not saved when building a player |
| `DontUnloadUnusedAsset` | not unloaded by `Resources.UnloadUnusedAssets` |
| `DontSave` | not saved to the Scene and not destroyed when a new Scene loads; shortcut for `DontSaveInBuild \| DontSaveInEditor \| DontUnloadUnusedAsset` |
| `HideAndDontSave` | GameObject not shown in the Hierarchy, not saved to the Scene, not unloaded by `Resources.UnloadUnusedAssets` |

Setting `DontSaveInEditor`, `DontSaveInBuild` or `HideInHierarchy` removes the object internally from the Scene and from
its current physics scene (2D and 3D), and triggers its `OnDisable` and `OnEnable` calls. These flags control whether
non-persistent instantiated assets (ScriptableObjects, Materials not yet saved with `AssetDatabase`) are serialized to
the scene.

```csharp
public class ExampleClass : MonoBehaviour
{
    private Material ownedMaterial;
    void OnEnable()
    {
        ownedMaterial = new Material(Shader.Find("Diffuse"));
        ownedMaterial.hideFlags = HideFlags.HideAndDontSave;
        GetComponent<Renderer>().sharedMaterial = ownedMaterial;
    }
    // Objects created as hide and don't save must be explicitly destroyed by the owner of the object.
    void OnDisable() { DestroyImmediate(ownedMaterial); }
}
```

## Ownership rule
The script reference states that objects created as hide and don't save must be explicitly destroyed by their owner;
`DontSave` also means the object is not destroyed when a new Scene is loaded. Destroy such objects in `OnDisable` or
`OnDestroy`.

## EditorOnly tag
A tag is a reference word assigned to GameObjects (one tag per GameObject). The built-in tags, which do not appear in
the Tag Manager, are Untagged, Respawn, Finish, EditorOnly, MainCamera, Player and GameController. A GameObject tagged
`EditorOnly` in a Scene is destroyed when the game builds, and so are its child GameObjects. Tag names, once created in
the Tag and Layer Manager (Add Tag... in the Inspector), cannot be renamed.

## Checked
Date: 2026-11-07.
Read in full: HideFlags and Object.hideFlags script reference pages (6000.6 docs, field table, Remarks, sample) and the
"Assign tags to GameObjects" manual page.
Corrected: the draft said `HideAndDontSave` included `NotEditable`; the page defines it without `NotEditable`. The draft
also said `DontSaveInBuild` is "stripped from builds"; the page says "not saved when building a player".
Removed as unconfirmed: the `[ExecuteAlways]` preview sample, "leaked objects" warnings, Memory Profiler advice, the
claim that components on EditorOnly objects referenced at runtime are null in builds, "hidden objects still run
scripts", the editor menu tip and the invented Verify checklist.
Method: documentation only; no commands were run.
