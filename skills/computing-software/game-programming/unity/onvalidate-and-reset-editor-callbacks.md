---
id: computing-software.game-programming.unity.onvalidate-and-reset-editor-callbacks
name: onvalidate-and-reset-editor-callbacks
category: computing-software
field: game-programming
product: unity
tags: [unity, monobehaviour, onvalidate-reset, onvalidate, reset, editor-callbacks, inspector-validation, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity's OnValidate and Reset editor-time callbacks safely: clamping and auto-wiring fields, when they fire, and what must never run inside them."
sources: ["https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnValidate.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.Reset.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OnValidate and Reset editor callbacks

**Goal:** catch bad inspector values and pre-fill references at edit time, without side effects that corrupt scenes or spam errors.

## When they run
| Callback | Fires | Use for |
|---|---|---|
| `Reset()` | Reset in the Inspector's context menu, or when a component is first added (drag and drop in the Inspector, or `GameObject.AddComponent` from an Editor script). Edit mode only: not called for components added at runtime. | Good default values and auto-wiring (`GetComponent`, find by tag). |
| `OnValidate()` | Editor-only. When the script is loaded or a value changes in the Inspector; also at other stages of normal Editor operation such as loading scenes, importing assets, building a Player and entering Play mode. | Validate serialized fields and enforce data constraints after Inspector edits. |

```csharp
public class Spawner : MonoBehaviour {
    [SerializeField] float interval = 1f;
    [SerializeField] int maxAlive = 10;
    [SerializeField] Collider area;

    void Reset() { area = GetComponent<Collider>(); }       // auto-wire on add

    void OnValidate() {
        interval = Mathf.Max(0.05f, interval);              // clamp, cheap
        maxAlive = Mathf.Clamp(maxAlive, 1, 500);
    }
}
```

## Rules
- Do not treat `OnValidate` as a general-purpose callback for all property changes or Editor-side logic; only validate the data that changed.
- It can be called often during Inspector interaction, and also from threads other than Unity's main thread (such as the loading thread). Do not create objects or call other non-thread-safe Unity API from it.
- You cannot reliably do Camera rendering from `OnValidate`; add a listener to `EditorApplication.update` and render on the next Editor update (see also `EditorApplication.delayCall`).
- `OnValidate` saves nothing itself. Values it assigns are written to disk only when the scene or asset is saved for another reason. When Unity calls it while loading or importing an object, the dirty state is cleared afterwards, so assignments made during a load are not scheduled for saving, even with `EditorUtility.SetDirty`.
- Do not rely on it to persist computed values, especially in Prefabs: a Prefab Variant stores only explicitly edited values as overrides. To persist a computed value in an asset, assign it from an explicit edit, for example an `AssetPostprocessor.OnPostprocessAllAssets` callback that saves the Prefab with `PrefabUtility.SavePrefabAsset`.
- Wrap editor-only API in `#if UNITY_EDITOR` so builds compile.

## Checked
Method: 2026-11-09 docs-only read of the MonoBehaviour.OnValidate and MonoBehaviour.Reset script reference pages in full. Confirmed the trigger conditions, edit-mode-only behaviour, threading, dirty-state and Prefab Variant notes. Removed claims the pages do not state: undo/redo and Awake ordering, the exact SendMessage error text, the Range and Min attribute advice, and the Verify checklist.
