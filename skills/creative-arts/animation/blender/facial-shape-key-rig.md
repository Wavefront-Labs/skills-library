---
id: creative-arts.animation.blender.facial-shape-key-rig
name: facial-shape-key-rig
category: creative-arts
field: animation
product: blender
tags: [blender, facial-rig, facial-shape-key-rig, shape-key-face-rig, shape-key-drivers, face-ui-sliders]
level: practitioner
status: docs-checked
description: "Build a shape-key face rig in Blender: FACS/viseme key set, slider bones with limit constraints, driver setup, combination correctives and a face GUI."
sources:
  - https://docs.blender.org/manual/en/latest/animation/shape_keys/introduction.html
  - https://docs.blender.org/manual/en/latest/animation/shape_keys/shape_keys_panel.html
  - https://docs.blender.org/manual/en/latest/animation/drivers/drivers_panel.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/transform/limit_location.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# facial-shape-key-rig

Goal: animator-friendly controls driving a library of facial shape keys.

## 1. Shape key set
Basis + expressions split left/right: `brow_up.L`, `brow_down.L`, `blink.L`, `smile.L`, `frown.L`, `jaw_open`, `pucker`, `funnel`, visemes (`AI`, `E`, `O`, `U`, `MBP`, `FV`). Use FACS-style action units for granularity. Sculpt symmetrical shapes, then split left/right with a vertex group mask (the shape key's Vertex Group field, then Shape Key Specials > New Combined to bake the masked result into a new key), or mirror with Shape Key Specials > New from Objects Flipped (needs matching topology) or Flip (Object Mode, symmetrical vertices).

## 2. Slider controls
- Bones in a face GUI (a board next to the head or on-face): each slider bone has **Limit Location** (local space, with Minimum/Maximum set on the slider axis, for example Y 0 to 0.1 as a practice range, and **Affect Transform** on so the Location values clamp too) and locked other channels.
- 2D joystick bones (X/Y) for mouth corners or eyes.

## 3. Drivers
On each shape key Value: Add Driver, driver type **Scripted Expression** (or the built-in Average/Sum/Min/Max functions); variable of type **Transform Channel** (bone, Y Location, **Local Space**). Expression `var * 10` (0.1 travel -> 1.0). Use the Drivers Editor curve/modifiers to shape the response; the shape key **Range** Min/Max limits the Value.

## 4. Correctives
Combination shapes (`smile + jaw_open` fix) driven by product of inputs: expression `smile * jaw`. Name `smile_jaw_open_corr`.

## 5. Package
Custom properties on a root bone for global intensities; bone collections for GUI; lock unused transforms.

## Gotchas
- Drivers reading World Space break when the head moves; always Local Space.
- Many dependent drivers can slow playback; the manual recommends sticking to the Simple Expressions subset, which Blender evaluates directly (even with Python script execution disabled), and shows a "Slow Python expression" warning for anything else.
- Check each key's **Relative To** field when keys are built on other keys.

## Verify
Move each slider full range: only its shape activates, 0 returns to neutral; combination tests show no double transformation.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release). Confirmed: shape key Specials New Combined, New from Objects Flipped, Flip, plus the Vertex Group, Range and Relative To fields (animation/shape_keys/shape_keys_panel.rst); driver types Average/Sum/Min/Max and Scripted Expression, Transform Channel variables with World/Transform/Local Space, and the Simple Expressions guidance (animation/drivers/drivers_panel.rst); Limit Location has Minimum/Maximum X, Y, Z and Affect Transform (limit_location.rst). Wrong in the old text: the specials item is New Combined (not New Shape from Mix), the checkbox is Affect Transform (not For Transform), there is no Shape Key > Mirror menu, and the driver types are named as above. Slider travel values are practice values.

Method: documentation only; no commands were run.
