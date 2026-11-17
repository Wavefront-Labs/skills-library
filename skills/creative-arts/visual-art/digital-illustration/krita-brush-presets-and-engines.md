---
id: creative-arts.visual-art.digital-illustration.krita-brush-presets-and-engines
name: krita-brush-presets-and-engines
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, krita, digital-brushes, brush-engine, krita-brushes, brush-presets, pixel-brush, color-smudge, bundles, brush-tips, sensors]
level: practitioner
status: docs-checked
description: "Use and organise Krita brush presets: brush engines, the brush settings sections, tagging presets, and importing and exporting resource bundles."
sources: ["https://docs.krita.org/en/reference_manual/brushes/brush_engines.html", "https://docs.krita.org/en/reference_manual/brushes/brush_settings.html", "https://docs.krita.org/en/reference_manual/resource_management.html", "https://docs.krita.org/en/reference_manual/dockers/brush_preset_docker.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Krita brush presets and engines

In Krita a **brush preset** is a brush engine plus its settings. The engine decides what kind of mark is made, and the
Brush Editor exposes the engine's settings.

## Brush engines (as listed in the Krita manual)
Bristle, Chalk, Clone, Color Smudge, Curve, Deform, Dyna, Filter, Grid, Hatching, MyPaint, Particle, Pixel, Quick,
Shape, Sketch, Spray, Tangent Normal. Open the manual page for an engine to read its options before building
presets on it; engines differ in which settings they offer.

## Brush settings sections shared across engines
The manual groups the overall settings into: Brush Tips, Locked Brush Settings, Masked Brush, Opacity and Flow,
Options, Sensors and Texture. Sensors drive an option (such as opacity or size) from input, and each has an
editable curve; test the pressure curve on a scratch canvas with your tablet.

## Organising presets
- In the Brush Presets docker, right-click a brush to add or remove a tag.
- Resources can belong to one or more tags. Bundles can include tags.
- Share presets as a **bundle**: Settings > Manage Resources, then the Create bundle button, which walks you
  through choosing resources, tags, details and a save location. Import a `.bundle` with the Import button at the
  top right of the same dialog. Deleting an imported bundle's file means it will not load on the next start.
- Krita keeps tags, names, versions and other resource data in a SQLite cache; deleting that cache removes the
  tags and relationships it tracks.

## Gotchas
- The bundle creator was overhauled in Krita 5.3, so the dialog may differ from older guides.
- Back up custom brushes as a bundle before reinstalling or clearing the resource cache.

## Verify
- [ ] Preset saved with a name and tag.
- [ ] Pressure curve tested on a scratch canvas.
- [ ] Custom brushes backed up as a bundle.

## Checked

2026-11-01. Confirmed in the Krita manual: the engine list (brush_engines), the settings sections (brush_settings),
Settings > Manage Resources, Create bundle, Import button, `.bundle`, tags, SQLite cache, the 5.3 bundle-creator
change (resource_management), and right-click tagging (brush_preset_docker). Removed because the pages fetched did
not state them: per-engine descriptions, Pixel as default, the F5 shortcut, spacing values, the list of sensor
names, texture mode and masked-brush detail, Overwrite / Save New Brush Preset behaviour, favourites, reload
button, "no restart needed" and the performance remarks.
Method: documentation only; no commands were run.
