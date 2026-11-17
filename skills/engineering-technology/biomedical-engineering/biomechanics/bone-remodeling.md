---
id: engineering-technology.biomedical-engineering.biomechanics.bone-remodeling
name: bone-remodeling
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [bone-remodeling, wolff-law, mechanostat, adaptive-bone, strain-energy-density]
level: advanced
status: draft
description: "Explain and model bone adaptation to load (Wolff law, Frost mechanostat, strain-energy-density remodelling) and its use in implant design and stress shielding studies."
sources: ["Frost, Bone Mass and the Mechanostat (Anatomical Record, 1987)", "Huiskes et al., Adaptive bone-remodeling theory applied to prosthetic-design analysis (J Biomech, 1987)", "Nordin and Frankel, Basic Biomechanics of the Musculoskeletal System", "https://www.isbweb.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Bone remodelling and Wolff law

**Goal:** understand how load history changes bone mass and structure, and use that in implant analysis.

## Concepts
- **Wolff law:** bone adapts its architecture to the loads it carries. It is a qualitative principle; quantitative models are approximations.
- **Mechanostat (Frost):** strain windows. Very low strain (disuse) leads to net loss; a physiological window maintains bone; high strain causes modelling to add bone; microdamage and fracture occur at higher strain. Commonly cited strain levels are order-of-magnitude (disuse below roughly a few hundred microstrain, modelling around 1000-1500 microstrain or more, microdamage above about 3000, fracture near 20000-25000); treat as approximate and confirm in the literature.
- **Remodelling units:** osteoclasts resorb, osteoblasts form; coupled process taking months.

## Computational models
- Strain-energy-density (SED) models: the rate of density change depends on the difference between SED per unit mass and a reference, with a dead zone (lazy zone) where no net change occurs. Iterate with FEA to predict density redistribution after an implant.
- Parameters (reference stimulus, dead-zone width, rate constant) are calibrated to data and uncertain; test sensitivity.
- Use the model qualitatively to compare designs (for example stiff versus compliant stems) and validate against DXA or radiographic bone density change data.

## Verify
- [ ] Loading cases cover daily activity, not a single peak load.
- [ ] Parameters and dead zone justified; sensitivity shown.
- [ ] Predictions compared with clinical density data where possible.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
