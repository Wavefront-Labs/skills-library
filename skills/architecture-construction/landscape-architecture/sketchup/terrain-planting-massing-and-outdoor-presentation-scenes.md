---
id: architecture-construction.landscape-architecture.sketchup.terrain-planting-massing-and-outdoor-presentation-scenes
name: terrain-planting-massing-and-outdoor-presentation-scenes
category: architecture-construction
field: landscape-architecture
product: sketchup
tags: [sketchup, sketchup-pro, landscape-architecture, terrain, terrain-modelling, sandbox-tools, from-contours, from-scratch, smoove, geo-location, shadows, sun-study, planting-massing, tree-components, scenes, concept-design]
level: practitioner
status: docs-checked
description: "Build concept landscape terrain in SketchUp from contours or from scratch, reshape it with Smoove, run geolocated shadow studies and save presentation scenes."
sources:
  - https://help.sketchup.com/en/sketchup/creating-terrain-scratch
  - https://help.sketchup.com/en/sketchup/sculpting-and-fine-tuning-terrain
  - https://help.sketchup.com/en/sketchup/casting-real-world-shadows
  - https://help.sketchup.com/en/sketchup/creating-scenes
  - https://help.sketchup.com/en/sketchup/controlling-visibility-tags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terrain, planting massing and outdoor presentation scenes in SketchUp

**Goal:** a concept-stage landscape model that shows levels, spaces and planting structure
well enough to make decisions, and stays light enough to orbit live with a client.

## 1. Terrain
- The Sandbox tools are available as a toolbar you add in View > Toolbars.
- **From Contours:** select your contour lines and SketchUp generates a TIN from them. The
  TIN is a group and can be edited like any other grouped geometry. Put contours at their
  real elevations first: contours left flat give a flat TIN with no levels.
- **From Scratch:** after you set length and width, a flat rectangular TIN (a grouped
  entity) appears in the model.
- Keep existing terrain separate from proposed terrain (copy the group) and lock the
  existing one.

## 2. Shaping
- **Smoove** smooths and moves; it is for creating or editing hills and valleys. Negative
  values in the Measurements box create a depression, positive values raise the area.
- Treat Sandbox shaping as concept only. Design levels belong in the grading plan; see
  `architecture-construction.landscape-architecture.grading-drainage-design.contour-grading-spot-elevations-and-surface-drainage`.
  Label concept terrain so nobody mistakes it for engineered levels.

## 3. Planting massing
- Model trees as components sized to height and spread at a stated age: this is design
  information, not decoration. Keep them simple so the file orbits smoothly.
- Hedges, shrub masses and meadows as simple volumes with a material communicate structure
  better than thousands of individual plants.
- Use tags (best applied to groups and components) to separate existing trees, proposed
  trees, shrub masses, existing terrain, proposed terrain and hardscape.

## 4. Shadows and sun
- SketchUp bases shadows on the model's location coordinates, north orientation and time
  zone, and you must geolocate the model before using Shadows.
- Choose the time and date in the Shadows panel (sliders and dropdowns). Step through key
  dates and times and save each as a scene for a shadow-study board.

## 5. Scenes
- A scene stores view-related properties: the view, styles, fog, shadows, section cuts,
  hidden geometry and tag visibility. Use Update Scene after changing any of them.
- Add eye-level views in key spaces, an aerial overview and section cuts through level
  changes.

## Verify
- [ ] Contours at correct elevations; TIN checked for odd spikes by eye.
- [ ] Proposed terrain separate from existing; existing locked.
- [ ] Trees sized to a stated age, counted and tagged.
- [ ] Geolocation, north and time zone checked before trusting shadows.
- [ ] Scenes recall correctly; file orbits smoothly.

## Checked
2026-11-01. Confirmed on the SketchUp Help pages in sources: Sandbox toolbar location, From
Contours and From Scratch results, Smoove behaviour, shadow prerequisites and controls,
scene contents and Update Scene, tag behaviour. Removed as not confirmed: Stamp and Drape
details, Add Location imagery terrain, contour import advice, plugins, face-me trees,
renderer names, eye height and tree-age figures.
Method: documentation only; no commands were run.
