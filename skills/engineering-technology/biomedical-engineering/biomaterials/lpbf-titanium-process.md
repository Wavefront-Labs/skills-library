---
id: engineering-technology.biomedical-engineering.biomaterials.lpbf-titanium-process
name: lpbf-titanium-process
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [laser-powder-bed-fusion, additive-manufactured-implants, lpbf, additive-manufacturing, ti-6al-4v, powder-reuse, hot-isostatic-pressing, astm-f3001, astm-f2924]
level: advanced
status: verified
description: "Control laser powder bed fusion of Ti-6Al-4V implants: energy density, atmosphere, powder reuse, orientation, stress relief, HIP and witness coupons."
sources: ["ASTM F2924 Standard specification for additive manufacturing titanium-6 aluminum-4 vanadium with powder bed fusion (confirm edition)", "ASTM F3001 Additive manufacturing titanium-6 aluminum-4 vanadium ELI with powder bed fusion", "FDA guidance Technical Considerations for Additive Manufactured Medical Devices (December 2017)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LPBF titanium process control

**Goal:** repeatable, qualified Ti-6Al-4V parts from laser powder bed fusion with known mechanical properties and surface.

Regulated manufacturing; follow the FDA additive-manufacturing guidance, ISO 13485 process validation and applicable ASTM or ISO standards (confirm editions).

## Process parameters
- **Power, speed, hatch spacing and layer thickness** set the volumetric energy density: E = P / (v h t). Typical values for Ti-6Al-4V sit in the range of tens of J/mm3 with layers of 30-60 microns, but the processing window is machine-specific; define it by density cubes and tensile tests.
- **Scan strategy:** rotation between layers, contour passes, supports for overhangs; downskin parameters differ.
- **Atmosphere:** high-purity argon with controlled oxygen level (typically below a few hundred ppm) and gas-flow design that clears spatter.

## Powder
- Specify powder per ASTM F3001 or F2924: chemistry (oxygen limit for ELI), size distribution, morphology, flowability.
- **Reuse:** powder picks up oxygen and fines; track reuse count and test oxygen and particle size each lot; define blend rules.

## Post-processing
1. Stress relief on the build plate (typical 650-800 C, in vacuum or argon (gated: unconfirmed, source is paywalled or blocked)).
2. Remove from plate by wire EDM; remove supports.
3. **Hot isostatic pressing (HIP)** (for example about 900-950 C, 100 MPa, 2 h (gated: unconfirmed, source is paywalled or blocked); ASTM F3001 has HIP clauses, confirm the required parameters there) closes internal porosity and improves fatigue; confirm with microstructure and tests.
4. Machining and surface finishing for critical interfaces; chemical or electropolish; cleaning validation for residual powder.

## Qualification
- Witness specimens (tensile, fatigue, density, microstructure) per build in multiple locations and orientations; mechanical properties are anisotropic, so test relevant orientations.
- Non-destructive inspection (CT) for critical features, with a rule for acceptance.
- Process validation: installation, operational and performance qualification across the build volume; requalify after machine service.

## Verify
- [ ] Oxygen, density and tensile results meet the standard in every orientation used.
- [ ] Powder lot and reuse records traceable to each build.
- [ ] Fatigue of surface-as-built regions assessed.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
