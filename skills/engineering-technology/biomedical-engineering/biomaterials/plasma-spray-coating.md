---
id: engineering-technology.biomedical-engineering.biomaterials.plasma-spray-coating
name: plasma-spray-coating
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [plasma-spray, surface-modification, implant-coatings, titanium-plasma-spray, hydroxyapatite-coating, porous-coating, astm-f1147, astm-f1854, coating-adhesion]
level: advanced
status: draft
description: "Specify and test plasma-sprayed titanium and hydroxyapatite coatings on implants: process variables, porosity, thickness, adhesion and shear tests, and FDA expectations."
sources: ["ASTM F1854 Standard test method for stereological evaluation of porous coatings on medical implants (confirm edition)", "ASTM F1147 Tension testing of calcium phosphate and metallic coatings", "ASTM F1044 Shear testing of calcium phosphate coatings and metallic coatings", "US FDA guidance on calcium phosphate coating (current text at https://www.fda.gov)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Plasma-sprayed implant coatings

**Goal:** a porous or bioactive coating that bonds well to the substrate and gives bone ingrowth or on-growth, with controlled variability.

Regulated implant coatings; FDA guidance on calcium phosphate coatings sets recommended properties (confirm current edition and any EU or other requirements).

## Process
- Powder fed into a plasma jet (thousands of degrees) melts and accelerates onto a grit-blasted substrate; splats solidify into a layered, porous coating.
- **Titanium porous coating:** thickness often in the range of several hundred microns to about a millimetre, porosity roughly 30-50%, pore size around 100-300 microns; sprayed in vacuum or inert gas to limit oxidation.
- **Hydroxyapatite (HA):** thickness commonly 50-150 microns; high temperature decomposes HA to amorphous calcium phosphate, tricalcium phosphate and calcium oxides, so crystallinity and phase purity are controlled.
- Key variables: powder size and morphology, torch power, gas mix, stand-off distance, substrate temperature, traverse speed and fixturing. Lock them in a validated procedure.

## Tests
1. **Thickness and porosity:** metallographic sections with image analysis (ASTM F1854) for titanium; XRD for HA phase content and crystallinity (ASTM F2024, confirm).
2. **Adhesion:** tensile adhesion (ASTM F1147) and shear (ASTM F1044), fatigue of coated specimens (ASTM F1160), abrasion (ASTM F1978).
3. **Composition:** HA Ca/P ratio, trace elements (ASTM F1185 on HA and F1609 on calcium phosphate coatings; confirm).
4. **Substrate effect:** plasma-sprayed titanium notches the surface and can lower fatigue strength; test coated and uncoated.
5. **Particle release:** sprayed coating particulate and dissolution studies.

## Acceptance
- Define criteria such as minimum tensile strength, shear strength, crystallinity and phase purity; the numbers should come from the FDA guidance and device-specific justification.
- Process capability by batch witness coupons.

## Verify
- [ ] Coupons with each lot pass adhesion and microstructure criteria.
- [ ] Coating cleaning and packaging validated (no residual grit).
- [ ] Fatigue test of finished coated device if the coating is in a high-stress region.
