---
id: computing-software.game-programming.unity.scriptableobject-shared-variables
name: scriptableobject-shared-variables
category: computing-software
field: game-programming
product: unity
tags: [unity, scriptableobject, so-variable, variable-reference, data-binding, game-programming]
level: practitioner
status: draft
description: "Use ScriptableObject variable assets (FloatVariable, reference-or-constant fields) in Unity for decoupled shared state, with reset rules and change events."
sources: ["https://unity.com/how-to/architect-game-code-scriptable-objects", "https://github.com/roboryantron/Unite2017"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ScriptableObject shared variables

**Goal:** HUD, audio and gameplay read the same value (player HP, score) without referencing each
other — the "Unite 2017 FloatVariable" pattern — with its pitfalls handled.

## Core types
```csharp
public abstract class Variable<T> : ScriptableObject {
    [SerializeField] T initialValue;
    [System.NonSerialized] T runtime;
    public event System.Action<T> Changed;
    public T Value { get => runtime; set { runtime = value; Changed?.Invoke(value); } }
    void OnEnable() => runtime = initialValue;   // reset on load / domain reload
}
[CreateAssetMenu(menuName = "Vars/Float")] public class FloatVariable : Variable<float> {}

[System.Serializable]
public class FloatReference {           // designer picks constant or shared asset
    public bool useConstant = true; public float constant; public FloatVariable variable;
    public float Value => useConstant ? constant : variable.Value;
}
```

## Runtime value vs asset value
Writing a serialized field at runtime in the editor **changes the asset on disk** (persists after
play). Keep runtime in a `[NonSerialized]` field initialised from the serialized initial value, as
above.

## Reset caveat
`OnEnable` on ScriptableObjects runs when the asset is loaded — in the editor, that is once per domain
reload, not per play session. With Enter Play Mode Options (domain reload off), reset explicitly:
subscribe to `EditorApplication.playModeStateChanged` in an editor-only block, or have a bootstrap
call `ResetAll()` on a registry.

## Change events
- Unsubscribe in `OnDisable` of listeners; the asset outlives scenes, so stale listeners leak and
  throw on destroyed objects.
- Avoid polling `Value` in Update in UI; bind to `Changed`.

## When not to use
Per-instance state (each enemy's HP) does not belong in a shared asset. Use it for truly global
values or tuning constants.

## Verify
- [ ] Play, change the value, stop: the asset's inspector shows the original initial value.
- [ ] Load scene twice; no duplicated callbacks (log subscriber count).
