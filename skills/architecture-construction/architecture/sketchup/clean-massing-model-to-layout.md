---
id: architecture-construction.architecture.sketchup.clean-massing-model-to-layout
name: clean-massing-model-to-layout
category: architecture-construction
field: architecture
product: sketchup
tags: [sketchup, sketchup-pro, layout, trimble, massing, concept-model, groups, components, tags, outliner, scenes, styles, back-faces, solid-tools, geo-location, shadows, purge-unused, presentation-drawings, cleanup]
level: practitioner
status: docs-checked
description: "Build a SketchUp massing model that stays editable: group and component discipline, tags, correct face orientation, solids, scenes, purging, then Send to LayOut."
sources:
  - https://help.sketchup.com/en/sketchup/grouping-geometry
  - https://help.sketchup.com/en/sketchup/controlling-visibility-tags
  - https://help.sketchup.com/en/3d-warehouse/orienting-faces
  - https://help.sketchup.com/en/sketchup/modeling-complex-3d-shapes-solid-tools
  - https://help.sketchup.com/en/sketchup/creating-scenes
  - https://help.sketchup.com/en/sketchup/casting-real-world-shadows
  - https://help.sketchup.com/en/sketchup/sending-sketchup-model-layout
  - https://help.sketchup.com/en/3d-warehouse/purging-unused-entities
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A clean SketchUp massing model, through to LayOut

**Goal:** a concept model you can change quickly in a design meeting, kept organised so it
produces consistent views for LayOut.

## 1. Group and component discipline
- Make each distinct object (floor plate, core, massing block) a group or component as
  soon as it exists. Objects nest and can be edited independently, even when stacked.
- Use components for anything repeated: editing one instance changes all instances.
- Lock finished Objects for snapping boundaries without accidental edits.

## 2. Tags
- Tags are the current name for Layers. They work best on groups and components; new
  geometry starts untagged.
- Tag visibility helps scene set-up and model performance. Keep a short, sensible list
  (site, existing, massing, glazing, entourage, annotation).

## 3. Face orientation and solids
- Faces have a white front and a blue back colour. Orient faces so the front colour faces
  outward; mixed orientation can leave colour gaps and cause problems in rendering software.
- Adjacent faces: select them and choose Orient Faces from the context menu. Non-adjacent
  faces: select each and choose Reverse Faces.
- A SketchUp solid has a finite enclosed volume with no missing faces and no faces that do
  not meet at an edge. Entity Info can tell you whether a selection is a solid. Subtract,
  Trim and Intersect need overlapping solids.
- SketchUp for Web has a built-in Solid Inspector; on desktop it is found in Extension
  Warehouse.

## 4. Geolocation and shadows
You must geolocate the model before using Shadows. Shadows depend on the model's location
coordinates, north orientation and time zone; set date and time in the Shadows panel.

## 5. Scenes
A scene stores the view, styles, fog, shadows, section cuts, hidden geometry and tag
visibility. Set those first, create the scene, and use Update Scene when they change.

## 6. Clean-up and LayOut
- Purge Unused (Model Info, Statistics section) removes unused entities. Deleting a
  component, tag or material by hand does not remove its linked subcomponents, tags or
  materials.
- Send to LayOut is on the Getting Started toolbar, the Large Tool Set and the File menu.
  SketchUp asks you to save first; LayOut asks which document type to create and places a
  viewport containing the model. For scale and updating linked models, read the LayOut
  help pages on perspective and scale and on managing changes to SketchUp files.

## Verify
- [ ] Every object is a named group or component; tags applied to containers.
- [ ] Faces oriented front colour outward; solids confirmed in Entity Info where needed.
- [ ] Model geolocated before shadow studies.
- [ ] Scenes recall the intended view and tags.

## Checked
2026-11-01. Confirmed on the SketchUp Help pages in sources: groups, components, locking,
tags, face colours and Orient/Reverse Faces, solid definition and Solid Inspector location,
geolocation before shadows, scene contents, Purge Unused, Send to LayOut. Removed as not
stated on those pages: units and precision advice, the sub-millimetre scaling workaround,
Monochrome style tip, Section Fill, "Solid Group" label, Pro-only claim, LayOut scale,
render modes, Update Model Reference steps, extensions advice, DWG-import advice.
Method: documentation only; no commands were run.
