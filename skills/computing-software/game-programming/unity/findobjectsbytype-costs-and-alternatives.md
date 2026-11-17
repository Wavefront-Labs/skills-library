---
id: computing-software.game-programming.unity.findobjectsbytype-costs-and-alternatives
name: findobjectsbytype-costs-and-alternatives
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-gameobject, findobjectsbytype, findanyobjectbytype, object-registry, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity FindObjectsByType and FindAnyObjectByType correctly (inactive objects, interfaces, sortMode overloads) and replace them with registries or serialized references."
sources: ["https://docs.unity3d.com/ScriptReference/Object.FindObjectsByType.html", "https://docs.unity3d.com/ScriptReference/Object.FindAnyObjectByType.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FindObjectsByType costs and alternatives

**Goal:** get references to scene objects without searching all loaded objects on every call.

## The API
- `FindObjectsByType<T>()` returns all active loaded objects of type T (`T : Object`).
  `FindObjectsByType<T>(FindObjectsInactive)` can include components on inactive GameObjects; without that parameter
  inactive objects are not included.
- The overloads that take a `FindObjectsSortMode` are deprecated in the current docs: use `FindObjectsByType<T>()` or the
  `FindObjectsInactive` overload. A sort order relying on `InstanceID` cannot be maintained in future versions
  (InstanceID will be replaced by EntityId). The page notes that not sorting saves time, which can be significant when
  many objects are returned.
- `FindAnyObjectByType<T>()` returns an arbitrary active loaded object of that type, or null. It is not guaranteed to be
  the same object between calls. `FindFirstObjectByType` is obsolete; use `FindAnyObjectByType` if you do not need a
  specific instance. There is also a `FindObjectsInactive` overload.
- Neither returns assets (meshes, textures, prefabs) or objects with `HideFlags.DontSave` set;
  `Resources.FindObjectsOfTypeAll` avoids that limit.
- You cannot pass an interface type directly: find components of a base type and filter with LINQ `OfType`.
- In the Editor, `FindObjectsByType` searches the Scene view by default; for the Prefab stage use the `StageUtility`
  APIs.

## Cost
The docs do not give a per-call cost figure; they say "loaded objects" are searched. Treat these calls as something to
keep out of `Update`, and measure in the Profiler before deciding.

## Alternatives
1. **Serialized reference** assigned in the Inspector (`[SerializeField] Player player;`).
2. **Self-registration** in a static list (or a ScriptableObject runtime set):
```csharp
public class Enemy : MonoBehaviour {
    public static readonly List<Enemy> All = new();
    void OnEnable() => All.Add(this);
    void OnDisable() => All.Remove(this);
}
```
3. **Bootstrap injection**: one scene-root script finds references once and hands them down.

## Gotchas
- A static list is not reset by a stopped play session when domain reload is disabled; clear it yourself at startup.
- Do not remove from a list while iterating it; iterate a copy or backwards.

## Checked
Date: 2026-11-07.
Read in full: the Object.FindObjectsByType script reference page (all overloads, Remarks, sample, deprecation
warnings) and the Object.FindAnyObjectByType page (all overloads, Remarks, sample). Page text is the 6000.6 docs.
Corrected: the draft presented `FindObjectsByType<T>(FindObjectsSortMode.None)` as the main call; those overloads are
now deprecated. Removed as unconfirmed: "InstanceID sort costs extra", "faster than the old FindObjectOfType (which
sorted)", the claim that `FindObjectOfType`/`FindObjectsOfType` are obsolete (the page only says `FindFirstObjectByType`
is), the `GameObject.Find`/`FindWithTag` bullet, the "2023.1+" version gate, the profiler label, physics-query
alternative, the `[RuntimeInitializeOnLoadMethod]` advice and the invented Verify checklist. The alternatives are design
suggestions, not documented claims.
Method: documentation only; no commands were run.
