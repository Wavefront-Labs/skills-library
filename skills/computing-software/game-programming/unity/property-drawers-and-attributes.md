---
id: computing-software.game-programming.unity.property-drawers-and-attributes
name: property-drawers-and-attributes
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-editor-scripting, property-drawer, propertyattribute, custom-attributes, decorator-drawer, uitoolkit-inspector, game-programming]
level: practitioner
status: docs-checked
description: "Write custom PropertyDrawers for Serializable classes and PropertyAttributes, with UI Toolkit (CreatePropertyGUI) and IMGUI (OnGUI) versions, per Unity's PropertyDrawer docs."
sources: ["https://docs.unity3d.com/ScriptReference/PropertyDrawer.html", "https://docs.unity3d.com/Manual/editor-PropertyDrawers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property drawers and attributes

**Goal:** reusable inspector widgets applied by type or by attribute, instead of a custom Editor per component.

## Two uses of a PropertyDrawer
1. Customize the GUI of every instance of a `[Serializable]` class: attach with `[CustomPropertyDrawer(typeof(YourClass))]`.
2. Customize script members that carry a custom `PropertyAttribute`: the attribute class extends `PropertyAttribute` (and may store parameters as public members); the drawer extends `PropertyDrawer` and is tagged `[CustomPropertyDrawer(typeof(YourAttribute))]`. The built-in `[Range(0f, 10f)]` is the worked example.

Place the attribute class in a regular (runtime) script; place the drawer in an editor script inside a folder called `Editor`. In the drawer, the `attribute` property gives the attribute instance (not applicable to class drawers), `fieldInfo` the reflected field and `preferredLabel` the label.

## UI Toolkit or IMGUI
- UI Toolkit: override `CreatePropertyGUI(SerializedProperty)` and return a `VisualElement`.
- IMGUI: override `OnGUI(Rect, SerializedProperty, GUIContent)`; override `GetPropertyHeight` to say how tall the field is, in pixels.
- UI Toolkit cannot run inside IMGUI: a drawer that only has a UI Toolkit implementation does not work inside an IMGUI custom Inspector or a parent IMGUI drawer. From Unity 2022.2 the default Inspector uses UI Toolkit exclusively in custom PropertyDrawers, but you may still need IMGUI when the drawer is called from a custom Editor. Before 2022.2 Unity recommends implementing both versions or using the drawer only in UI Toolkit inspectors.
- Unity's Manual page recommends UI Toolkit for new Editor extensions.

```csharp
// Runtime script
[Serializable] public class Ingredient { public string name; public int amount = 1; public IngredientUnit unit; }

// Editor script (UI Toolkit)
[CustomPropertyDrawer(typeof(Ingredient))]
public class IngredientDrawerUIE : PropertyDrawer
{
    public override VisualElement CreatePropertyGUI(SerializedProperty property)
    {
        var container = new VisualElement();
        container.Add(new PropertyField(property.FindPropertyRelative("amount")));
        container.Add(new PropertyField(property.FindPropertyRelative("unit")));
        container.Add(new PropertyField(property.FindPropertyRelative("name"), "Fancy Name"));
        return container;
    }
}
```

## IMGUI rules from the docs
- Wrap drawing in `EditorGUI.BeginProperty(position, label, property)` / `EndProperty()` so prefab override logic works on the whole property.
- `EditorGUILayout` functions are not usable in PropertyDrawers, for performance reasons; compute `Rect`s and use `EditorGUI`.
- Draw child fields with `GUIContent.none` when you draw the label yourself, and restore `EditorGUI.indentLevel` afterwards.
- Check `property.propertyType` (for example `SerializedPropertyType.Float` / `Integer`) and show a `LabelField` message when the attribute is used on an unsupported type.

## Gotchas
- Lists and arrays: the `SerializedProperty` passed to `CreatePropertyGUI` represents each item in the list; to customize the list itself you must wrap the property accordingly.
- For cleanup (for example detaching from editor events) implement `IDisposable` on the drawer; it is invoked when the Editor is destroyed.
- Keep each PropertyDrawer in its own file with a matching name: default object references can be assigned to only one PropertyDrawer, and with several types in one file the assigned type is the one matching the file name, otherwise the first defined.

## Verify
- [ ] The drawer renders in the default Inspector and, if used from custom Editors, in IMGUI too.
- [ ] Prefab overrides apply to the whole property.

## Checked
Confirmed against the PropertyDrawer script reference and the Property Drawers (IMGUI) manual page: two uses, `CustomPropertyDrawer`, `CreatePropertyGUI`/`OnGUI`/`GetPropertyHeight`, UI Toolkit versus IMGUI rules and the 2022.2 note, `BeginProperty`, `EditorGUILayout` restriction, array behaviour, `IDisposable`, default object reference file rule. Removed because the pages do not state them: the built-in attribute list other than `Range`, the ReadOnly and FloatRange samples, `DecoratorDrawer`, `fieldInfo.GetValue` versus undo and multi-edit claims.
Method: docs-only read of cited pages, 2026-11-08
