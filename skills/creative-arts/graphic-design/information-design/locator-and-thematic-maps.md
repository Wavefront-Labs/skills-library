---
id: creative-arts.graphic-design.information-design.locator-and-thematic-maps
name: locator-and-thematic-maps
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, locator-map, thematic-map, choropleth, map-design, map-projection, openstreetmap, natural-earth]
level: practitioner
status: draft
description: "Design locator and thematic maps: pick a projection and basemap with licence checks, simplify, use normalised choropleths with suitable classes, and label and credit properly."
sources:
  - https://www.openstreetmap.org/
  - https://www.naturalearthdata.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thematic and locator maps

**Goal:** a map that shows one thing clearly (where something is, or how a value varies), with honest data treatment and proper credit.

## Locator maps (where is it?)
- Show the target highlighted (strong colour) against a muted context, with a larger-scale context inset or an overview map.
- Keep only what orients the reader: borders, major water, a few labelled places. Remove roads and labels that do not help.
- Add scale information where distance matters, and a north arrow only when north is not up.

## Thematic maps (how does a value vary?)
- **Choropleth** (shaded areas): use for **rates or ratios** (per capita, per km2), never raw totals, because large areas dominate visually. Choose a sequential single-hue ramp for ordered data and a diverging ramp only with a meaningful midpoint.
- **Classes:** 4-7 classes; method (equal interval, quantiles, natural breaks) changes the story, so choose deliberately and state it in the legend. Test two methods.
- **Proportional symbols** for totals; **dot density** for distribution; **flow lines** for movement.
- Colour-blind-safe ramps; check on greyscale.

## Projection and geometry
- Pick a projection suited to the area and message (a world map's projection distorts area or shape; mention it if it matters). Do not use Web Mercator for comparing areas of large regions.
- Simplify boundaries for the output scale, but keep topology (avoid gaps and slivers).

## Data and licences
- Natural Earth data is dedicated to the public domain. OpenStreetMap data is under the ODbL licence and requires visible credit ("OpenStreetMap contributors") and share-alike obligations for derived databases. Other commercial basemap providers have their own terms; read them before publishing.
- Keep a record of data source and date for the credit line.

## Workflow
1. Prepare data and join in a GIS or mapping tool (QGIS is free; web tools such as Datawrapper are quick for choropleths).
2. Export vector (SVG or PDF) and finish typography, legend and annotations in Illustrator.
3. Legend: units, class breaks and the data year; title that states the finding.

## Self-check
Does the title state the finding? Are values normalised? Is the credit line there? Greyscale and colour-blind check done.
