---
id: creative-arts.animation.blender.comp-color-balance
name: comp-color-balance
category: creative-arts
field: animation
product: blender
tags: [blender, color-grade, color-balance-node, lift-gamma-gain, offset-power-slope, asc-cdl]
level: practitioner
status: docs-checked
description: "Grade with the compositor Color Balance node: lift/gamma/gain vs offset/power/slope (ASC CDL), working in linear, masks via factor, and matching a CDL from set or editorial."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/color/adjust/color_balance.html
  - https://docs.blender.org/manual/en/latest/compositing/types/color/adjust/hue_saturation.html
  - https://docs.blender.org/manual/en/latest/compositing/types/color/alpha_convert.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# comp-color-balance

Goal: primary colour grading in Blender's compositor.

## Node (Color > Adjust > Color Balance)

Inputs: **Image**, **Factor** (amount of influence), **Type**.
- **Lift/Gamma/Gain**: Lift adjusts the darkest areas, Gamma mainly the midtones, Gain the brightest parts.
- **Offset/Power/Slope (ASC-CDL)**: a standardised model so the same values give the same result across applications. Offset adjusts the shadows (an extra **Basis** value allows a negative offset), Power mainly the midtones, Slope the highlights. Formula in the manual: out = (i x s + o)^p, with Slope 0 or greater (nominal 1), Offset any number (nominal 0) and Power greater than 0 (nominal 1).
- **White Point**: sets what should be considered white, given as an input colour **Temperature** and **Tint** and an output Temperature and Tint. Defaults are a D65 white point; a Tint of 10 matches daylight.

**Factor**: connect a matte (for example a mask) to grade only an area.

## Workflow

1. Balance first: neutralise grey with the white point or the gain/slope colour opposite the cast.
2. Set contrast: slope or gain for highlights, lift or offset for blacks.
3. Creative look: midtone (gamma or power) tint.
4. Secondary grades through mattes after the primary.

## CDL exchange

A CDL from set or editorial gives Slope (RGB), Offset (RGB), Power (RGB) and Saturation. Enter the first three in Offset/Power/Slope mode and handle saturation with a Hue/Saturation/Value node after it. Apply it in the colour space it was made for, which may not be scene-linear; confirm with whoever supplied it.

## Gotchas

- Grading premultiplied images changes edges. Convert to straight with Alpha Convert first (see comp-alpha-over) and back afterwards.
- Strong lift or negative offset on scene-linear data can produce negative values that behave badly after the view transform.

## Verify

Sample a grey reference before and after the balance step. RGB values should be about equal. Compare the graded frame with the reference frame side by side in the Image Editor.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Color Balance Type options, Lift/Gamma/Gain and Offset/Power/Slope controls, Basis, White Point temperature and tint with D65 defaults, and the ASC-CDL formula. Removed the claim that lift behaves strongly on scene-linear data and the Wikipedia source.
Method: documentation only; no commands were run.
