---
id: creative-arts.fashion-design.clo-3d.importing-dxf-aama-patterns
name: importing-dxf-aama-patterns
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-pattern-tools, clo-2d-pattern, dxf-aama, clo-dxf-import, astm-dxf, pattern-import, gerber, lectra]
level: practitioner
status: draft
description: "Import DXF-AAMA/ASTM patterns into CLO 3D from Gerber, Lectra, Optitex or Tukatech: export settings, scale and units, grain, internal lines, graded sizes and clean-up."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.astm.org/d6673-10r20.html
  - https://en.wikipedia.org/wiki/AutoCAD_DXF
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Importing DXF-AAMA patterns into CLO

**Goal:** bring production patterns from 2D CAD into CLO with correct scale, grain lines,
notches and internal lines, ready for sewing.

## Export from the 2D CAD
- Export as **DXF-AAMA** or **ASTM D6673** (the ASTM version of AAMA DXF) - the standard
  format for pattern exchange with grain lines, notches, internal lines and grading.
- Include: piece names, grain lines, notches, drill holes, internal lines; graded nest if you
  want sizes.
- Export **net (sew) lines plus seam allowance** or both lines (CLO can use the sew line as the
  pattern outline and add seam allowance as a property).

## Import in CLO
1. **File > Import > DXF (AAMA/ASTM)** (also accessible via Add for adding to an open project).
2. Options:
   - **Scale/unit**: match the CAD unit (mm, cm, inch); wrong units = tiny or huge patterns.
   - Import as **Open** (new project) or **Add**.
   - Choose whether to import cut lines as the pattern outline and sew lines as internal
     lines, or vice versa (choose net line as outline for best sewing accuracy, then add
     seam allowance in CLO).
   - Grading options when a graded nest is present (import sizes).
   - Auto-arrangement attempts to place pieces on arrangement points.
3. Check: piece count, names, grain lines (CLO uses each pattern's grain direction for
   fabric physics), notches imported as notches.

## Clean-up
- Mirror/symmetric pieces: link with **Symmetric Pattern (Clone)** so edits copy across.
- Delete duplicate lines; convert unneeded internal lines.
- Set grain lines correctly on pieces that imported without them.
- Fix piece orientation (front/back side) before arranging.

## Gotchas
- Mixing cut lines and sew lines when sewing produces garments too large.
- Missing grain lines make fabric physics wrong (stretch in the wrong direction).
- Some CAD exports split curves into many points; simplify only if needed.

## Verify
- [ ] Measured piece dimensions in CLO match the CAD.
- [ ] Grain lines and notches present on every piece.
- [ ] Symmetric pieces linked.
