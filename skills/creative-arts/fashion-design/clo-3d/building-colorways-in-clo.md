---
id: creative-arts.fashion-design.clo-3d.building-colorways-in-clo
name: building-colorways-in-clo
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-colorway, clo-colorways, colorway-editor, pantone-library, digital-colourways]
level: practitioner
status: draft
description: "Build colorways in CLO 3D: Colorway Editor, assigning fabric, trim and graphic colours per colorway, Pantone libraries, batch renders and colorway reports."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building colorways in CLO

**Goal:** several colorways of one garment in a single project file, each with correct
fabrics, trims and artwork colours, rendered consistently.

## Colorway Editor
1. Open **Colorway Editor** (Window menu or the colorway area of the Object Browser).
2. Add a colorway (duplicate the current one); name it with the colour code from the
   line plan (e.g. "CW02 Navy").
3. For each material (fabrics, buttons, zippers, topstitches, graphics), set the colour per
   colorway: pick from a **Pantone library** or enter values; replace the texture for
   yarn-dyed fabrics or prints.
4. Switch between colorways to review in 3D.

## Rendering colorways
- Set the camera views once; **batch render** all colorways with the same render settings.
- Export colorway thumbnails for line sheets and digital showrooms.

## Accuracy
- Screen colour is not physical colour; reference Pantone TCX codes and physical lab dips.
- Use calibrated monitors for review; consistent lighting/HDRI in renders.
- For prints, each colorway needs its own texture file (recoloured repeat).

## Workflow tips
- Lock base design changes before creating colorways; edits to patterns apply to all
  colorways, but material assignments are per colorway.
- Keep material names meaningful ("shell", "contrast collar") for clear editing.

## Gotchas
- Editing a material in one colorway when you meant all.
- Trims left default in some colorways (silver zip in a gold-hardware colorway).
- Changing texture scale per colorway inconsistently.

## Verify
- [ ] Every material checked in every colorway.
- [ ] Names match line plan colour codes.
- [ ] Batch renders use identical camera and lighting.
