---
id: creative-arts.animation.blender.light-group-passes
name: light-group-passes
category: creative-arts
field: animation
product: blender
tags: [blender, render-passes, light-group-passes, lightgroup-pass, light-groups, relighting]
level: practitioner
status: docs-checked
description: "Set up Cycles light groups: assign lights, emissive objects and world to groups, render one pass per group, and relight in the compositor by recombining them."
sources:
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html#light-groups
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# light-group-passes

Goal: adjust the brightness and colour of each light (or group of lights) after rendering.

## Setup (Cycles only)

1. View Layer Properties > Passes > **Light Groups**: + to add groups (`key`, `fill`, `rim`, `practicals`, `sky`).
2. For each light or emissive object: Object Properties > Shading > **Light Group**: pick the group name.
3. World: World Properties > Settings > Light Group.
4. Or use **Add Used Lightgroups** (downward arrow next to the list) to create groups for names already assigned but not yet existing.

Each Light Group gives a limited *Combined* render pass lit only by that group's lights.

## Relight in the compositor

Multiply each group pass by a colour/intensity, then Add them together (Mix Color node):
```
key x 1.2 + fill x 0.6 (blue tint) + rim + practicals x 2 + sky
```
Build it as a node group with one input per group.

## Gotchas

- To reproduce the full render, every light, emissive object and the world must belong to a group; anything left out is missing from the sum. Use an `other` group if needed.
- Light groups are Cycles only; the manual marks the feature "Cycles only".

## Verify

Add all light group passes and compare with Combined; the difference should be noise only.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Light Groups behaviour, Cycles-only note, assignment locations, Add Used Lightgroups and Mix Color recombination (Render passes, Cycles object and Cycles world pages); panel location (ui.py). Removed unsupported claims (3.2 version gate, pass naming, denoising behaviour, memory and EEVEE statements).

Method: documentation only; no commands were run.
