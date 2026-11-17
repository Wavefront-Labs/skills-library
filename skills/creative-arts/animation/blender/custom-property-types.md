---
id: creative-arts.animation.blender.custom-property-types
name: custom-property-types
category: creative-arts
field: animation
product: blender
tags: [blender, custom-property-types, property-subtypes, property-subtype, custom-properties, id-properties, bpy]
level: practitioner
status: docs-checked
description: "Create the right kind of custom property: Float, Int, Boolean, String, arrays, Python and data-block types, subtypes like factor, angle, distance and colour, in UI and Python."
sources:
  - https://docs.blender.org/manual/en/latest/files/custom_properties.html
  - https://docs.blender.org/api/current/bpy.types.bpy_struct.html#bpy.types.bpy_struct.id_properties_ui
  - https://docs.blender.org/api/current/bpy.props.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# custom-property-types

Goal: custom properties that behave correctly as sliders, toggles, colours and links, for rigs, pipelines and drivers.

## In the UI

Object/Bone/Data/Scene Properties → *Custom Properties* → *New*, then the gear icon (*Edit Property*):
- **Type**: Float, Float Array, Integer, Integer Array, Boolean, Boolean Array, String, Data-Block (a reference to a Blender data-block), Python (edit a Python data type directly, for unsupported data types).
- **Subtype** (floats only): Plain Data, Pixel, Percentage, Factor, Angle, Time, Distance, Power, Temperature, Wavelength. Float arrays: Plain Data, Linear Color, Gamma-Corrected Color, Euler Angles, Quaternion Angles (colour subtypes need a value of 3 or 4 elements).
- Also: Property Name, Array Length (arrays longer than 7 elements are edited with *Edit Value*), Default, Min/Max, Soft limits, Step, Precision, Description, *Library Overridable*.

Subtype changes how the value displays and edits (Percentage suggests Min/Max of 0 and 100; the colour subtypes show a colour picker).

## In Python

```python
ob = bpy.context.object
ob["mass"] = 2.5                               # float
ob["tint"] = [1.0, 0.5, 0.2]                    # float array
ob["is_hero"] = True                            # bool
ob["target"] = bpy.data.objects["Cube"]         # data-block property
```
Set subtype, limits and default in the *Edit Property* dialog. `ob.id_properties_ui(key)` returns an object that manages the property's UI data, but the API pages do not document its methods, so check it in the Python console before scripting it.

## Custom vs registered properties

| | Custom (ID property) | Registered (`bpy.props` on a type) |
|---|---|---|
| Created | per data-block, any time | for every instance of the type, by an add-on |
| Survives without the add-on | yes | value kept as ID prop, UI lost |
| Access | `ob["name"]` | `ob.name` attribute |

Use custom properties for per-asset data (rig controls, pipeline metadata); registered properties for tool settings.

## Gotchas

- Pose-bone properties (`pose.bones["x"]["prop"]`) and bone properties (`bones["x"]["prop"]`) are different storage; rigs put animatable controls on pose bones.

## Verify

The property shows the expected widget (colour swatch, angle in degrees, toggle), is keyframable (`I` over it) and the Edit Property dialog shows the chosen subtype.

## Checked

Blender 5.2 manual (blender-v5.2-release, files/custom_properties) and Python API 5.2, read 2026-10-27.
- Property types, float and float-array subtype lists, array-length note (more than 7 elements need Edit Value), Min/Max, soft limits, step, precision: manual custom properties page. Corrected the subtype lists (the manual has no Time (frames/seconds) split and no Translation/Direction/Velocity array subtypes).
- `bpy_struct.id_properties_ui(key)` exists and returns an IDPropertyUIManager: API 5.2.
- Removed as unconfirmed: the `.update(...)`/`.as_dict()` call examples (the manager class page is not in the API docs), the underscore-hidden names claim, the bool-storage version and type-change conversion claims.

Method: documentation only; no commands were run.
