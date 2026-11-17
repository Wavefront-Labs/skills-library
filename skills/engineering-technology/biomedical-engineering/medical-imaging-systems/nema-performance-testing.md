---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.nema-performance-testing
name: nema-performance-testing
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [nema-testing, nema-nu-2, nema-nu-1, pet-performance, gamma-camera-performance]
level: practitioner
status: gated
description: "Plan NEMA performance measurements for PET and gamma cameras (NU 2 and NU 1): resolution, sensitivity, count rate, scatter fraction, image quality, setup and reporting."
sources: ["NEMA NU 2 Performance Measurements of Positron Emission Tomographs (2018 edition; 2024 revision listed, confirm at https://www.nema.org)", "NEMA NU 1-2018 Performance Measurements of Gamma Cameras (confirm edition)", "https://www.nema.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NEMA performance testing

**Goal:** measure system performance with standardised phantoms and methods that are comparable between systems.

## NU 2 (PET) measurements (summary; use the document for details)
- **Spatial resolution:** point sources in air at specified positions, full width at half maximum and tenth maximum of reconstructed profiles.
- **Sensitivity:** a line source in successive aluminium sleeves, extrapolated to zero attenuation.
- **Scatter fraction, count losses and randoms:** a long uniform line source in a scatter phantom measured as activity decays, giving noise equivalent count rate (NECR) peak.
- **Accuracy of corrections** for count losses and randoms.
- **Image quality:** a body phantom with hot and cold spheres in warm background, giving contrast recovery and background variability.

Edition status: NEMA NU 2-2018 is shown by the ANSI store as revised by NU 2-2024 (gated: unconfirmed, source is paywalled or blocked); use the edition named in your contract.

## NU 1 (gamma cameras and SPECT)
- Intrinsic and system uniformity, spatial resolution, energy resolution, count rate performance and sensitivity, with defined sources.

## Practice
1. Use the edition and test procedure agreed in the contract or specification; note that results differ between editions.
2. Use calibrated activity (dose calibrator traceable) and record isotope, decay correction and timing.
3. Report acquisition and reconstruction parameters; results depend on them.
4. Repeat annually or after major service as part of QA (see imaging-acceptance-testing).

## Verify
- [ ] Phantom filling and source activity measured and documented.
- [ ] Edition and any deviations reported.
- [ ] Results compared with the manufacturer's specification.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
