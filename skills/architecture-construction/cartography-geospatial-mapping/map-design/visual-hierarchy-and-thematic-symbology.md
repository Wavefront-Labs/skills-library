---
id: architecture-construction.cartography-geospatial-mapping.map-design.visual-hierarchy-and-thematic-symbology
name: visual-hierarchy-and-thematic-symbology
category: architecture-construction
field: cartography-geospatial-mapping
product: map-design
tags: [map-design, cartography, cartographic-design, visual-hierarchy, figure-ground, symbology, symbolisation, thematic-mapping, choropleth, graduated-symbols, proportional-symbols, classification, natural-breaks, jenks, quantile, equal-interval, normalisation, colour-schemes, sequential, diverging, qualitative, colorbrewer, colour-blind-safe, labelling, label-placement, typography, generalisation, layout, legend, map-projection, basemap]
level: practitioner
status: draft
description: "Design a map that reads: purpose and audience, figure-ground hierarchy, the right thematic method, normalised data, classification choice, colour schemes, label typography and a lean layout."
sources: ["Brewer, Designing Better Maps; ColorBrewer 2.0", "Dent, Torguson & Hodler, Thematic Cartography and Geovisualization", "Tyner, Principles of Map Design"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visual hierarchy and thematic symbology

**Goal:** a map whose main message is seen first, whose numbers are represented
honestly, and that remains readable in greyscale and by colour-blind readers.

## 1. Purpose, audience, medium
Write one sentence: *"This map shows X so that Y can decide Z."* It decides scale,
extent, what to include, and how much to generalise. Note the medium (A4 print, slide,
phone screen) — it decides minimum text size and line weights.

## 2. Visual hierarchy (figure-ground)
Rank every layer: **figure** (the thematic subject) → supporting reference (roads,
places) → background (land/water, basemap). Then encode the ranking:
- Figure: strongest contrast, saturation and weight.
- Reference: mid-grey, thinner lines, smaller labels.
- Background: low contrast, desaturated; water slightly darker or lighter than land
  consistently.
Squint test: blur your eyes — the first thing you see must be the figure. Most maps
fail because the basemap shouts.

## 3. Choose the thematic method by data type
- **Totals** (counts: population, cases) → **proportional/graduated symbols** or dot
  density. *Never* a choropleth of raw totals — large areas look important just for being large.
- **Rates/ratios/densities** (per capita, per km², %) → **choropleth**.
- **Categories** (land use, zoning) → qualitative colours (hue differences only).
- **Continuous surfaces** (elevation, temperature) → isolines or hypsometric shading.
Normalise counts by population or area before a choropleth.

## 4. Classification
- **Quantile:** equal count per class; good for ranking, but can split near-identical values.
- **Equal interval:** easy to read; poor on skewed data.
- **Natural breaks (Jenks):** groups clusters; data-specific so not comparable across maps.
- **Manual/meaningful breaks:** thresholds people care about (policy targets, round numbers).
Use 4–7 classes. Check the histogram first; state the method in the legend notes.
For multi-map comparisons use the **same breaks** on every map.

## 5. Colour
- **Sequential** (light → dark, one or two hues) for low-to-high data; darker = more.
- **Diverging** (two hues meeting at a neutral midpoint) only when the midpoint means
  something (zero change, national average).
- **Qualitative** hues for categories, similar lightness.
- Use tested schemes (e.g. ColorBrewer, viridis family); avoid rainbow ramps for ordered
  data — perceived lightness jumps around and misleads.
- Check colour-blind safety (simulate deuteranopia) and greyscale legibility.

## 6. Labels and type
- Hierarchy through size, weight and case: capitals spaced for large areas, italics for
  water features (a long convention), regular for settlements.
- Point labels: preferred position upper-right of the symbol, then other positions.
- Line labels follow the line, upright, on gentle curves; areas: spread inside the shape.
- Minimum print size around 6–7 pt; avoid label/feature collisions with halos sparingly
  (thin, background-coloured).

## 7. Layout
Title that states the message, legend with units and class method, scale bar
(appropriate for the projection), north arrow only if north isn't up or orientation
matters, source and date, CRS. Remove anything that doesn't serve the purpose.

## Projection
Thematic maps of areas need an **equal-area** projection at small scales; Web Mercator
inflates high latitudes and misleads area comparisons.

## Verify
- [ ] Squint test: the figure reads first.
- [ ] Choropleth only on normalised data; totals use symbols.
- [ ] Classes 4–7, method stated, identical breaks across compared maps.
- [ ] Palette sequential/diverging/qualitative to match the data; colour-blind checked.
- [ ] Legend has units; source, date and CRS noted; projection suits the message.
