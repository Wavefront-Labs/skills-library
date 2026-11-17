---
id: creative-arts.graphic-design.editorial-layout.output-preview-and-total-area-coverage
name: output-preview-and-total-area-coverage
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, pdf-x, print-ready-pdf, total-area-coverage, ink-limit, output-preview, separations, tac, overprint-simulation, rich-black-limit]
level: advanced
status: draft
description: "Inspect separations and total ink coverage in Acrobat Output Preview: plate list, TAC highlighting against the press limit, overprint simulation, and fixing over-inked areas."
sources:
  - https://helpx.adobe.com/acrobat/using/output-preview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Output preview and total area coverage

**Goal:** confirm what each plate will print and that no area carries more ink than the press and paper can take.

## Output Preview (Acrobat Pro > Print Production > Output Preview)
- **Simulation Profile:** set to the output intent (e.g. PSO Coated v3, GRACoL2013). Tick **Simulate Overprinting**
  and optionally Simulate Paper Color / Black Ink.
- **Separations** list: every plate in the file (Process Cyan/Magenta/Yellow/Black + spots). Untick plates to see
  what is on each; unexpected spots show up here.
- Hover anywhere: the panel shows **ink percentages per plate** and the total at that point.

## Total area coverage (TAC / total ink limit)
- Tick **Total Area Coverage** and enter the limit: e.g. **300%** for coated sheetfed (FOGRA39 profile limit 330%,
  many printers ask 300-320%), **260-280%** for uncoated, ~240% for newsprint, web offset coated ~300%. Areas over the
  limit are highlighted.
- Over-limit areas risk set-off (ink transferring to the next sheet), slow drying, muddy shadows.

## Typical causes and fixes
| Cause | Fix |
|---|---|
| Rich black built as 100/100/100/100 (400%) or RGB black converted | Use the printer's rich black recipe (e.g. C60 M40 Y40 K100 = 240%) - see rich black |
| Images converted with the wrong profile | Reconvert from RGB with the correct profile, or let PDF/X-4 output handle it |
| Shadows of dark photos | Correct profile conversion handles TAC via GCR; otherwise convert with the right profile in Photoshop |
| Overlapping transparencies with multiply | Flatten/adjust the artwork, recheck |
Fix at source and re-export; avoid editing colours in the PDF.

## Overprint checks
With Simulate Overprinting on, check: black text overprints (no white halos on misregistration), white objects do not
overprint (would vanish), spot varnish/white plates overprint as intended.

## Verify
- [ ] Only the quoted plates appear in the Separations list.
- [ ] TAC highlight shows no areas over the printer's limit.
- [ ] Overprint simulation looks as intended.
