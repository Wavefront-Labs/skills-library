---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.automatic-exposure-control
name: automatic-exposure-control
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [automatic-exposure-control, ct-dose, ctdi, aec, tube-current-modulation, exposure-index, dose-optimization, ionization-chamber]
level: advanced
status: gated
description: "Understand and test automatic exposure control in radiography, mammography and CT: sensor placement, density setting, tube current modulation and noise targets."
sources: ["IEC 60601-2-54 Particular requirements for the basic safety and essential performance of X-ray equipment for radiography and radioscopy (2022 edition is current: https://webstore.iec.ch/en/publication/69988)", "IEC 62494-1:2008 https://webstore.iec.ch/en/publication/7107", "Bushberg et al., The Essential Physics of Medical Imaging", "McCollough et al., CT dose index and patient dose: they are not the same thing (Radiology 2011;259:311-316)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Automatic exposure control (AEC)

**Goal:** consistent image quality across patient sizes with the lowest dose consistent with the diagnostic task.

## Radiography and mammography
- Ionisation chambers or solid-state detectors placed behind the grid and before the detector measure the dose; the generator terminates the exposure at a set signal ("backup time" protects against failure).
- Controls: **density setting** (steps typically each change about 20-25% in dose (gated: unconfirmed, source is paywalled or blocked)), field selection (left, centre, right cells), and a minimum response time.
- Calibrations: sensor response versus kVp, patient thickness (phantom steps), and receptor type; the target is constant detector dose (or exposure index) across kVp and thickness within tolerance (commonly about +/- 10-20% across thickness (gated: unconfirmed, source is paywalled or blocked); check the protocol).
- Digital systems report an **exposure index** which should be monitored per IEC 62494-1 (Medical electrical equipment - Exposure index of digital X-ray imaging systems - Part 1: Definitions and requirements for general radiography; edition 1.0, 2008, per the IEC webstore).

## CT tube current modulation
- **Angular (xy)** and **longitudinal (z)** modulation adjusts tube current based on patient attenuation from the scout image (and in real time), so that image noise matches a target set by the operator ("noise index" or "reference mAs" depending on vendor).
- Larger patient parts get more mA; small patients get less. Settings include minimum and maximum mA, thresholds, and organ-dose modulation options that reduce current over superficial organs.
- Beam energy selection (automatic kV) can also adapt.

## Testing
1. Scan or expose water, acrylic or anthropomorphic phantoms of different sizes; record the resulting mA or mAs and noise (CT) or detector dose (radiography).
2. Check that the dose changes with size as intended and image noise stays within the target.
3. Check behaviour with off-centre positioning (CT AEC is sensitive to centring and can raise dose).
4. Confirm backup timers and safety limits.

## Gotchas
- Metal implants or contrast confuse AEC sensors and scout-based modulation.
- Incorrect centring or the wrong cell selection yields over- or underexposure.

## Verify
- [ ] Image quality (noise, contrast-to-noise) stable across phantom sizes.
- [ ] Dose indices (CTDIvol, DLP) reported and compared with diagnostic reference levels.
- [ ] Documented tolerances and acceptance records.
