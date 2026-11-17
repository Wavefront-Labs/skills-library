---
id: computing-software.game-programming.unity.scriptableobject-runtime-state-pitfalls
name: scriptableobject-runtime-state-pitfalls
category: computing-software
field: game-programming
product: unity
tags: [unity, scriptableobject, so-runtime-state, play-mode-persistence, onenable, hideflags, nonserialized, game-programming]
level: practitioner
status: draft
description: "Avoid ScriptableObject runtime-state bugs: edits persisting after Play Mode, values differing in builds, OnEnable timing and reset patterns for mutable SO state."
sources: ["https://docs.unity3d.com/Manual/class-ScriptableObject.html", "https://docs.unity3d.com/ScriptReference/ScriptableObject.OnEnable.html", "https://docs.unity3d.com/Manual/ConfigurableEnterPlayMode.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ScriptableObject runtime state pitfalls

**Goal:** use ScriptableObjects that hold mutable game state (player health variable, runtime set,
current score) without Editor/build divergence.

## The core behaviour
- In the **Editor**, an SO asset is the asset on disk. Changing a field during Play Mode changes the
  loaded object, and Unity saves it the next time the project saves. The value survives exiting
  Play Mode.
- In a **build**, the SO is loaded from read-only data; changes live in memory until the SO is
  unloaded, then they are gone. Nothing is written back.
- If no loaded scene/object references the SO, Unity can unload it (`Resources.UnloadUnusedAssets`,
  scene change), and the next load gets the original values. So state can "randomly" reset in builds.

## Pattern: separate authored value from runtime value
```csharp
[CreateAssetMenu(menuName = "Game/Float Variable")]
public class FloatVariable : ScriptableObject, ISerializationCallbackReceiver
{
    public float initialValue;               // authored, saved
    [System.NonSerialized] public float runtimeValue;   // never serialized, never saved

    public void OnAfterDeserialize() { runtimeValue = initialValue; }
    public void OnBeforeSerialize() { }
}
```
`[NonSerialized]` keeps runtime data out of the asset file. Reset it in `OnAfterDeserialize` or
from an explicit `ResetState()` called by a bootstrap at game start.

## Enter Play Mode options
With **Enter Play Mode Options > Disable Domain Reload / Scene Reload** (faster iteration), static
fields and already-loaded SOs are NOT reset between plays and `OnEnable` may not run again. Reset
explicitly:
```csharp
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
static void ResetStatics() { s_instances.Clear(); }
```
For SO state, have a `GameBootstrap` call `ResetState()` on a list of resettable assets on start.

## Runtime sets and lists
Runtime sets (`List<Enemy>` on an SO that enemies add themselves to in `OnEnable`) keep stale
entries after Play Mode if the list is serialized. Mark the list `[NonSerialized]` and clear it on
play start; null-check entries when iterating.

## Avoiding accidental asset edits
- Never write to authored fields at runtime; treat them as const. Code review rule: SO setters only
  touch `[NonSerialized]` fields.
- To get a mutable per-entity copy use `Instantiate(asset)` and destroy the copy when done.
- `hideFlags = HideFlags.DontSave` on runtime-created SOs (`ScriptableObject.CreateInstance`) stops
  them leaking into scenes.

## Verify
- [ ] Play, change state, stop: the asset's inspector shows the authored values, and `git status` shows
  no modified `.asset` files.
- [ ] Same test with Domain Reload disabled.
- [ ] Development build: state resets on new game, persists across scene loads when intended.
