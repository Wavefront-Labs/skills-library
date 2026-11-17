---
id: architecture-construction.interior-design.sketchup.room-modelling-and-furniture-layout-for-client-scenes
name: room-modelling-and-furniture-layout-for-client-scenes
category: architecture-construction
field: interior-design
product: sketchup
tags: [sketchup, sketchup-pro, interior-design, interior-modelling, room-modelling, 3d-modelling, groups, components, tags, outliner, furniture-layout, scenes, space-planning, client-presentation]
level: practitioner
status: docs-checked
description: "Organise a SketchUp interior model with groups, components and tags, lay out furniture options, keep the file light with Purge Unused, and save scenes for client review."
sources:
  - https://help.sketchup.com/en/sketchup/grouping-geometry
  - https://help.sketchup.com/en/sketchup/editing-all-instances-component
  - https://help.sketchup.com/en/sketchup/controlling-visibility-tags
  - https://help.sketchup.com/en/sketchup/creating-scenes
  - https://help.sketchup.com/en/3d-warehouse/purging-unused-entities
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Room modelling and furniture layout for client scenes

**Goal:** a light, well-organised SketchUp model of a room or suite that you can rearrange
in front of a client and turn into clean views.

Check dimensions against the survey yourself: no tool setting here replaces measuring.

## 1. Groups and components
- Grouped geometry is an Object. A group is a selection of several pieces of geometry; a
  component is a more complex, reusable Object.
- Objects can nest (furniture inside a room inside a house) and each can be edited
  independently, even when stacked.
- Lock finished Objects: it gives boundaries for snapping without accidentally modifying
  the geometry.
- Make anything repeated (chairs, lights, doors) a component: editing one instance changes
  all instances of it.

## 2. Tags for visibility
- Tags are the current name for Layers and give the same functionality and more.
- Tags work best on groups and components; new geometry starts untagged.
- Tag visibility helps set up scenes and can make the model run more efficiently.
- Suggested tags: shell, furniture option A, furniture option B, lighting, ceiling, CAD
  underlay. Build layout options on separate tags and toggle them rather than keeping
  separate files.
- Name Objects so the Outliner stays readable.

## 3. Keep the file light
- Imported models carry subcomponents, tags and materials. Purge Unused, in the Statistics
  section of Model Info, is the easiest way to remove unused entities.
- Deleting a component, tag or material by hand does not remove its linked subcomponents,
  tags or materials; check for those separately.

## 4. Scenes for the client
- A scene stores view-related properties. Set the view, styles, fog, shadows, section cuts,
  hidden geometry and tag visibility first, then create the scene.
- In Show Details, Visible Tags saves your tag visibility, Camera Location saves point of
  view, zoom distance and field of view, and Style and Fog saves those settings.
- Update an existing scene with Update Scene (context-click the scene or use the panel
  control); it updates the scene to the current view.
- Name scenes by option and room (for example "Option A living room") so each recalls
  the right set-up.

## Gotchas
- Loose geometry stuck to other geometry: group it.
- Scenes that do not recall tag visibility: check Visible Tags is ticked for the scene.

## Verify
- [ ] Spot-check three dimensions against the survey.
- [ ] Every object is a group or component, named, and tagged.
- [ ] File purged of unused entities.
- [ ] Each scene recalls the right option and camera.

## Checked
2026-11-01. Confirmed on the SketchUp Help pages in sources: group/component definitions,
nesting, locking, component instance editing, tags (rename from layers, best on groups and
components, untagged by default, scenes), Purge Unused location and manual-delete caveat,
what scenes save and Update Scene. Removed as not on those pages: template and units,
DWG import advice, typed-length entry, Push/Pull steps, polygon-count claims, field of view
and eye height figures, section plane height, material texture sizing, renderer names.
Method: documentation only; no commands were run.
