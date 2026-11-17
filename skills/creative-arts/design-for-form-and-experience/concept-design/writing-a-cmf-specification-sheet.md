---
id: creative-arts.design-for-form-and-experience.concept-design.writing-a-cmf-specification-sheet
name: writing-a-cmf-specification-sheet
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [cmf, color-material-finish, cmf-spec-sheet, colour-specification, material-callouts, surface-finish, product-design, supplier-handoff]
level: practitioner
status: draft
description: "Write a CMF spec sheet that a supplier can quote and match: part map, material grade, colour reference, texture code, gloss, coatings and approval samples."
sources:
  - "IDSA CMF Design resources (idsa.org)"
  - "Mold-Tech (Standex) texture library documentation"
  - "VDI 3400 surface texture standard"
  - "ASTM D523 Standard Test Method for Specular Gloss"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CMF specification sheet

**Goal:** one document per product colourway that turns the CMF design intent into
something a moulder, painter and QC inspector can each act on without guessing.

## Sheet layout
1. **Header:** product, colourway name, revision, date, owner, status (concept / for quote /
   released).
2. **Part map:** an exploded or callout render with every visible part numbered (P01 housing
   top, P02 bezel, P03 button...). Include parts seen only when in use (inside a lid).
3. **Table, one row per part:**
| Field | Example |
|---|---|
| Material + grade | PC/ABS, supplier grade X, UL94 V-0 if required |
| Colour | Supplier masterbatch code + Pantone or RAL reference + "match to approved plaque CW-02" |
| Finish / texture | Mold-Tech MT-11010 or VDI 3400 ref 24; or SPI A-2 polish for gloss |
| Gloss | 5-8 GU at 60 degrees (ASTM D523) |
| Secondary process | Soft-touch paint, PVD, anodise type II, pad print, laser etch |
| Notes | Avoid weld line on top face, gate hidden under label |
4. **Graphics and marking:** logo files, size, position from a datum, process.
5. **Approval:** physical colour plaques (golden samples) referenced by ID, viewing
   conditions (D65 light booth), tolerance (for example Delta E 2000 under 1.0).

## Rules
- A Pantone number alone is not a plastic spec; Pantone swatches are printed ink. Always
  require a moulded plaque in the actual resin and texture.
- Texture changes perceived colour and gloss: specify colour as measured on the textured plaque.
- Same colour on two materials (painted metal next to moulded plastic) needs a cross-material
  match plaque set; expect them to diverge under different light (metamerism).
- Keep one sheet per colourway; do not mix CW-01 and CW-02 in one table.

## Verify
Hand the sheet to someone outside the team: they can say for every visible surface what it is
made of, what colour, which texture, and against which physical sample it is accepted.
