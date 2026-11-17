---
id: engineering-technology.biomedical-engineering.biomechanics.bone-mechanical-testing
name: bone-mechanical-testing
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [bone-testing, bone-mechanics, cortical-bone, trabecular-testing, specimen-preparation]
level: practitioner
status: gated
description: "Test bone specimens mechanically: specimen preparation and hydration, end artefacts, strain measurement, rate effects and what to report for cortical and trabecular bone."
sources: ["Cowin (ed.), Bone Mechanics Handbook", "Keaveny et al., Biomechanics of trabecular bone (Annual Review of Biomedical Engineering, 2001)", "Nordin and Frankel, Basic Biomechanics of the Musculoskeletal System", "https://www.isbweb.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bone mechanical testing

**Goal:** obtain reproducible modulus and strength values and interpret them against the right reference.

## Preparation
- Keep specimens hydrated with saline; freezing storage (about -20 C) has small effect on mechanics if thawed gently, drying has a big effect (gated: unconfirmed, source is paywalled or blocked).
- Machine with water or saline cooling to avoid heat damage; record orientation relative to the bone axis (cortical bone is anisotropic).
- Record donor age, sex, site, density or bone volume fraction.

## Test methods
- **Tension or compression of machined cortical coupons:** measure strain with an extensometer or optical method on the gauge length; crosshead displacement overestimates strain (machine compliance and end effects).
- **Trabecular cubes or cylinders:** compression with the aspect ratio and end treatment controlled; end artefacts (damage at cut ends) reduce apparent modulus unless bonded or embedded ends and strain-on-gauge methods are used.
- **Bending (three or four point) and torsion** of whole bones or machined beams for structural properties.
- **Rate:** bone is viscoelastic; report strain rate. Fatigue and creep need defined stress levels and cycle counts.
- **Indentation and microCT-based FEA** give local or image-based estimates.

## Report
- Specimen origin and handling, orientation, density, strain measurement method, loading rate, temperature, modulus definition (linear region fit) and yield definition (for example 0.2 percent offset).

## Verify
- [ ] Hydration and temperature controlled and reported.
- [ ] Strain measured on the specimen, not crosshead only.
- [ ] Anisotropy and density accounted for when comparing with literature (see trabecular-cortical-properties).

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
