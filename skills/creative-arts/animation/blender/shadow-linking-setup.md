---
id: creative-arts.animation.blender.shadow-linking-setup
name: shadow-linking-setup
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, shadow-linking, shadow-linking-setup, blocker-collection, light-linking]
level: practitioner
status: docs-checked
description: "Use shadow linking: blocker collections on lights to choose which objects cast shadows from a given light, with include and exclude states."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_linking.html
  - https://docs.blender.org/manual/en/latest/render/eevee/object_settings/object_data.html
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# shadow-linking-setup

## Concept

Shadow linking gives control over which objects block the light (cast shadows) from a given light or emitter. Each emitter can have a **Shadow Blocker Collection**. Blockers can be set to Include or Exclude like light receivers: only included objects cast shadows from that light; excluded objects stop blocking it; with both, the light is blocked only by the included objects minus the excluded ones.

Example from the manual: a rim light that only illuminates a character (light linking) and is not blocked by any objects in the scene (shadow linking).

## Setup

Select the light or emissive mesh: Object Properties > Shading > **Shadow Linking** (Cycles or EEVEE Shading panel) > Shadow Blocker Collection > New. Drag objects or collections from the Outliner onto the list and set Include or Exclude. Alternative: select the objects, add the light, press Ctrl-L and choose *Link Receivers/Blockers to Emitter*.

## Uses

- Character's hair casting ugly shadows from the key onto the face: exclude hair from blocking the key only.
- Set pieces blocking a hero rim light: exclude the set.

## Difference from ray visibility

Object Visibility > Ray Visibility > Shadow off stops the object casting shadows (from every light); shadow linking is per light.

## Gotchas

- With shadow linking renders can be slower and trace additional rays, because direct and indirect lighting take different paths.
- Easy to create physically impossible looks that lighting leads will not expect - document it in the scene notes.

## Verify

Toggle the exclude: the shadow from that object vanishes only for that light; shadows from other lights remain.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Shadow Blocker Collection panel entries, Include/Exclude rules, Ctrl-L Link Receivers/Blockers to Emitter, rim-light example and shadow-linking performance note (Light Linking page and EEVEE object settings page); Shadow ray visibility meaning (object settings pages). Removed unsupported claim about indirect shadows and the lamp shade example.

Method: documentation only; no commands were run.
