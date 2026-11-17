---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.anti-scatter-grid
name: anti-scatter-grid
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [anti-scatter-grid, x-ray-tube, x-ray-generation, grid-ratio, bucky-factor, grid-cutoff, scatter-radiation, air-gap]
level: practitioner
status: gated
description: "Choose anti-scatter grids: ratio, strip density, focal distance, Bucky factor, grid cutoff errors, moving versus stationary grids and alternatives like air gap."
sources: ["Bushberg et al., The Essential Physics of Medical Imaging (scatter and grids)", "Curry, Dowdey and Murry, Christensen's Physics of Diagnostic Radiology", "IEC 60627 Diagnostic X-ray imaging equipment - Characteristics of general purpose and mammographic anti-scatter grids (confirm edition)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Anti-scatter grids

**Goal:** reduce scattered radiation that lowers image contrast, at a controlled dose cost.

## Construction and terms
- Thin lead strips separated by radiolucent interspace material (aluminium or carbon fibre).
- **Grid ratio r = h / D**, strip height divided by interspace width. Common general radiography ratios are 6:1 to 12:1, mammography about 4:1 to 5:1 (gated: unconfirmed, source is paywalled or blocked) (textbook values).
- **Strip density** (lines per centimetre, typically 40-80 (gated: unconfirmed, source is paywalled or blocked)); higher density hides lines but may thin strips.
- **Focused grid:** strips angled to converge at a focal distance (for example 100 or 180 cm); work only within the focal range.

## Performance measures
- **Bucky factor (grid factor)** = exposure with grid / exposure without grid for the same image receptor dose; typically 3-5 for general radiography, higher for high ratios and higher kVp (gated: unconfirmed, source is paywalled or blocked).
- **Contrast improvement factor**, **selectivity**, and primary and scatter transmission.
- Higher ratio removes more scatter but increases patient dose and positioning sensitivity.

## Cutoff errors
Grid cutoff (loss of primary radiation at one or both edges) occurs when:
- the tube is off-level (tilted across the lines),
- off-centre (lateral decentring),
- off-focus (distance outside the focal range),
- or the grid is upside down (focused grids).

## Moving versus stationary
A **Potter-Bucky** grid moves during exposure to blur the lines; stationary grids show lines unless density is high or digital line suppression is applied. In digital radiography, aliasing between grid lines and the detector pixel pitch creates moire patterns; choose a grid frequency that avoids it.

## Alternatives
- **Air-gap technique:** increased object-to-detector distance reduces scatter reaching the detector at the cost of magnification and geometric unsharpness.
- Software scatter correction.

## Verify
- [ ] Bucky factor measured in your system and used in technique charts.
- [ ] Test for cutoff with off-centre and angle conditions.
- [ ] No moire at the detector in test images.
