---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.spect-collimators
name: spect-collimators
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [spect-collimator, gamma-camera-collimator, parallel-hole, lehr, septal-penetration]
level: advanced
status: draft
description: "Choose SPECT collimators: parallel-hole, fan, cone and pinhole geometries, hole size and length, resolution-sensitivity trade-off, septal penetration and energy rating."
sources: ["Bushberg et al., The Essential Physics of Medical Imaging (nuclear imaging chapters)", "Cherry, Sorenson and Phelps, Physics in Nuclear Medicine", "https://www.snmmi.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SPECT collimators

**Goal:** select a collimator geometry that gives the best compromise of resolution and sensitivity for the isotope and task.

## Principles
- A collimator is a lead or tungsten plate with holes that accepts photons travelling in a narrow direction range. **Parallel-hole** collimators are standard; **fan-beam and cone-beam** magnify for small organs; **pinhole** gives high resolution and magnification for small objects (thyroid, small animals).
- **Geometric resolution** of a parallel-hole collimator: R_g is about d times (L + z) divided by L, where d is hole diameter, L the hole length and z the source distance; resolution worsens linearly with distance. Example (illustrative values): d = 1.5 mm, L = 35 mm, z = 100 mm gives R_g of about 5.8 mm.
- **Sensitivity** scales roughly with (d / L) squared, so improving resolution (long, narrow holes) costs sensitivity: the trade-off defines collimator classes such as low-energy high-resolution (LEHR) and low-energy general-purpose (LEGP).
- **Septal penetration:** photons crossing septa blur the image; septal thickness must stop photons at the isotope energy. Technetium-99m (140 keV) uses low-energy collimators; higher-energy isotopes (for example iodine-131) need medium or high energy collimators with thicker septa.

## Selection
1. Isotope energy and count rate; organ size and distance; required resolution at the working distance.
2. Orbit close to the patient and avoid larger z.
3. Verify with a point or line source: measure resolution (full width at half maximum) versus distance and sensitivity.

## Verify
- [ ] Collimator rating matches the isotope energy.
- [ ] Resolution and sensitivity measured and compared with specification.
- [ ] Damage inspection (bent septa) and uniformity check.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
