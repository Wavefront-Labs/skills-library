---
id: creative-arts.animation.blender.color-spill
name: color-spill
category: creative-arts
field: animation
product: blender
tags: [blender, keying, color-spill, spill-suppression, despill, green-screen]
level: practitioner
status: docs-checked
description: "Remove green or blue screen spill with the Color Spill node: Spill Channel, Limit Method (Simple, Average), Limit Strength, Spill Strength, and Keying node despill."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/color_spill.html
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/keying.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# color-spill

Goal: remove the screen's colour bleeding onto the subject (edges, hair, shiny surfaces) without making skin grey or purple.

## Node (Keying category > Color Spill)

- **Image** and **Factor** (1.0 fully applies the effect, lower values blend with the original).
- **Spill Channel**: R, G (common for green screens) or B (common for blue screens).
- **Limit Method**: **Simple** compares the **Limit Channel** (R, G or B) with the others and reduces the spill channel if it is higher; **Average** uses the average of the other two channels as the limit.
- **Limit Strength**: limiting strength of the limit channel.
- **Spill Strength** (panel): when enabled, a **Strength** per colour channel can be set; when disabled the spill channel has unit scale and the others are zero.
- Output: **Image** with the corrected channels.

The Keying node has its own Despill panel (**Strength** and **Balance**); the manual says its Strength uses the same implementation as the Color Spill node's unspill amount, and its Balance is similar to the Limit Channel.

## Placement

Despill after keying and before layering over the new background (Alpha Over). Take the matte from the key and the colour from the despilled image, applying the matte with a Set Alpha node or Mix.

## Tips

- If light from the screen should be replaced by the new background's colour, add a little of the background colour back where spill was removed.
- Hair and blonde subjects show spill most. Check closely.

## Gotchas

- Despilling green-heavy costumes or plants removes their colour too. Mask them out of the despill.
- The Keying node's own despill may be enough. Do not stack both at full strength.

## Verify

Sample skin and hair pixel values before and after. Green should no longer exceed the other channels in neutral areas, and skin should keep a natural tone over the new background.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Color Spill inputs and settings (Factor, Spill Channel, Limit Method Simple/Average, Limit Channel, Limit Strength, Spill Strength panel) and the Keying node Despill Strength and Balance equivalence. Removed the Ratio and Unspill slider names, which 5.2 renames, and the Fac input name.
Method: documentation only; no commands were run.
