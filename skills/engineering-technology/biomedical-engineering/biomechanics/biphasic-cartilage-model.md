---
id: engineering-technology.biomedical-engineering.biomechanics.biphasic-cartilage-model
name: biphasic-cartilage-model
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [biphasic-cartilage, cartilage-mechanics, confined-compression, aggregate-modulus, poroelastic]
level: advanced
status: draft
description: "Use the biphasic (solid plus fluid) model of articular cartilage: confined compression creep and stress relaxation, aggregate modulus and permeability, and how to fit them."
sources: ["Mow, Kuei, Lai and Armstrong, Biphasic creep and stress relaxation of articular cartilage in compression (J Biomech Eng, 1980)", "Mow and Hayes, Basic Orthopaedic Biomechanics and Mechano-Biology", "https://www.isbweb.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Biphasic cartilage model

**Goal:** describe cartilage as a porous, permeable solid matrix saturated with fluid, so time-dependent behaviour comes from fluid flow.

## Model
- Two incompressible phases: solid (collagen and proteoglycan) and interstitial fluid. Load is shared between solid stress and fluid pressure; drag between phases (permeability k) controls flow.
- Equilibrium response is set by the **aggregate modulus H_A** (order 0.5 to 1 MPa for healthy human cartilage) and **permeability k** (order 10^-15 m^4 per newton second; confirm for your tissue and site).

## Confined compression test
1. Cut a cylindrical plug, place in a confining chamber with a porous platen on top so fluid exits axially.
2. **Creep:** apply a constant load; thickness decreases toward equilibrium. **Stress relaxation:** apply a ramp displacement then hold; stress peaks then relaxes.
3. The characteristic time scales as thickness squared divided by (H_A times k). For a 2 mm sample this is of the order of an hour or more, so tests must be long enough to reach equilibrium.
4. Fit the analytical solution to determine H_A and k; the equilibrium value gives H_A, the transient gives k.

## Extensions
- Indentation tests with biphasic or poroviscoelastic solutions for intact joints; transversely isotropic, fibril-reinforced and swelling (charged matrix) models for more realism.
- Use poroelastic elements in FE when fluid pressure and load sharing matter (for example meniscus and cartilage contact).

## Verify
- [ ] Plug thickness, hydration bath and temperature controlled.
- [ ] Test duration reaches equilibrium; fit quality reported.
- [ ] Parameter values compared with literature for the same species and site.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
