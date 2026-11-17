---
id: creative-arts.animation.blender.light-linking-collections
name: light-linking-collections
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, light-linking, light-linking-collections, receiver-collection, light-linking-exclude]
level: practitioner
status: docs-checked
description: "Use light linking in Cycles and EEVEE: receiver collections on lights and emitters, include and exclude states, and typical uses like isolated rim lights."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_linking.html
  - https://docs.blender.org/manual/en/latest/render/eevee/object_settings/object_data.html
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# light-linking-collections

## Concept

A light (or emissive mesh) gets a **Receiver Collection**. Entries are set to Include or Exclude:
- Only Include entries: the light affects only those objects.
- Only Exclude entries: the light affects every object except those.
- Both: the light affects only the included objects minus the excluded ones (for example include a character collection, then exclude one object of it).

Light linking is documented for Cycles and EEVEE; emissive mesh objects only support it with Cycles, and Grease Pencil objects do not support it at all.

## Setup

1. Select the light or emissive mesh: Object Properties > Shading > **Light Linking** (Cycles or EEVEE Shading panel) > Receiver Collection > New.
2. Drag objects or collections from the Outliner onto the list.
3. Set each entry to Include or Exclude.

Alternative: select the objects, add the light to the selection, press Ctrl-L (Link/Transfer Data menu) and choose *Link Receivers/Blockers to Emitter*.

## Uses

- Rim light on the character only, not the set.
- Eye catchlight light that only affects the eyes.
- Removing a practical's light on one object.

## Tips

- Several lights can use the same linking collection. They can also use an existing scene collection, but dedicated linking collections are recommended so changes do not affect the scene layout.
- Sampling for light linking is most efficient with the Cycles light tree enabled.

## Gotchas

- Overuse makes lighting non-physical and hard to debug; name collections clearly (`LL_key_char`).

## Verify

Render with/without the receiver collection: only the intended objects change in lighting from that light.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Setup steps, Ctrl-L Link Receivers/Blockers to Emitter, Include/Exclude rules, emissive-mesh Cycles-only and Grease Pencil limits, reuse of collections, light tree performance note (Light Linking page); Receiver Collection in EEVEE and Cycles Shading panels (object settings pages). Removed unsupported claims (version gate, nesting, light-group interplay, indirect-light behaviour).

Method: documentation only; no commands were run.
