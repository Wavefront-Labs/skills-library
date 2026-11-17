---
id: creative-arts.fashion-design.knitwear-design.knit-charts-and-stitch-graphs
name: knit-charts-and-stitch-graphs
category: creative-arts
field: fashion-design
product: knitwear-design
tags: [fashion-design, knitwear-design, knit-spec, knit-tech-pack, knit-chart, stitch-graph, stitch-symbols, knit-programming-brief]
level: practitioner
status: draft
description: "Draw knit charts and stitch graphs for programmers and hand knitters: grid aspect ratio, standard symbols, repeats, colour keys and needle-out diagrams for trims."
sources:
  - https://www.craftyarncouncil.com/standards/knit-chart-symbols
  - https://www.bloomsbury.com/uk/knitwear-9782940411719/
  - https://www.shimaseiki.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stitch graphs and knit charts

**Goal:** unambiguous charts that a programmer (machine) or knitter (hand) can follow to
knit exactly the stitch and colour pattern designed.

## Grid
- One square = one stitch wide x one row high.
- Use a **knitter's grid** with the stitch aspect ratio of the gauge (stitches are wider
  than tall), so motifs look as they will knit. Example: 7 stitches/2.5 cm and 10 rows/2.5 cm
  = cells 1.43:1.
- Mark repeats with bold lines and number rows (odd rows right to left for flat hand
  knitting; machine charts per programmer convention).

## Symbols
- Use standard symbols (Craft Yarn Council for hand-knit charts): knit, purl, cable left/
  right (with stitch counts), yarn over, k2tog, ssk, tuck, miss, transfer.
- Provide a **legend** on every chart; machine houses may use their own codes - agree with
  the programmer.

## Colour charts
Colour key with yarn references (spinner, quality, colour code). For jacquard, mark
backing type; for intarsia, mark carrier areas.

## Needle-out diagrams
For ribs and trims: show which needles are in action on front and back beds (e.g. 1x1 rib
alternates front/back; 2x2 = 2 front, 2 back).

## Gotchas
- Square grids distort motifs in the knit.
- Missing legend or non-standard symbols cause programming errors.
- Charts not showing where the repeat starts relative to CF make placement random.

## Verify
- [ ] Grid aspect ratio matches gauge.
- [ ] Legend and colour key present.
- [ ] Repeat start positioned relative to CF/hem.
