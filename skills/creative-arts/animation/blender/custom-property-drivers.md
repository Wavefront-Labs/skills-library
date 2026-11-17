---
id: creative-arts.animation.blender.custom-property-drivers
name: custom-property-drivers
category: creative-arts
field: animation
product: blender
tags: [blender, custom-property-drivers, property-driven, driven-custom-property, drivers, rig-ui, custom-properties]
level: practitioner
status: docs-checked
description: "Drive rig and modifier values from custom properties: Copy as New Driver, Single Property variables with bracket paths, pose bone properties, and expressions with ranges."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/drivers/usage.html
  - https://docs.blender.org/manual/en/5.2/animation/drivers/drivers_panel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# custom-property-drivers

Goal: one animator-facing slider controls many internal values (shape keys, constraint influences, modifier toggles).

## Fast way: Copy As New Driver

1. Right-click the custom property (for example on the control bone's Custom Properties) and choose **Copy As New Driver**.
2. Right-click the target property (shape key value, constraint influence, modifier setting) and choose **Paste Driver**. To add the variable to an existing driver instead, use **Paste Driver Variables** in the driver panel.

## Manual setup

Target property, right-click, *Add Driver* (or Ctrl-D over the property); the Edit Driver popover opens with one variable to fill in.
- Variable type *Single Property*; ID Type and ID pick the data-block that holds the property (for example the armature object).
- RNA Path: `["prop_name"]` for a custom property on the chosen ID; for a custom property on a bone use the path that Copy As New Driver produces.
- Driver Type: Average, Sum, Min, Max, or Scripted Expression. Simple expressions use the variable names and the operators and functions Blender supports natively: arithmetic, comparisons, `min`, `max`, `abs`, `clamp`, `lerp`, `smoothstep` and others. Examples: `var`, `var * 0.5`, `max(0, var)`, `1 - var`, `var > 0.5`.

## IK/FK and visibility switches

Drive constraint influences with the property and its inverse (`1 - var`). A visibility toggle can be driven with `var > 0.5`.

## Gotchas

- Expressions outside the simple subset run as Python and show a "Slow Python expression" warning; a few are fine, but keep most drivers simple. Simple expressions are evaluated even when Python script execution is disabled.
- Access object data through driver variables rather than direct references, so dependencies are tracked; the `self` option may not track dependencies fully.

## Verify

Drivers editor shows no invalid drivers; dragging the slider moves every driven value; no "Slow Python expression" warning appears.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Drivers Usage and Drivers panel pages: Add Driver and Ctrl-D, Copy As New Driver with Paste Driver and Paste Driver Variables, driver types, RNA path for custom properties, the simple expression subset, the Slow Python expression warning, self dependency note. Removed unconfirmed claims about renamed paths, Library Overridable, Auto Run Python Scripts and dependency cycles, and unverifiable property names.

Method: documentation only; no commands were run.
