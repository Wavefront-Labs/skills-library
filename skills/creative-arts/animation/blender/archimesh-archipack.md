---
id: creative-arts.animation.blender.archimesh-archipack
name: archimesh-archipack
category: creative-arts
field: animation
product: blender
tags: [blender, archimesh, archipack, archviz-modeling, parametric-architecture, bundled-addons]
level: practitioner
status: gated
description: "Generate architectural elements with the Archimesh add-on: rooms, doors, windows, cabinets, stairs, roofs and shelves, plus how it is installed in current Blender."
sources:
  - https://docs.blender.org/manual/en/4.1/addons/add_mesh/archimesh.html
  - https://extensions.blender.org/add-ons/archimesh/
  - https://github.com/s-leger/archipack
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# archimesh-archipack

Goal: block out interiors quickly with parametric pieces, then refine.

## Archimesh

The Blender 4.1 manual documents Archimesh as a bundled add-on (author Antonio Vazquez, GPL, community support). The extensions.blender.org listing "Archimesh" ("Generate rooms, doors, windows, and other architecture objects") shows a minimum of Blender 4.2, so on current releases install it as an extension. In the 4.1 manual it lives in the 3D Viewport Sidebar, Create tab, and generates:
- Rooms, doors, windows, kitchen cabinets, shelves, columns, stairs, tile roofs, books, lamps, Venetian blinds, roller curtains and Japanese curtains.
- The manual's original videos date from the Blender 2.7 series but it says they are still a valid resource.

Parameter names and panel details were not confirmed against the current extension. (gated: unconfirmed, source is paywalled or blocked)

## Holes in walls

Door and window holes in walls are a common Archimesh workflow, but the 4.1 manual page does not describe it; check the add-on's own panel. (gated: unconfirmed, source is paywalled or blocked)

## Archipack

Archipack is a separate add-on; its current status, licence and features were not checked in this review, so look at its own project page before choosing it. (gated: unconfirmed, source is paywalled or blocked)

## Gotchas

- Set the scene units before creating rooms (practice).
- Edit generated meshes only after you are done adjusting parameters (practice).

## Verify

Dimensions of the generated room match the plan when checked in the Sidebar or with the Measure tool.

## Checked

2026-10-27, Blender manual 4.1 (add-on docs) and extensions.blender.org. Confirmed against the Blender 4.1 manual page add_mesh/archimesh (element list, location, author, licence, video note) and the extensions.blender.org listing for Archimesh (tagline, minimum Blender 4.2), both fetched on this date. Removed unconfirmed parameter details, Auto Holes behaviour and the Archipack history; those are gated.

Method: documentation only; no commands were run.
