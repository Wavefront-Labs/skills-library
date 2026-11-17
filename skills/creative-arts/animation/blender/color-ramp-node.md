---
id: creative-arts.animation.blender.color-ramp-node
name: color-ramp-node
category: creative-arts
field: animation
product: blender
tags: [blender, shader, color-ramp-node, color-ramp, map-range, value-remap]
level: practitioner
status: verified
description: "Remap values in Blender shaders with Color Ramp and Map Range: interpolation modes, constant bands, clamping, stepped/smoothstep and masks."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/color/color_ramp.html
  - https://docs.blender.org/manual/en/5.2/interface/controls/templates/color_ramp.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/utilities/math/map_range.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# color-ramp-node

## Color Ramp

- **Factor** in -> **Color** and **Alpha** out. Add (+) and remove (-) stops, set each stop's Position and Color; Ctrl-LMB click also adds a stop. The tools menu has Flip, Distribute Stops from Left (useful with Constant) and Distribute Stops Evenly.
- **Interpolation** (RGB mode): B-Spline, Cardinal, Linear, Ease, Constant (hard bands for toon shading and masks). Python `ColorRamp.interpolation` ids: EASE, CARDINAL, LINEAR, B_SPLINE, CONSTANT; a new ramp is Linear with stops at 0 (black) and 1 (white). `ramp.evaluate()` at 0, 0.25, 0.5, 0.75, 1 gave: Linear 0, .25, .5, .75, 1; Constant 0, 0, 0, 0, 1; Ease 0, .156, .5, .844, 1; Cardinal 0, .223, .5, .777, 1; B-Spline .167, .318, .5, .682, .833 (it does not reach the end colours).
- **Color Mode**: RGB, HSV or HSL. HSV/HSL keep saturation between hues and offer hue interpolation Clockwise, Counter-Clockwise, Near and Far (Python `color_mode` RGB/HSV/HSL, `hue_interpolation` CW, CCW, NEAR, FAR).
- Mask sharpening: noise -> ramp with the black and white stops close together.

## Map Range

- Inputs Value (or Vector), From Min, From Max, To Min, To Max, and Steps. Data Type Float or Vector. **Clamp** limits output to the target range.
- Interpolation Type: **Linear**, **Stepped Linear** (Steps controls quantisation), **Smooth Step**, **Smoother Step**.
- Use it when ranges should be exact numbers or driven from other sockets, since the From/To values are inputs.
- Rendered with From 0-1 and To 10-20: value 0.3 gave Linear 13, Stepped Linear (Steps 4) 12.5, Smooth Step 12.16, Smoother Step 11.63; value 1.5 gave 20 with Clamp on for every type, and with Clamp off Linear 25 and Stepped Linear 27.5 while Smooth Step and Smoother Step stayed at 20.

## Use cases

- Roughness variation: noise -> Map Range into a narrow roughness range.
- Height masks: Object Z -> Map Range -> Color Ramp for a snow line.
- Toon: Shader to RGB (EEVEE only) -> Color Ramp with Constant interpolation.

## Verify

Plug the ramp output into an Emission shader: bands sit at the intended stop positions.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against color/color_ramp, the Color Ramp widget page and utilities/math/map_range: interpolation and colour modes, hue directions, tools, Ctrl-LMB, Map Range inputs, data types, Clamp, interpolation types and Steps. Removed the Node Wrangler shortcut, the luminance-conversion remark, the claim about socket-driven stops and the numeric ranges.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Color Ramp node sockets (Fac in; Color, Alpha out) and enums; ramp evaluation; Map Range sockets (Value, From Min, From Max, To Min, To Max, Steps, plus Vector variants), Data Type FLOAT/FLOAT_VECTOR, Interpolation Type LINEAR/STEPPED/SMOOTHSTEP/SMOOTHERSTEP, Clamp, evaluated by rendering the result as emission. Unrun (documentation only): the + / - / Ctrl-LMB stop editing, tools menu items, Shader to RGB being EEVEE only, the use-case recipes.

Method: manual text confirmed from documentation; node behaviour run headless in Blender 4.5.14.
