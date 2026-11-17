---
id: engineering-technology.biomedical-engineering.biomechanics.hyperelastic-tissue-models
name: hyperelastic-tissue-models
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [hyperelastic, soft-tissue-mechanics, viscoelasticity, constitutive-model, ogden, mooney-rivlin, neo-hookean, fung, parameter-fitting]
level: advanced
status: draft
description: "Fit hyperelastic constitutive models to soft-tissue tests: neo-Hookean, Mooney-Rivlin, Ogden, Yeoh and Fung forms, preconditioning, multi-mode data and stability checks."
sources: ["Holzapfel, Nonlinear Solid Mechanics", "Fung, Biomechanics: Mechanical Properties of Living Tissues", "FEA package documentation for hyperelastic material fitting (for example Abaqus and Ansys user manuals)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Hyperelastic tissue models

**Goal:** a constitutive model that reproduces measured soft-tissue behaviour across the strain range you will simulate and is numerically stable in FE.

## Choosing a form
- **Neo-Hookean:** one parameter, small to moderate strain, rubber-like; rarely fits tissue's stiffening.
- **Mooney-Rivlin, Yeoh:** polynomial in invariants; Yeoh handles strain stiffening with a few parameters.
- **Ogden:** principal-stretch series, flexible for biaxial data.
- **Fung exponential and HGO (Holzapfel-Gasser-Ogden):** exponential stiffening and fibre families, used for arteries, ligaments, skin.
- Add near-incompressibility (volumetric term with bulk modulus or hybrid elements).

## Workflow
1. **Test:** preconditioned tissue (cyclic loading until the response repeats), hydrated at the right temperature, with tests in more than one mode (uniaxial plus equibiaxial or shear) so the fit is unique; record geometry carefully.
2. **Convert** raw force-displacement to stress-stretch (Cauchy or first Piola-Kirchhoff, state which).
3. **Fit** with nonlinear least squares, ideally on all modes simultaneously; start from physical initial guesses and check parameter bounds.
4. **Check stability** (Drucker): the fitted model must stay stable in all deformation modes in your simulation, not only the tested ones; FE packages report stability checks.
5. **Validate** on an independent test (indentation, inflation) not used for fitting.

## Gotchas
- A single uniaxial test fits many models equally well and extrapolates differently.
- Strain-rate effects need viscoelasticity (see quasi-linear-viscoelasticity).
- Over-parameterised fits (Ogden order 3) overfit noise.

## Verify
- [ ] Fit residual reported per mode.
- [ ] Stability check passed for planned deformations.
- [ ] Independent validation error stated.
