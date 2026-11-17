---
id: creative-arts.graphic-design.information-design.schematic-transit-network-maps
name: schematic-transit-network-maps
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, schematic-map, network-map, transit-map, metro-map, line-diagram, harry-beck]
level: advanced
status: draft
description: "Design schematic transit-style network maps: simplify geography to 45-degree and vertical lines, even station spacing, clear interchanges, line colours and labels."
sources:
  - https://helpx.adobe.com/illustrator/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Schematic (transit-style) network maps

**Goal:** a diagram where the topology is clear (which lines connect where) even though geography is distorted on purpose.

## Principle
The model is the London Underground diagram drawn by Harry Beck from 1931, which discarded geographic accuracy in favour of clear connections: stations are shown in sequence along straight lines, with interchanges obvious. Most modern transit maps follow its approach.

## Build steps
1. **Collect data:** lines, ordered station lists, interchanges, termini, ordering of branches. Keep the network as data (a table or a graph).
2. **Choose a grid:** lines run horizontal, vertical or at 45 degrees only. Set a grid unit in Illustrator (**Preferences > Guides & Grid**) and snap to it.
3. **Place the trunk lines first,** then branches; keep the relative position of stations roughly right where it helps the reader (river, centre, airports) without letting geography drive the layout.
4. **Even station spacing** (or a small number of fixed spacings) along each line. Stations are small ticks on a line; interchanges are larger markers (circle or connected tick).
5. **Bends:** use rounded corners with a consistent radius; avoid more bends than needed.
6. **Colour and line weight:** one colour per line with strong separation, checked for colour-blind readers; add line labels at the ends and direct labelling beside the line where space allows.
7. **Labels:** station names horizontal where possible, placed consistently relative to the marker (never over lines); halo or knock-out where crossing is unavoidable.

## Extras
- Zone shading, river hint and airport symbols, accessibility symbols in a legend.
- Provide a geographic overview or note that it is not to scale.

## Failure modes
- Distortion so strong that a short walk looks long; tolerate it only when labelled.
- Too many angles; labels overlapping lines.

## Self-check
Trace each line end to end; verify every interchange connects the correct lines and that the station order matches the service pattern.
