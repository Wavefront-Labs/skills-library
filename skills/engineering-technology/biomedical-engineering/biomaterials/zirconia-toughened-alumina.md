---
id: engineering-technology.biomedical-engineering.biomaterials.zirconia-toughened-alumina
name: zirconia-toughened-alumina
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [zirconia-toughened-alumina, bioceramics, hydroxyapatite, ceramic-bearing, alumina, y-tzp, low-temperature-degradation, iso-6474, ceramic-head]
level: advanced
status: draft
description: "Select ceramic bearings for joint replacement: alumina, ZTA and zirconia properties, phase-transformation ageing, fracture risk, taper design and proof testing."
sources: ["ISO 6474-1 Implants for surgery - Ceramic materials - Part 1 high purity alumina (confirm edition)", "ISO 6474-2 Composite materials based on high purity alumina matrix with zirconia reinforcement", "ISO 13356 Ceramic materials based on yttria-stabilized tetragonal zirconia (Y-TZP)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Alumina, ZTA and zirconia bearings

**Goal:** choose the bearing ceramic and design its interfaces to avoid brittle fracture while retaining the low wear of ceramic-on-ceramic or ceramic-on-polyethylene.

Safety-critical implant work; confirm current edition of the ISO standards and regulatory guidance for ceramic components.

## Materials (approximate; check supplier data)
- **High-purity alumina:** hard, very low wear and bioinert; flexural strength of the order of 400-600 MPa and fracture toughness near 4 MPa m^0.5; susceptible to brittle fracture.
- **Zirconia-toughened alumina (ZTA):** alumina matrix with dispersed zirconia (and additives) giving higher strength and toughness (strengths around 1000 MPa and toughness above 6 MPa m^0.5 reported) with alumina's stability.
- **Y-TZP zirconia:** higher strength and toughness but susceptible to **low-temperature degradation**: tetragonal-to-monoclinic transformation in humid or aqueous conditions roughens the surface; field problems with zirconia heads in the early 2000s were linked to processing and ageing, which makes ageing tests essential.

## Design rules
- Ceramics fail from flaws; limit stress concentrations (radii, taper geometry) and design the taper with the correct angle and tolerance matched to the stem.
- Avoid edge loading in ceramic liners (positioning, chamfers); liner-shell mismatch and impingement chip ceramic edges.
- Stem taper contamination (fluid or debris at assembly) can cause fracture.

## Testing and quality
1. Raw material: chemistry, grain size, density, strength per ISO 6474 or 13356.
2. **Proof testing** (each head loaded to a defined force in a fixture) to screen defects, in addition to static burst tests (ISO 7206-10 head load tests; confirm part and edition) and fatigue.
3. **Ageing:** hydrothermal ageing in autoclave and monitoring of monoclinic phase for zirconia-containing materials.
4. Surface roughness, sphericity, wear in a hip simulator (ISO 14242) with micro-separation conditions.
5. Lot traceability and non-destructive inspection.

## Verify
- [ ] Burst strength with margin over body-weight-derived loads.
- [ ] Ageing results show no significant monoclinic increase.
- [ ] Taper and liner tolerances controlled; fracture-risk entries in the risk file.
