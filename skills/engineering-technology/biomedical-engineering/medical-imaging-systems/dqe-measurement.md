---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.dqe-measurement
name: dqe-measurement
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [detective-quantum-efficiency, digital-radiography, dqe, dqe-measurement, rqa5, iec-62220-1, nnps, flat-panel-detector]
level: advanced
status: gated
description: "Measure detective quantum efficiency of a digital X-ray detector: RQA5 beam, linearisation, edge MTF, flat-field NNPS, incident photon fluence and IEC 62220-1 reporting."
sources: ["IEC 62220-1-1:2015 Medical electrical equipment - Characteristics of digital X-ray imaging devices - Part 1-1: Determination of the detective quantum efficiency - Detectors used in radiographic imaging (https://webstore.iec.ch/en/publication/21937)", "On the robustness of detective quantum efficiency within the limits of IEC 61267 RQA standard radiation qualities (https://pmc.ncbi.nlm.nih.gov/articles/PMC10997859/)", "Dobbins, Image quality metrics for digital systems (Handbook of Medical Imaging, SPIE)", "Cunningham and Shaw, Signal-to-noise optimization of medical imaging systems (J Opt Soc Am A 1999;16:621)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DQE measurement

**Goal:** report the detector's frequency-dependent efficiency at transferring signal-to-noise ratio, DQE(f), comparable across devices.

## Definition
DQE(f) = MTF(f)^2 / (q x NNPS(f)), where q is the incident photon fluence (photons per mm2) at the detector, MTF the presampling modulation transfer function and NNPS the normalised noise power spectrum (NPS divided by the squared mean large-area signal, after linearisation).

## Procedure
1. **Beam:** RQA5 radiation quality (IEC 61267; about 70 kV tube voltage with 21 mm of aluminium added filtration (gated: unconfirmed, source is paywalled or blocked)) with specified HVL; verify with a calibrated dosimeter.
2. **Incident air kerma:** measure with a calibrated chamber at the detector plane (corrected for back-scatter and distance); fluence q follows from kerma (roughly 30,000 photons/mm2 per microgray for RQA5; a 2024 open-access study reports 29 921 with 95% interval 29 516 to 30 243, about 0.8% from the IEC 62220-1 value; use the value in the standard (gated: unconfirmed, source is paywalled or blocked)).
3. **Linearise:** acquire a series of flat-field images at several kerma levels and fit the detector response; convert pixel values to a linear (kerma-proportional) scale.
4. **MTF:** image a slightly angled edge device (tungsten or steel edge), compute the edge spread function, differentiate and Fourier transform, with oversampling from the angle.
5. **NNPS:** acquire many uniform exposures (enough ROIs for a stable estimate), detrend with a 2D polynomial, compute the 2D NPS and take the radial or axis slices per the standard; normalise.
6. Combine with kerma values and plot DQE(f) up to Nyquist; commonly quoted as DQE(0) and DQE at 1, 2, 3 cycles/mm.

## Gotchas
- Detector corrections (gain, offset, defect) must be on as in clinical use, with a statement of which.
- Grid and anti-scatter hardware must be removed.
- Incorrect kerma or beam quality changes DQE directly (DQE scales with 1/q).
- Lag and ghosting require waiting and dark-image checks.

## Verify
- [ ] DQE(0) in plausible range for the detector type (scintillator CsI flat panels are typically higher than amorphous-selenium or Gd2O2S at low frequency).
- [ ] Repeat measurement within a few percent.
- [ ] Beam and dosimetry traceability recorded.
