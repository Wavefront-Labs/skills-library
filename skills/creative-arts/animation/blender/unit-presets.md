---
id: creative-arts.animation.blender.unit-presets
name: unit-presets
category: creative-arts
field: animation
product: blender
tags: [blender, scene-units, unit-presets, imperial-units, metric-units, unit-scale, separate-units]
level: practitioner
status: docs-checked
description: "Set Blender scene units correctly: Metric/Imperial/None, Unit Scale, length/mass/time/temperature units, Separate Units, and what unit scale does to physics, export and grid."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html
  - https://docs.blender.org/manual/en/latest/interface/controls/buttons/fields.html
  - https://docs.blender.org/manual/en/latest/files/import_export/stl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# unit-presets

Goal: dimensions that read in the units the client uses, without breaking simulation scale or exports.

## Scene Properties > Units

- **Unit System**: *None* (plain BU), *Metric*, *Imperial*.
- **Unit Scale**: scale factor between internal Blender units and the values shown in the interface (1.0 with Metric = 1 BU is 1 m). The manual says it only influences displayed values, not how things behave internally: physics simulations do not take the unit scale into account. Change it for display needs, or for microscopic or astronomical work where a small or large scale avoids precision problems.
- **Separate Units**: show `1 m 25 cm` / `5' 3"` instead of decimals.
- **Rotation**: Degrees / Radians.
- **Length**: Adaptive (unit chosen by the value's magnitude) or a fixed unit; the manual's tables list metric units from micrometer to kilometer and imperial thou, inch, foot, yard, chain, furlong and mile. **Mass**, **Time** and **Temperature** work the same way.

## Presets that work

| Use | System | Scale | Length |
|---|---|---|---|
| Film/archviz/game (default) | Metric | 1.0 | Meters or Centimeters |
| 3D printing | Metric | 0.001 | Millimeters |
| US architecture | Imperial | 1.0 | Feet / Inches, Separate Units on |

Save as defaults (*File > Defaults > Save Startup File*, which makes the current file the default startup file) once decided. The table rows are practice conventions, not manual recommendations.

## Typing values

Number fields store values and units and accept mathematical expressions, which Blender evaluates with Python: for example `25cm` or `2ft + 3in`. Short names such as `cm`, `mm`, `ft`, `in` and `mi` come from the manual's unit tables.

## Gotchas

- Physics simulations do not take the unit scale into account, so model objects at a sensible size in Blender units rather than relying on Unit Scale to fix their size (practice).
- Exporters: the FBX exporter has **Apply Unit** (on by default) and **Apply Scalings** options; the STL importer and exporter have a **Scene Unit** option that applies the scene's unit (as defined by unit scale); check each exporter's own documentation for how it treats units. A non-1.0 unit scale is a common cause of 100× or 1000× size errors (practice).

## Verify

Add a default cube (2 Blender units): N panel *Dimensions* reads 2 m with Unit Scale 1.0, or 2 mm with Unit Scale 0.001 and Length set to Millimeters.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release), with rna_scene.cc (UnitSettings, scale_length range 1e-9 to 1e9) and wm_files.cc (operator name Save Startup File). Confirmed: Unit System None/Metric/Imperial, Unit Scale display-only with physics ignoring it, Separate Units, Rotation, Length/Mass/Time/Temperature and the unit tables (scene_layout/scene/properties.rst); number fields store units and evaluate Python expressions (interface/controls/buttons/fields.rst); the STL Scene Unit option (files/import_export/stl.rst); FBX Apply Unit and Apply Scalings (add-on source). Wrong in the old text: simulations do not compute in BU x scale (the manual says unit scale is ignored by physics), and the verify step claimed a default cube reads 2000 mm at Unit Scale 0.001, but it reads 2 mm. Removed unconfirmed claims about glTF and the grid.

Method: documentation only; no commands were run.
