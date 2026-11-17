---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.beam-hardening-artifacts
name: beam-hardening-artifacts
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [beam-hardening, ct-reconstruction, filtered-backprojection, cupping, streak-artifact, polychromatic-beam, water-correction, dual-energy]
level: advanced
status: gated
description: "Recognise and reduce CT beam hardening: cupping and streaks, causes in polychromatic beams, water and bone corrections, filters, dual-energy options and phantom checks."
sources: ["Hsieh, Computed Tomography: Principles Design Artifacts and Recent Advances (artifact chapters)", "Kak and Slaney, Principles of Computerized Tomographic Imaging", "Barrett and Keat, Artifacts in CT: recognition and avoidance (RadioGraphics 2004;24:1679-1691)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CT beam hardening artefacts

**Goal:** minimise cupping and dark streaks caused by the polychromatic X-ray spectrum.

## Cause
X-ray tubes produce a spectrum; low-energy photons are attenuated more, so the beam's mean energy rises as it passes through the object (it hardens). Reconstruction assumes monochromatic attenuation, so the line integral is not linear with thickness, giving artefacts.

## Appearance
- **Cupping:** centre of a uniform object appears darker than the periphery.
- **Dark bands and streaks** between dense objects (bone, metal, contrast agent), for example between the petrous bones.

## Corrections
1. **Hardware:** added beam filtration and a bowtie filter flatten the spectrum and reduce path-length variation; higher kVp reduces effects (with more noise in contrast).
2. **Water (first-order) correction:** a polynomial correction applied to the projection data to linearise the response of water-equivalent material; calibrate with water phantoms of several diameters.
3. **Iterative bone correction** (second-order): estimate bone thickness from an initial image and correct the projections; reduces bone-induced streaks and cupping in the head.
4. **Metal artefact reduction** algorithms (MAR) for implants; they combine interpolation and iterative methods.
5. **Dual-energy CT:** monoenergetic reconstructions and basis material decomposition reduce beam hardening.

## Evaluation
- Scan a uniform water phantom at various diameters; measure the mean HU in the centre and edge ROIs; cupping magnitude = centre minus edge (acceptable tolerances are typically a few HU in QC protocols (gated: unconfirmed, source is paywalled or blocked); confirm yours).
- Phantoms with high-density inserts reveal streaks; measure the HU deviation between inserts.

## Verify
- [ ] Water uniformity within tolerance at the kVp used.
- [ ] After correction, streak artefacts reduced on the test phantom.
- [ ] HU accuracy of inserts still within tolerance.
