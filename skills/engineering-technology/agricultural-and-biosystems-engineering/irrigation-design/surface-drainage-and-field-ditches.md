---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.surface-drainage-and-field-ditches
name: surface-drainage-and-field-ditches
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, surface-drainage, field-ditches, land-forming, bedding, grassed-waterway, design-storm, drainage-ditch]
level: practitioner
status: gated
description: "Design surface drainage for fields: land forming, bedding, shallow field ditches, design storm, ditch capacity and outlet erosion control."
sources:
  - "USDA NRCS National Engineering Handbook, Part 650 Engineering Field Handbook (https://www.nrcs.usda.gov)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Surface drainage and field ditches

**Goal:** remove ponded water from the field surface quickly enough to protect the crop, without erosion.

## Methods
- Land forming or smoothing to remove depressions and give continuous slope to field ditches.
- Bedding: crowned beds with furrows between to carry water.
- Field ditches (shallow, flat-sided, crossable) collecting from rows, then laterals, then mains.
- Surface inlets in depressions that connect to subsurface drains.

## Design
1. Choose a design storm and criterion: for example the removal of a depth of water in a number of hours for a crop; regional guidelines specify the frequency (for example 10-year events for vegetables, less for field crops (gated: unconfirmed, source is paywalled or blocked)), so use your agency's.
2. Compute peak runoff with a method suited to the area (Rational method for small areas, NRCS curve number methods).
3. Size ditches with Manning's equation (`open-channel-design-with-the-manning-equation`), with side slopes for machinery to cross and for stability.
4. Outlets: stabilise with rock or pipe drops; avoid headcutting; check downstream capacity and legal rights.

## Notes
Wetland and stream regulations can limit ditch work; get permits. Sediment and nutrient losses may be regulated.

## Verify
- [ ] Ditch grade survey as-built.
- [ ] Inspect after the first storm for erosion and ponding.
- Design return period for your area: take it from the regional drainage guide (gated: unconfirmed, source is paywalled or blocked).
