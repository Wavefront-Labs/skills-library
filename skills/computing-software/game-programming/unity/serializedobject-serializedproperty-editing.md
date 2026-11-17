---
id: computing-software.game-programming.unity.serializedobject-serializedproperty-editing
name: serializedobject-serializedproperty-editing
category: computing-software
field: game-programming
product: unity
tags: [unity, serializedobject, serializedproperty, editor-scripting, undo, prefab-overrides, custom-editor, game-programming]
level: practitioner
status: docs-checked
description: "Edit Unity objects from editor code via SerializedObject/SerializedProperty for undo, prefab overrides and multi-object editing; Update and ApplyModifiedProperties rules."
sources: ["https://docs.unity3d.com/ScriptReference/SerializedObject.html", "https://docs.unity3d.com/ScriptReference/SerializedProperty.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SerializedObject and SerializedProperty editing

**Goal:** editor tools and inspectors that support Undo, prefab overrides, multi-selection and scene-dirty tracking
without extra editor API calls.

## Why not write fields directly
Setting `go.transform.localPosition = Vector3.zero` from an editor script works, but is not undoable, and you would have to
use other editor APIs to mark the object dirty so the change is saved with the Scene. `SerializedObject` and
`SerializedProperty` handle dirtying individual serialized fields so they go through the Undo system and are styled
correctly for Prefab overrides when drawn in the Inspector.

## Pattern (from the SerializedObject reference)
```csharp
var transforms = Selection.gameObjects.Select(go => go.transform).ToArray();
var so = new SerializedObject(transforms);            // several targets at once
so.FindProperty("m_LocalPosition").vector3Value = Vector3.zero;
so.ApplyModifiedProperties();                         // flush the changes
```
- Property names are serialized field names such as `m_LocalPosition`. In the Inspector, Shift+Right Click on a property
  name shows its path.
- A new `SerializedObject` is up to date. Changes made to properties must be flushed with `ApplyModifiedProperties`.
- If you keep a `SerializedObject` for more than one frame, call `Update()` before reading data, because the targets may
  have been changed elsewhere. Two `SerializedObject` streams on the same targets are independent and must be synchronised
  manually.
- With several targets the value getters (`floatValue`, `vector3Value`, ...) return only the first target's value, while
  assigning affects all targets. Use `hasMultipleDifferentValues` to detect mixed values.
- `ApplyModifiedProperties` does not run property-setter validation. Re-validate in `MonoBehaviour.OnValidate()` (for
  example clamp a value that a setter and a `Range` attribute also clamp).
- `ApplyModifiedPropertiesWithoutUndo` applies changes without registering an undo operation.

## Properties worth knowing (SerializedProperty reference)
- `arraySize`, `GetArrayElementAtIndex(i)`, `FindPropertyRelative(path)` for arrays and nested structures.
- `prefabOverride` (is the value different from its Prefab) and `isInstantiatedPrefab`.
- `managedReferenceValue` for a field with the `SerializeReference` attribute.
- `GetIterator()` on the `SerializedObject` returns the first property; `NextVisible` moves to the next visible one.
  `Next` descends into children and `Parent` navigates back up.

## In custom inspectors
`Editor.serializedObject` is a stream to all inspected targets, so `[CanEditMultipleObjects]` editors work with several
objects. It lives as long as the `Editor`, and the base `OnInspectorGUI` calls `Update` before drawing controls and
`ApplyModifiedProperties` after user interaction. If you add your own controls (for example a button that sets
properties), call `serializedObject.ApplyModifiedProperties()` before your method returns, or the edits are lost the next
time the base implementation calls `Update`.

## Verify
- [ ] Ctrl+Z reverts the tool's change.
- [ ] A custom inspector button's edits end with `ApplyModifiedProperties`.

## Checked
Date: 2026-11-09. Read in full: Script Reference SerializedObject (Remarks and examples) and the SerializedProperty
overview plus member summaries. Removed as not on those pages: the `[field: SerializeField]` backing-field path format,
the `EditorGUI.showMixedValue` advice, the UI Toolkit `PropertyField`/`Bind` claim, the note that non-serialized members
are invisible, and the full `arraySize++` array-append recipe.
Method: docs-checked 2026-11-09 against the two Unity Script Reference pages named above.
