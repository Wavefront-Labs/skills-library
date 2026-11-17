---
id: creative-arts.animation.blender.light-groups
name: light-groups
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, light-groups, lightgroups, render-passes, compositing]
level: practitioner
status: docs-checked
description: "Relight Cycles renders in comp with Light Groups: create groups in the view layer, assign lights, emissive objects and world, and rebalance passes."
sources:
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html#light-groups
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
  - https://docs.blender.org/manual/en/latest/render/cycles/world_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# light-groups

## Create

View Layer Properties > Passes > **Light Groups** (Cycles only): + to add groups (`key`, `fill`, `rim`, `env`). Each Light Group provides a limited *Combined* render pass in which the scene is lit only by the lights of that group.

## Assign

- Light or emissive object: Object Properties > Shading > **Light Group** field.
- World: World Properties > Settings > **Light Group** field.
- Typing a name that does not exist and pressing the add button next to the field creates the group and assigns the object or world to it.
- From the downward arrow next to the Light Group list: *Add Used Lightgroups* (creates groups for lights that reference a non-existing one) and *Remove Unused Lightgroups*.

## Compositing

Add the passes together with a Mix Color node to rebuild the full render; by making more complex combinations you can change the colour and intensity of individual lights without re-rendering. To reproduce the full render, every light, emissive object and the world must belong to a group.

## Use

Rebalance key/fill ratio, recolour a practical, animate a light flicker in comp without re-rendering.

## Gotchas

- Cycles only.

## Verify

Add all light group passes in comp: the difference with the Combined pass is about zero (check with a Difference mix).

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Light Groups definition, Cycles-only note, assignment from Object > Shading and World > Settings, Add/Remove Used Lightgroups and Add-based recombination (Render passes, Cycles object and Cycles world pages); panel location under View Layer > Passes (ui.py). Removed unsupported claims (pass naming, denoising advice, memory growth).

Method: documentation only; no commands were run.
