---
id: creative-arts.graphic-design.editorial-layout.dielines-and-die-cut-artwork
name: dielines-and-die-cut-artwork
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, print-finishing, print-specification, dieline, die-cut, cutter-guide, crease-lines, perforation, packaging-artwork, overprint-dieline, spot-colour-layer]
level: practitioner
status: draft
description: "Prepare die-cut artwork: dieline as a named overprinting spot colour on its own layer, cut/crease/perf conventions, bleed past cuts and safe zones."
sources:
  - https://helpx.adobe.com/illustrator/using/spot-process-colors.html
  - https://www.esko.com/en/products/artioscad
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dielines and die-cut artwork

**Goal:** artwork that the die cutter can read unambiguously and that looks right after cutting and folding.

## Get the dieline from the converter
Ask the printer/packaging converter for the **dieline** (structural drawing, often from ArtiosCAD) as PDF/AI/DXF for
the exact stock. Do not draw your own for production unless they ask - their die exists already or is made from their
CAD.

## Set up the file
- Put the dieline on its **own top layer** (`Dieline`), locked.
- Colour the lines with a **spot colour swatch** named as the printer asks (`Dieline`, `CutContour`, `Die`), 100%,
  e.g. magenta-looking; set strokes to **Overprint Stroke** so the dieline never knocks out art if it reaches the plates.
- Line conventions (confirm with the printer): **solid = cut**, **dashed = crease/fold**, dash-dot or other = perforation;
  some use different spot colours per function.
- Never outline or modify the dieline geometry; never add effects to it.

## Artwork rules
- **Bleed:** 3 mm (packaging often 3-5 mm) beyond every cut edge, including inner cut-outs (windows).
- **Safe zone:** keep text and critical elements >= 3 mm inside cut lines and away from crease lines (folds crack ink
  and shift slightly).
- Glue areas: no ink/varnish where adhesive goes (the converter marks glue flaps) - knock out artwork there.
- Check orientation on each panel (top/bottom of a carton) - build a **3D mock-up** or print, cut and fold a sample.

## Output
PDF with the dieline layer visible as a separate spot plate; some printers want a second PDF without the dieline.
Separations Preview: dieline appears only on its own plate.

## Gotchas
- Dieline in CMYK colour instead of spot = it prints on the job.
- Small details or text near cuts get trimmed due to die tolerance (~1 mm).

## Verify
- [ ] Dieline on own layer, spot colour, overprint; untouched geometry.
- [ ] Bleed beyond all cuts; text inside safe zones; folded sample checked.
