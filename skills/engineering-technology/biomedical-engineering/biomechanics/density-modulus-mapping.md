---
id: engineering-technology.biomedical-engineering.biomechanics.density-modulus-mapping
name: density-modulus-mapping
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [density-modulus-mapping, implant-fea, bone-fea, ct-based-fe, qct, bone-density-calibration, power-law-modulus, helgason]
level: advanced
status: draft
description: "Map CT density to elastic modulus in bone FE models: phantom calibration, density to modulus relations, binning, site dependence and limits of each equation."
sources: ["Helgason et al., Mathematical relationships between bone density and mechanical properties: a literature review (Clin Biomech 2008)", "Morgan, Bayraktar and Keaveny, Trabecular bone modulus-density relationships depend on anatomic site (J Biomech 2003)", "Carter and Hayes, The compressive behavior of bone as a two-phase porous structure (J Bone Joint Surg Am 1977)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Density-to-modulus mapping for bone FE

**Goal:** assign each element of a CT-based bone model a modulus from CT intensity that is defensible for the anatomical site.

## Steps
1. **CT calibration:** scan with a phantom of known equivalent bone density (for example K2HPO4 or hydroxyapatite rods) in the same field of view, same kV and reconstruction; fit HU to equivalent density (rho_QCT).
2. **Convert** equivalent density to apparent density or ash density as the chosen relation requires (the conversion factor depends on the paper).
3. **Choose a modulus relationship** from the literature, matching site and loading: power law E = a rho^b; for example vertebral and femoral trabecular relations of Morgan (E in MPa, rho in g/cm3 with exponents around 1.5-2) and Carter and Hayes (cubic dependence for combined cortical and trabecular). Relations vary widely among sources, so confirm the units and variable definition before use.
4. **Cortical bone:** modulus limited to a physiological cap (about 17-20 GPa); partial-volume effects at thin cortex underestimate density, so correct or model the cortical thickness explicitly.
5. **Binning:** group elements into a limited number of materials (for example 10-100 bins) to limit file size and avoid false precision, with Abaqus or Ansys material assignment scripts.
6. **Poisson ratio:** about 0.3 as a default, with other values justified.
7. **Validate:** compare simulated strain or stiffness against experimental data on the same specimens (strain gauges, DIC) and compute errors.

## Gotchas
- Mixing a relation developed for one site (vertebra) with another (femur) without validation.
- Using HU directly without phantom calibration; HU depends on scanner, kV, and patient size.
- Mesh resolution that does not capture trabecular heterogeneity but is given trabecular properties.

## Verify
- [ ] Phantom calibration line stored with R-squared.
- [ ] Sensitivity run for plus or minus 20% in modulus and for different equations.
- [ ] Validation error vs experiment reported.
