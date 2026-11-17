---
id: creative-arts.animation.blender.library-overridable-props
name: library-overridable-props
category: creative-arts
field: animation
product: blender
tags: [blender, library-overridable, overridable-property, library-overrides, custom-properties, rig-ui]
level: advanced
status: docs-checked
description: "Make custom and add-on properties editable on linked assets: the Library Overridable option, property_overridable_library_set from Python, and registered property override flags."
sources:
  - https://docs.blender.org/manual/en/latest/files/custom_properties.html
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html
  - https://docs.blender.org/api/current/bpy.types.bpy_struct.html
  - https://docs.blender.org/api/current/bpy_types_enum_items/property_override_flag_items.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# library-overridable-props

Goal: animators can edit and key rig sliders on a linked character in a shot file.

## Why it matters

For custom properties, whether they can be overridden is decided in the asset file; the Custom Properties edit pop-up has a **Library Overridable** option: "Allow the property to be overridden when the data-block is linked."

## Set it in the asset file

- UI: Custom Properties panel > edit icon > check **Library Overridable**.
- Python, for many properties at once:

```python
import bpy
rig = bpy.data.objects["RIG_hero"]
for pb in rig.pose.bones:
    for key in pb.keys():
        if not key.startswith("_"):
            pb.property_overridable_library_set(f'["{key}"]', True)
```

`bpy_struct.property_overridable_library_set(property, overridable)` defines a property as overridable or not, **for custom properties only**, and returns True when the status was set. Call it on the owner (pose bone, object, and so on) with the property name in bracket form as above.

## Registered (add-on) properties

```python
bpy.types.Object.my_toggle = bpy.props.BoolProperty(override={'LIBRARY_OVERRIDABLE'})
```

`override` takes a set from *Property Override Flag Items*; the only item is `LIBRARY_OVERRIDABLE` ("Make that property editable in library overrides of linked data-blocks"). For a property to be overridable, its whole chain of parent properties must also be overridable.

## Checking in the shot

Outliner > Library Overrides > Properties view lists overridden properties; an edited property shows a teal-blue outline or background. You can also add or remove an override from a property's context menu (Add Override(s), Remove Override(s)).

## Gotchas

- The flag lives in the asset file; save the asset, then resync overrides in shots (`creative-arts.animation.blender.override-resync`).
- Overriding an existing animation is not possible; the override gets a new Action instead, and animated properties supersede overrides.

## Verify

Link the rig into a new file, make a library override with the rig editable, and edit the custom slider: the value is accepted, shows as overridden, and survives save and reload.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/custom_properties.rst, files/linked_libraries/library_overrides.rst) and the current Python API (bpy_struct.property_overridable_library_set, bpy.props override argument, Property Override Flag Items).
Confirmed: Library Overridable option and wording, method signature and custom-property restriction, the single flag and parent-chain note, override view and teal colour, animation rule. Removed unconfirmed claims: custom properties being non-overridable by default and greyed out on linked rigs, a gear icon for editing properties, data-block pointer properties resolving to linked IDs only, and drivers being evaluated on the override.
Method: documentation only; no commands were run.
