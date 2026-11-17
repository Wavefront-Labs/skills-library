---
id: engineering-technology.biomedical-engineering.biomechanics.trabecular-cortical-properties
name: trabecular-cortical-properties
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [trabecular-bone, bone-mechanics, bone-biomechanics, cortical-bone, anisotropy, apparent-density, bone-modulus]
level: practitioner
status: gated
description: "Use realistic cortical and trabecular bone properties in design and models: anisotropy, density-dependent modulus, strength and strain limits, and how age and site change them."
sources: ["Keaveny et al., Biomechanics of trabecular bone (Annu Rev Biomed Eng 2001)", "Currey, Bones: Structure and Mechanics", "Nordin and Frankel, Basic Biomechanics of the Musculoskeletal System"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cortical and trabecular bone properties

**Goal:** choose defensible material properties for bone in implants, test blocks and models, with an honest range.

Values below are typical order-of-magnitude figures recalled from textbooks and reviews and are not checked against a free primary source (gated: unconfirmed, source is paywalled or blocked) (the Keaveny 2001 abstract confirms only that properties vary widely with site, age and disease, depend strongly on density, and that failure strains are almost independent of density); they vary strongly with site, age, sex, disease and test method, so use measured or study-specific data where available.

## Cortical bone
- Transversely isotropic: stiffer along the long axis. Longitudinal modulus roughly 15-20 GPa, transverse roughly 6-12 GPa.
- Longitudinal ultimate strength: in compression higher than in tension (very roughly 170 MPa vs 130 MPa); strength in shear and transverse directions is lower.
- Yield strain is small, around 0.6-0.8% in tension and about 1% in compression; post-yield is limited, so fracture follows soon after.

## Trabecular bone
- Apparent density range from about 0.1 to 1.0 g/cm3; modulus and strength are strongly density dependent (modulus roughly proportional to density squared, strength to density to the 1.5 to 2 power in common fits).
- Apparent modulus from about 0.1 to 2 GPa depending on site (vertebra low, femoral neck higher); highly anisotropic and heterogeneous.
- Tissue-level modulus (the trabecula itself) about 10-20 GPa, similar to cortical tissue.

## Using it
1. For FE models map CT density to modulus per element with a published relationship (see density-modulus-mapping) and note the equation's site and calibration.
2. For bench tests use synthetic bone (cellular polyurethane foams, e.g. grades covered by ASTM F1839) for repeatability and cadaveric bone for realism; say which you used.
3. Account for age and osteoporosis: reduced density and cortical thinning can halve strength.

## Gotchas
- Dry bone is stiffer and more brittle than wet bone; keep specimens hydrated and test at body temperature where practical.
- Loading rate matters (bone is viscoelastic).

## Verify
- [ ] Material properties tied to a citation and site.
- [ ] Sensitivity run with plus or minus 20% modulus.
