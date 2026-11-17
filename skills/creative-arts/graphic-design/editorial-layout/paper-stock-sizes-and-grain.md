---
id: creative-arts.graphic-design.editorial-layout.paper-stock-sizes-and-grain
name: paper-stock-sizes-and-grain
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, print-finishing, print-specification, paper-stock, iso-216, paper-sizes, gsm, paper-weight, grain-direction, coated, uncoated, opacity, bulk, caliper, sra3]
level: practitioner
status: draft
description: "Specify paper for print jobs: ISO 216 and US sizes, gsm vs lb weights, coated vs uncoated, opacity, bulk and grain direction, and how each choice affects colour, folding and cost."
sources:
  - https://www.iso.org/standard/36631.html
  - https://www.papersizes.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Paper stock, sizes and grain

**Goal:** a paper specification that suits the design, prints the colour you expect, folds
cleanly and fits the press sheet economically.

## Sizes
- **ISO 216 A series:** A0 = 1 m2 (841 x 1189 mm); each step halves: A3 297x420, A4 210x297,
  A5 148x210, A6 105x148. Aspect ratio 1:sqrt(2), so halving keeps proportions.
- **B series** (posters, books) and **C series** (envelopes: C5 fits A5/A4 folded once,
  DL 110x220 fits A4 folded in three).
- **SRA** sizes (SRA3 320x450 mm) are press sheets with room for bleed and marks: an A4 with
  bleed fits on SRA4, not A4 stock.
- **US:** Letter 8.5x11 in, Legal 8.5x14, Tabloid 11x17; press sheets 12x18, 19x25, 25x38.
Design to sizes that impose efficiently on the printer's sheet - an odd size can cost a whole extra sheet per copy.

## Weight
- **gsm** (g/m2) internationally. Rough guide: 80-100 gsm letterhead/copy; 115-170 gsm
  brochure text; 250-350 gsm covers, postcards, business cards (350-400+).
- **US basis weight** (lb) depends on paper category: 80 lb text ~ 118 gsm; 80 lb cover ~ 216 gsm.
  Always convert to gsm when comparing.
- **Caliper/bulk** (thickness, microns) matters for spine width and feel; two papers at the same
  gsm can differ in thickness.

## Surface
- **Coated** (gloss, silk/satin, matt): ink sits on top, sharp detail, saturated colour,
  higher ink limits.
- **Uncoated** (offset, bond): ink absorbs, colours flatter/darker, more dot gain - use an
  uncoated profile and avoid large dark solids or fine reversed type.
- **Opacity:** thin uncoated stock shows through (show-through) - important for text both sides.
- Brightness/whiteness and optical brighteners affect colour (FOGRA51 assumes OBA papers).

## Grain direction
Paper fibres align in one direction. **Folds and binding must run parallel to the grain**:
across-grain folds crack (especially on heavy coated stock with solid colour on the fold) and
book pages fight the spine. Long-grain vs short-grain is quoted on the printer's stock list.
Heavy stocks (>170 gsm) need **creasing/scoring** before folding.

## Verify
- [ ] Spec names size, gsm, surface finish, brand/stock if known, and grain for folded/bound work.
- [ ] Colour profile matches the coated/uncoated choice.
- [ ] Format checked against the printer's press sheet for waste.
