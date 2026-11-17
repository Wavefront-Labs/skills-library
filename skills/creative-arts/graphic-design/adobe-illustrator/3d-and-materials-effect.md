---
id: creative-arts.graphic-design.adobe-illustrator.3d-and-materials-effect
name: 3d-and-materials-effect
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-3d-materials, 3d-and-materials, extrude, revolve, inflate, ray-tracing, substance-materials, map-artwork, illustrator-effects]
level: practitioner
status: draft
description: "Use Illustrator's 3D and Materials panel: extrude, revolve and inflate, map artwork onto surfaces, add Substance materials and lighting, and render or expand for output."
sources:
  - https://helpx.adobe.com/illustrator/using/create-3d-objects.html
  - https://helpx.adobe.com/illustrator/using/3d-effects-panel.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 3D and Materials effect

**Goal:** quick 3D objects (packaging mockups, extruded type, revolved bottles, inflated icons) inside
Illustrator, kept as an editable effect on 2D artwork.

## Create
1. Draw the 2D profile: a closed shape or type for **Extrude** and **Inflate**; half a profile (open or closed,
   drawn to the right of the axis) for **Revolve**.
2. Effect > 3D and Materials (Window > 3D and Materials). Choose Object type: Plane, Extrude, Revolve, Inflate.
3. Set **Depth**, **Bevel** (extrude), **Revolve angle** and **Offset from** (left or right edge), and
   rotate with the on-canvas widget or presets (Front, Isometric Left, etc.).

## Materials and artwork mapping
- **Materials** tab: default materials or Adobe Substance materials (wood, metal, plastic); adjust their
  parameters (colour, roughness, metallic).
- **Map artwork**: drag a symbol or graphic into the Materials tab (Graphics section), then position and scale it
  on the selected face. Labels for bottles and box art go here; keep the art as a symbol so edits update the 3D.

## Lighting and render
- **Lighting** tab: presets (Standard, Diffuse, Top Left, Right) or custom, with intensity, rotation,
  height, softness and ambient light; **Shadows** behind or below the object.
- **Render with Ray Tracing** gives realistic light and reflections but is slow; turn it on only for final
  output and set quality to High.
- Object > **Expand Appearance** for a static result; with ray tracing it produces a raster image, without
  ray tracing it produces vector shading. Export the 3D model (OBJ, USDA, GLTF) from the panel menu for
  other apps.

## Gotchas
- Classic 3D (Effect > 3D and Materials > 3D (Classic)) is the old engine; mixing both in a file is confusing.
- Complex type with many points makes the effect slow; outline and simplify first.
- Strokes on the source shape are extruded too; remove them or outline them intentionally.
- Raster render resolution follows Document Raster Effects Settings; set it before final export.

## Verify
- [ ] Mapped art sits on the right face, unstretched, and updates when the symbol is edited.
- [ ] Final output either live with correct raster resolution or expanded to the agreed format.
