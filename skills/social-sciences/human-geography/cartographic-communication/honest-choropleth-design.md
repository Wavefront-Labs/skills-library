---
id: social-sciences.human-geography.cartographic-communication.honest-choropleth-design
name: honest-choropleth-design
category: social-sciences
field: human-geography
product: cartographic-communication
tags: [cartographic-communication, cartography, thematic-mapping, choropleth, choropleth-design, data-classification, quantile, equal-interval, natural-breaks, jenks, standard-deviation-classification, manual-breaks, colorbrewer, sequential-palette, diverging-palette, colour-blind-safe, viridis, map-projection, equal-area-projection, web-mercator, albers, cartogram, dot-density, proportional-symbols, bivariate-map, map-uncertainty, margins-of-error, legend-design, map-critique, how-to-lie-with-maps, small-numbers-problem]
level: practitioner
status: draft
description: "Designing choropleths that don't mislead: normalisation, classification (quantile, Jenks, equal interval), colour schemes, equal-area projections and uncertainty."
sources: ["Monmonier, How to Lie with Maps (3rd ed., 2018)", "Brewer, Designing Better Maps (2nd ed.)", "Brewer & Pickle, 'Evaluation of Methods for Classifying Epidemiological Data on Choropleth Maps' (2002)", "ColorBrewer 2.0 (colorbrewer2.org)", "Slocum et al., Thematic Cartography and Geovisualization"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Honest choropleth design

**Goal:** publish area-shaded maps of social data whose visual message matches the
data — and be able to critique maps that don't.

## 1. Is a choropleth even right?
Choropleths shade areas, so big empty areas dominate perception (a sparsely populated
county looks more important than a dense city).
- **Counts** (number of people, cases) → proportional symbols or dot-density, not a
  choropleth.
- **Rates/ratios/percentages** → choropleth is appropriate.
- Big-area distortion matters (elections!) → consider a **cartogram** or hex-tile map.

## 2. Normalise
Divide by an appropriate denominator: population, households, land area, people at
risk. "Per 100,000 residents" ≠ "per km²" — choose by the question. Small populations
make rates jumpy (**small-numbers problem**): flag, suppress, aggregate, or smooth
(empirical Bayes).

## 3. Classification
- **Quantile:** equal number of areas per class. Good for ranking and a balanced
  look; can put very different values in one class or split near-identical ones.
- **Equal interval:** equal value ranges; honest for evenly spread data, but skewed
  data leaves most areas in one class.
- **Natural breaks (Jenks):** minimises within-class variance; data-specific, so not
  comparable across maps.
- **Standard deviation:** pair with a diverging palette around the mean.
- **Manual/meaningful breaks:** policy thresholds (e.g. 50%), round numbers.
- **5–7 classes** is the usual readable maximum. Brewer & Pickle found quantile
  performs well for general reading tasks in their tests.
- **Gotcha:** the same data can look calm or alarming by classification alone — try
  several (QGIS *Symbology › Graduated › Mode*; ArcGIS Pro *Graduated Colors › Method*)
  and choose deliberately. For a series of maps (years, variables) use **identical
  breaks** so they're comparable.
- Show a histogram of the data with breaks while choosing.

## 4. Colour
- **Sequential** (light → dark) for low → high; **diverging** only when there's a
  meaningful midpoint (zero change, national average); **qualitative** for categories.
- Use ColorBrewer or viridis-family schemes; check colour-blind safety and print/
  grayscale legibility.
- Darker = more is the expected convention; don't use rainbow ramps.
- No-data areas get a distinct neutral (hatched or light grey) and a legend entry.

## 5. Projection
For area-shaded maps use an **equal-area projection** (e.g. Albers Equal Area for the
contiguous US, Lambert Azimuthal Equal Area (EPSG:3035) for Europe, Equal Earth for the
world). **Web Mercator** inflates high-latitude areas and exaggerates them visually.

## 6. Legend, labels and uncertainty
- Legend with units and class bounds that don't overlap (10–19.9, 20–29.9).
- Title states variable, place, date; note data source and denominator.
- Survey estimates (e.g. ACS) have margins of error: hatch unreliable areas, or add
  a companion map of coefficients of variation. A bivariate map (value × reliability)
  is an option.

## 7. Map critique checklist (for others' maps)
Raw counts on areas? Unmarked classification? Mercator? Truncated colour ramp? Missing
no-data class? Different breaks between compared maps?

See social-sciences.human-geography.gis-social-research.geocoding-census-joins-and-thematic-maps
for producing the underlying rates, and the cartography skill
architecture-construction.cartography-geospatial-mapping.map-design.visual-hierarchy-and-thematic-symbology
for general visual hierarchy.

## Verify
- [ ] Mapped variable is normalised; counts shown with symbols instead.
- [ ] Classification method chosen deliberately and stated; identical breaks across a series.
- [ ] Palette type matches data (sequential/diverging) and is colour-blind safe.
- [ ] Equal-area projection used.
- [ ] Legend has units, non-overlapping bounds, no-data class, source and reliability notes.
