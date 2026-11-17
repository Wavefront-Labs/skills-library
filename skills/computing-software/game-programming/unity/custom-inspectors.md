---
id: computing-software.game-programming.unity.custom-inspectors
name: custom-inspectors
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-editor-scripting, editor-extension, custom-inspector, customeditor, serializedobject, serializedproperty, uitoolkit-inspector, undo, game-programming]
level: practitioner
status: docs-checked
description: "Write Unity custom inspectors: CustomEditor, CreateInspectorGUI (UI Toolkit), OnInspectorGUI (IMGUI), SerializedObject Update/ApplyModifiedProperties, multi-object caveats."
sources: ["https://docs.unity3d.com/Manual/editor-CustomEditors.html", "https://docs.unity3d.com/ScriptReference/SerializedObject.html", "https://docs.unity3d.com/Manual/UIE-HowTo-CreateCustomInspector.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom inspectors

**Goal:** replace the default Inspector for a MonoBehaviour or ScriptableObject safely.

## Basics
- Custom Inspectors only work for types deriving from MonoBehaviour or ScriptableObject; for a plain
  serializable class use a `PropertyDrawer` (derive from `PropertyDrawer`, `[CustomPropertyDrawer(typeof(T))]`,
  override `CreatePropertyGUI`).
- Create a class deriving from `Editor` with `[CustomEditor(typeof(MyComponent))]`.
- The script must be in an `Editor` folder or an Editor-only assembly definition, because the
  `UnityEditor` namespace is not accessible elsewhere; otherwise standalone builds fail.
- `[CanEditMultipleObjects]` lets one editor edit several selected objects. `Editor.target` is the
  inspected object.

## UI Toolkit (the manual strongly recommends UI Toolkit over IMGUI)
- Override `public override VisualElement CreateInspectorGUI()`, build a root `VisualElement`, return it.
  UXML can be loaded with a `VisualTreeAsset` field and `inspectorUXML.CloneTree()`.
- Binding is automatic: `CreateInspectorGUI()` does an implicit bind after you return your tree; set a
  control's `binding-path` to the field name (`make`, `yearBuilt`).
- `PropertyField` works for most serialized property types, including custom serializable classes and
  arrays, and shows the custom property drawer if one exists. It adjusts when the variable type changes,
  but UI Builder cannot preview it. Page style class: `unity-base-field__aligned`.
- Page shows `FillDefaultInspector` as a related link (not opened).

## IMGUI
```csharp
[CustomEditor(typeof(LookAtPoint))][CanEditMultipleObjects]
public class LookAtPointEditor : Editor {
    SerializedProperty lookAtPoint;
    void OnEnable() { lookAtPoint = serializedObject.FindProperty("lookAtPoint"); }
    public override void OnInspectorGUI() {
        serializedObject.Update();
        EditorGUILayout.PropertyField(lookAtPoint);
        serializedObject.ApplyModifiedProperties();
    }
}
```
Page notes: OnInspectorGUI works like OnGUI but runs in the Inspector; the Script field disappears
unless you draw it. `OnSceneGUI` runs in the Scene view and can use `Handles`; the example wraps edits in
`EditorGUI.BeginChangeCheck`/`EndChangeCheck` with `Undo.RecordObject`. 2D GUI in OnSceneGUI needs
`Handles.BeginGUI()`/`EndGUI()`.

## SerializedObject
- Handles dirtying serialized fields so changes are undoable, tracked as scene changes, and styled for
  Prefab overrides. Using it is the recommended approach in custom Editors over modifying targets directly.
- It opens a data stream to one or more targets. Changes to a `SerializedProperty` must be flushed with
  `ApplyModifiedProperties`. If you keep an instance for more than one frame, call `Update` before reading.
- `Editor.serializedObject` persists for the Editor's lifetime; the base `OnInspectorGUI` calls `Update`
  and `ApplyModifiedProperties`. If you override and call `base.OnInspectorGUI()` then change properties on a
  button press, call `ApplyModifiedProperties` before the method exits or the change is lost.
- `ApplyModifiedProperties` does not respect validation in property setters; also validate in
  `OnValidate`.
- Value getters such as `floatValue` are not multi-select friendly: setting affects all targets, reading
  returns the first target's value.
- Members listed: `ApplyModifiedPropertiesWithoutUndo`, `FindProperty`, `isEditingMultipleObjects`,
  `targetObjects`, `hasModifiedProperties`.

## Checked
Date: 2026-11-07

Read in full: the IMGUI "Create custom Editors" page, the UI Toolkit "Create a custom Inspector" page
and the `SerializedObject` page including its examples. The `PropertyField`, `InspectorElement` and
`SerializedProperty` pages were not opened.

Removed because the pages do not confirm it: "UI Toolkit default in Unity 2022.2+" (the page shows
2022.3+ for the how-to only), the Spawner/Respawn sample and its `targets` loop, `DrawDefaultInspector`
and `InspectorElement.FillDefaultInspector` usage, `PrefabUtility.RecordPrefabInstancePropertyModifications`,
the `m_`-prefix naming rule and null-on-typo claim, and the Verify list.

Method: documentation only; no commands were run.
