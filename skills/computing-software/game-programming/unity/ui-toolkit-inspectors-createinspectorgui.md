---
id: computing-software.game-programming.unity.ui-toolkit-inspectors-createinspectorgui
name: ui-toolkit-inspectors-createinspectorgui
category: computing-software
field: game-programming
product: unity
tags: [unity, createinspectorgui, ui-toolkit, custom-inspectors, propertyfield, editor-scripting, game-programming]
level: practitioner
status: draft
description: "Build Unity custom inspectors and property drawers with UI Toolkit: CreateInspectorGUI, PropertyField binding, UXML layouts, conditional fields and TrackPropertyValue."
sources: ["https://docs.unity3d.com/Manual/UIE-HowTo-CreateCustomInspector.html", "https://docs.unity3d.com/ScriptReference/Editor.CreateInspectorGUI.html", "https://docs.unity3d.com/ScriptReference/PropertyDrawer.CreatePropertyGUI.html", "https://docs.unity3d.com/Manual/UIE-Binding.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UI Toolkit inspectors

**Goal:** custom inspectors with retained-mode UI, automatic binding, undo and multi-edit.

## Inspector
```csharp
[CustomEditor(typeof(Spawner)), CanEditMultipleObjects]
public class SpawnerEditor : Editor {
    [SerializeField] VisualTreeAsset uxml;   // assign default reference on the script asset
    public override VisualElement CreateInspectorGUI() {
        var root = uxml ? uxml.Instantiate() : new VisualElement();
        var mode = new PropertyField(serializedObject.FindProperty("mode"));
        var radius = new PropertyField(serializedObject.FindProperty("radius"));
        root.Add(mode); root.Add(radius);
        root.TrackPropertyValue(serializedObject.FindProperty("mode"), p =>
            radius.style.display = p.enumValueIndex == 1 ? DisplayStyle.Flex : DisplayStyle.None);
        root.Add(new Button(() => ((Spawner)target).SpawnNow()) { text = "Spawn now" });
        return root;
    }
}
```
- `PropertyField` binds automatically when the inspector is bound: undo, prefab override bolding and
  multi-object editing come for free.
- In UXML use `<uie:PropertyField binding-path="radius"/>`; `binding-path` maps to serialized names.
- If `CreateInspectorGUI` returns null, Unity falls back to `OnInspectorGUI` (IMGUI).

## Property drawers
```csharp
[CustomPropertyDrawer(typeof(RangeInt))]
public class RangeIntDrawer : PropertyDrawer {
    public override VisualElement CreatePropertyGUI(SerializedProperty p) {
        var row = new VisualElement { style = { flexDirection = FlexDirection.Row } };
        row.Add(new PropertyField(p.FindPropertyRelative("start")));
        row.Add(new PropertyField(p.FindPropertyRelative("length")));
        return row;
    }
}
```
Unity 2022.2+ draws default inspectors with UI Toolkit, so UITK drawers work everywhere; IMGUI-only
drawers still work via IMGUIContainer fallback.

## Gotchas
- Initial values are set after binding; read them in `TrackPropertyValue` callbacks or schedule
  (`root.schedule.Execute`) rather than in CreateInspectorGUI directly.
- Calling target methods bypasses Undo; wrap with `Undo.RecordObject`.
- UI state (foldouts) persists with `viewDataKey`.

## Verify
- [ ] Undo, prefab overrides and multi-select editing work on every field.
- [ ] Conditional fields update immediately when the controlling field changes.
