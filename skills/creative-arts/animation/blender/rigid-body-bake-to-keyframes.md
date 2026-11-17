---
id: creative-arts.animation.blender.rigid-body-bake-to-keyframes
name: rigid-body-bake-to-keyframes
category: creative-arts
field: animation
product: blender
tags: [blender, rigid-body, bake-to-keyframes, rigid-body-bake, physics-baking, game-export, art-direction]
level: practitioner
status: docs-checked
description: "Turn a Blender rigid body sim into editable keyframes: cache bake vs Bake to Keyframes, cleaning keys, art-directing pieces afterwards and exporting to engines."
sources:
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/world.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/tips.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# rigid-body-bake-to-keyframes

## Cache bake vs keyframes

- **Cache bake** (Scene > Rigid Body World > Cache): **Bake** calculates the sim and protects the cache (Object Mode required); **Delete Bake** clears it. **Start / End** set the simulated frame range. Save the file first: without a saved file the cache is in memory and may be lost.
- **Bake To Keyframes** (Object > Rigid Body menu): converts rigid body dynamics to normal keyframes.

## Workflow

1. Tune and cache-bake the sim; review.
2. Select the pieces and use Object > Rigid Body > Bake To Keyframes; review the dialog options in your Blender version.
3. Optionally thin the keys in the Graph Editor (see `fcurve-decimate-smooth`) to make them editable.
4. Art-direct: adjust a hero piece's keys or shift its timing in the Dope Sheet.
5. Export: formats that carry transform animation (FBX, glTF, Alembic) then carry the motion rather than a sim an engine cannot read.

## Variants

- Mixed: hero pieces keyed, background pieces left in the cache.

## Gotchas

- Keep a backup collection of the original rigid bodies if you may want to re-simulate.

## Verify

Disable the Rigid Body World: baked objects still animate identically; keyed pieces play in the target app.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Rigid Body World Cache fields (Start/End, Bake, Delete Bake, memory-cache warning) and that Bake To Keyframes lives in the Object > Rigid Body menu. Removed the Start/End/Step option list for the operator, the claims about what happens to objects in the sim and the "Alembic is better for many pieces" claim, because the manual does not document them.
Method: documentation only; no commands were run.
