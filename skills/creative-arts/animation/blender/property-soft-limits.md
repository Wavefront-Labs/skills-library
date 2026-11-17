---
id: creative-arts.animation.blender.property-soft-limits
name: property-soft-limits
category: creative-arts
field: animation
product: blender
tags: [blender, property-soft-limits, soft-min, soft-max, property-step, custom-properties, rig-ui]
level: intro
status: docs-checked
description: "Set custom property limits that feel right: hard min and max versus soft min and max for slider range, step and precision, and setting them from Python."
sources:
  - https://docs.blender.org/manual/en/latest/files/custom_properties.html
  - https://docs.blender.org/api/current/bpy.props.html#bpy.props.FloatProperty
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# property-soft-limits

Goal: sliders that drag through a sensible range while still allowing extreme typed values when needed.

## The four limits

- **Min / Max** (hard): typed values are clamped to these. Use for physically impossible values (negative scale factors, influence > 1).
- **Soft Min / Soft Max**: the limits the slider can be adjusted to without typing the value numerically; typed values can go beyond them (up to the hard limits).
- **Step**: a multiplier for how much the value changes at a time; the internal float step size is 0.01, so Step 5 changes it by 0.05 and Step 100 by 1.0 (integers use a step of 1).
- **Precision**: the number of digits shown after the decimal point for floats.

Example rig control "Smile": Min -1, Max 2, Soft Min 0, Soft Max 1: animators drag 0-1 normally and can type 1.3 for an extreme pose.

## Edit them

Gear icon (*Edit Property*) next to the property; enable *Soft Limits* to set Soft Min and Max. From Python, `pbone.id_properties_ui("smile")` returns the object that manages the property's UI data; its methods are not documented on the API pages, so check it in the Python console.

## Registered properties

```python
bpy.props.FloatProperty(name="Smile", min=-1, max=2, soft_min=0, soft_max=1, step=1, precision=3)
```

## Gotchas

- Changing limits does not edit existing keyframes; Bezier overshoot can push animated values past soft limits, so clamp in drivers when the range matters (practice).

## Verify

Drag the slider: it stops at the soft limits; type a value beyond soft but inside hard: accepted; type beyond hard: clamped.

## Checked

Blender 5.2 manual (files/custom_properties) and Python API 5.2, read 2026-10-27.
- Soft Limits, Soft Min/Max, Step (internal 0.01 for floats, Step 5 = 0.05, integers 1) and Precision descriptions: manual custom properties page.
- `bpy.props.FloatProperty(min, max, soft_min, soft_max, step=3, precision=2, ...)` signature: API 5.2.
- Removed as unconfirmed: the `.update(...)` example on the UI manager, the integer-precision and library-override claims.

Method: documentation only; no commands were run.
