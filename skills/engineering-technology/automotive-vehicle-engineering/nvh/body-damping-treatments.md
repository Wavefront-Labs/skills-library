---
id: engineering-technology.automotive-vehicle-engineering.nvh.body-damping-treatments
name: body-damping-treatments
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [body-damping, damping-treatment, constrained-layer-damping, extensional-damping, loss-factor, oberst-beam, sprayable-damping, astm-e756, sae-j1637, panel-damping, body-acoustics]
level: practitioner
status: gated
description: "Specify body damping treatments: free-layer and constrained-layer pads and sprayables, loss factor and temperature range, placement from vibration maps, and Oberst bar testing."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "ASTM E756 and SAE J1637 (vibration damping material properties by the Oberst beam method); astm.org returned 403 and the SAE page did not load, confirm titles and editions"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Body damping treatments

## 1. Purpose
Large thin steel panels (floor, dash, roof, doors) vibrate and radiate noise; damping reduces resonant response and the radiated sound and structure-borne noise in the mid frequencies. It does not reduce non-resonant (mass-controlled) transmission; insulation does that.

## 2. Types
- **Free-layer (extensional) damping:** a viscoelastic layer (bitumen sheet, butyl or polymer) bonded to the panel; damping from extension of the layer; effective with thicker layers; heavy.
- **Constrained-layer damping:** viscoelastic layer plus a stiff constraining layer (aluminium or steel foil); shear of the viscoelastic core gives more damping per mass.
- **Sprayable or liquid-applied sound deadener:** robot-applied waterborne coatings that cure in the paint oven, automated and weight-efficient; typically lower efficiency per mass than pads.
- **Bonded or integral:** laminated steel (a viscoelastic core between steel sheets) for dash panels and oil pans.

## 3. Material properties
Loss factor (eta) and modulus vs temperature and frequency (viscoelastic materials peak in damping near their glass transition). Select material whose peak covers the operating range (typical cabin-panel range roughly -10 to 50 degC, wider for under-body; engineering judgement (gated: unconfirmed, source is paywalled or blocked)). Measure by the Oberst (vibrating cantilever beam) method per ASTM E756 or SAE J1637, giving composite loss factor of a coated steel strip; convert to material properties using the standard's equations.

## 4. Placement
- Identify panels and areas with highest vibration response and radiating contribution (see panel acoustic contribution); apply damping at high-velocity zones (antinodes of mode shapes, away from panel edges).
- Coverage: partial coverage (often of the order of 30-50% of area in the high-response region (gated: unconfirmed, source is paywalled or blocked)) typically gives most of the achievable damping; beyond that, the benefit per kg falls. Use FE modal strain-energy or measured loss factors to optimise.
- Avoid placing on ribbed or stiff regions where the panel does not bend.
- Compatibility with paint ovens, adhesives, sealer; adhesion on oiled steel.

## 5. Verification
Subtractive or additive vehicle tests with measured interior SPL for a given excitation (modal shaker, road, or tyre); measure panel loss factors by impact decay or modal tests; confirm a durable bond after ageing and thermal cycling. Weight and cost efficiency: dB per kg.

## Verify
- [ ] Damping material measured on Oberst beam across temperature.
- [ ] Placement chosen from vibration or strain-energy maps.
- [ ] Coverage vs benefit curve checked, not just full coverage.
- [ ] Bond durability and manufacturing compatibility confirmed.
