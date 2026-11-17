---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.attenuation-correction
name: attenuation-correction
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [attenuation-correction, pet, spect, nuclear-imaging, ct-based-attenuation, mu-map, 511-kev, mr-ac]
level: advanced
status: verified
description: "Correct attenuation in PET and SPECT: LOR attenuation factors, transmission sources, CT-based 511 keV conversion, MR-based methods, misregistration and metal artefacts."
sources: ["https://physics.nist.gov/PhysRefData/XrayMassCoef/ComTab/water.html", "Cherry, Sorenson and Phelps, Physics in Nuclear Medicine", "Kinahan et al., Attenuation correction for a combined 3D PET/CT scanner (Med Phys 1998;25:2046-2053)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Attenuation correction in PET and SPECT

**Goal:** correct for photon absorption in the body so that images are quantitatively accurate and free of depth-dependent bias.

## PET physics
- For an annihilation along a line of response (LOR), both 511 keV photons must escape, so the survival probability is exp(-integral of mu along the whole LOR), **independent of the position of the source along that LOR**. The attenuation correction factor (ACF) = exp(integral of mu dl) can therefore be measured with an external transmission source.
- Water at 511 keV has a linear attenuation coefficient of about 0.096 per cm (NIST XCOM: mass attenuation 0.09687 and 0.08956 cm2/g at 0.5 and 0.6 MeV, log-log interpolated to 0.511 MeV gives 0.0960 cm2/g, density 1 g/cm3); soft tissue about the same, bone higher, lung lower by density.

## Methods
1. **Transmission scans** with a rotating rod or point source (Ge-68 or Cs-137) before or after emission imaging, measure projections directly (older systems).
2. **CT-based:** acquire a low-dose CT; convert CT numbers (HU at about 80-140 kVp) to linear attenuation at 511 keV using a **bilinear (piecewise) scaling**: a line through air and water for soft tissue, a second slope for bone, with a different slope because the photoelectric effect at CT energies overstates bone attenuation at 511 keV. Smooth to PET resolution, and forward project to get ACFs.
3. **MR-based** (PET/MR): no direct measure of bone attenuation. Methods: segmentation of Dixon water/fat images into soft tissue, fat, lung, air (bone ignored or added from atlas), ultrashort-echo-time sequences for bone, atlas-based and deep-learning pseudo-CT.
4. **SPECT:** the attenuation depends on source depth, so correction uses a measured or CT-derived attenuation map within iterative reconstruction (for example with an ordered-subset algorithm including a depth-dependent attenuation model), plus scatter and resolution recovery; the Chang first-order method is an approximation for uniform media.

## Artefacts and pitfalls
- **Misregistration** between PET and CT from respiration or patient movement causes errors (for example a lung-liver dome artefact); check registration or use respiratory gating or breath-hold CT.
- **Metal implants** create CT streaks that overestimate attenuation (hot artefacts); review non-attenuation-corrected images and use metal artefact reduction.
- **Oral and IV contrast** raise HU and lead to attenuation overestimation unless corrected.
- **Truncation** of the CT field of view for patients with arms down.

## Verify
- [ ] Uniform phantom (cylinder with known activity) reconstructed with correction shows uniform activity within a few percent.
- [ ] Compare uncorrected and corrected images for suspicious artefacts.
- [ ] Verify HU to mu conversion curve on a phantom with inserts of known density.
