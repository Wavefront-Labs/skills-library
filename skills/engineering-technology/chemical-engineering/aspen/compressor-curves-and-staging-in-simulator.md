---
id: engineering-technology.chemical-engineering.aspen.compressor-curves-and-staging-in-simulator
name: compressor-curves-and-staging-in-simulator
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-rotating-equipment-and-hydraulics, compressor-curves-and-staging-in-simulator, compressor-curves, multistage-compression, intercooler]
level: practitioner
status: gated
description: "Enter compressor performance curves and set up multistage compression with intercoolers in Aspen Plus and HYSYS."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compressor curves and staging in simulator

**Goal:** Enter compressor performance curves and set up multistage compression with intercoolers in Aspen Plus and HYSYS.

## Steps
1. For staging, split the overall pressure ratio roughly equally per stage, subject to a maximum discharge temperature or ratio per stage; use MCompr with intercoolers (gated: unconfirmed, source is paywalled or blocked). Check on ideal-gas isentropic work (computed: k=1.4, 300 K inlet, overall ratio 9, intercooling back to 300 K): one stage 7.62 kJ/mol, two equal-ratio stages 6.44 kJ/mol, and the minimum over all splits is at ratio 3 per stage, so equal ratios are the right first split.
2. Specify intercooler outlet temperatures and pressure drops, with knockout of condensate where relevant.
3. Enter curves (head, efficiency and flow at several speeds) in the performance-curve form (AspenTech's study guide confirms performance curves for pumps and compressors) to rate an existing machine at off-design conditions.
4. Run cases at minimum, normal and maximum flow and check surge and stonewall margins.
5. Compare simulation power and discharge temperature with the vendor datasheet.

## Gotchas
- Curves are speed and gas specific; correct for molecular weight and inlet conditions if the gas differs.
- Do not extrapolate beyond the curve.

## Verify
- [ ] Operating points lie within surge and stonewall limits.
- [ ] Staged power is lower than single-stage as expected.
