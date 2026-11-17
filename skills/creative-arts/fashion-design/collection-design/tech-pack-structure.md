---
id: creative-arts.fashion-design.collection-design.tech-pack-structure
name: tech-pack-structure
category: creative-arts
field: fashion-design
product: collection-design
tags: [fashion-design, collection-design, tech-pack, techpack, tech-pack-structure, techpack-template, spec-package, product-development, plm]
level: practitioner
status: draft
description: "Structure a garment tech pack: cover page, flats, measurements, BOM, construction, artwork, colourways, labels, packing and revision log, in PLM or spreadsheet form."
sources:
  - https://www.astm.org/d5219-21.html
  - https://en.wikipedia.org/wiki/Product_lifecycle_management
  - https://www.fitnyc.edu/academics/academic-divisions/art-and-design/fashion-design/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tech pack structure and page set

**Goal:** a document set that lets a factory you have never met make the sample right
the first time, and that records every change after.

## Standard page set
1. **Cover/style summary**: style number, name, season, category, size range, base size,
   fabric summary, front/back flat, designer, dates, factory, status.
2. **Flats/sketches**: front, back (side and inside views where needed), with callouts.
3. **Detail pages**: close-up drawings of pockets, collars, closures with measurements.
4. **Points of measure (POM) and spec sheet**: base size measurements, tolerances,
   graded sizes.
5. **Bill of materials (BOM)**: fabrics, linings, interlinings, trims, labels, thread,
   packaging, each with supplier, ref, colour, placement and quantity.
6. **Construction**: seam types, stitch types and SPI, seam allowances, finishes.
7. **Artwork/print/embroidery**: placement, size, colours, files.
8. **Colourways**: colour per component per colourway.
9. **Labels and packaging**: care/content label, size label, hangtags, folding, polybag.
10. **Fit comments and revision log**: dated changes, who approved.

## Tools
PLM systems (Centric, Backbone, Gerber/Lectra PLM, Bamboo Rose) or Illustrator/Excel
templates. Keep one source of truth; PDFs sent out are dated snapshots.

## Rules
- Units stated (cm or inches) on every measurement page.
- Every revision gets a date, version and changed fields highlighted.
- Use standard POM codes and terminology (ASTM D5219 for body/garment dimension terms).

## Gotchas
- Missing back views and inside details cause the most sample errors.
- Changing the tech pack without a revision note creates disputes over which sample is right.
- Over-long tech packs bury key info; summary page first.

## Verify
- [ ] All ten sections present (or marked N/A).
- [ ] Units and version on every page.
- [ ] Revision log updated with every change.
