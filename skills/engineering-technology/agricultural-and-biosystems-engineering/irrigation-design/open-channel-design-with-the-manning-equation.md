---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.open-channel-design-with-the-manning-equation
name: open-channel-design-with-the-manning-equation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, manning-open-channel, manning-equation, canal-design, channel-lining, normal-depth, freeboard, permissible-velocity]
level: advanced
status: gated
description: "Design a trapezoidal irrigation canal or ditch using Manning's equation: roughness, normal depth, velocity limits, lining, freeboard and check structures."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Open channel design with the Manning equation

**Goal:** a canal section that carries the design flow at a stable depth without erosion or silting.

## Equation
Q = (k/n) x A x R^(2/3) x S^(1/2), where A is flow area, R hydraulic radius (A / wetted perimeter), S bed slope, n Manning roughness, and k = 1.0 in SI (m, m3/s) or 1.486 in US units (ft, cfs; computed as 3.2808^(1/3), usually rounded to 1.49). Solve for normal depth by iteration for a given section.

## Choosing n and section
- n depends on lining and condition: concrete lined channels are commonly about 0.012-0.017, earth channels about 0.02-0.03 with weeds raising it (gated: unconfirmed, source is paywalled or blocked). Use the guidance in NRCS or ASCE tables for your channel type.
- Trapezoidal sections: side slopes set by soil (flatter for sandy soils); bottom width / depth ratio near efficient hydraulic shape for lined canals, wider for earth channels.
- Limit velocity: below the permissible non-erosive velocity for the soil or lining and above the silt-deposition limit.
- Freeboard above the water surface for waves and fluctuations; follow the design manual.
- Check structures raise levels at turnouts; design turnouts hydraulically for required head.

## Seepage
Seepage loss through earth canals can be a large fraction of water diverted; consider lining or piping where economics allow.

## Verify
- [ ] Normal depth computed at maximum and minimum flows.
- [ ] Velocity within permissible limits at each flow.
- n values for your condition: use NRCS or ASCE tables and local calibration (gated: unconfirmed, source is paywalled or blocked).
