---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.pet-detector-design
name: pet-detector-design
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [pet-detector, pet, spect, scintillator, lyso, bgo, sipm, time-of-flight, coincidence-window, depth-of-interaction]
level: advanced
status: gated
description: "Understand PET detector design: scintillator choice (LYSO, BGO), SiPM or PMT readout, crystal pitch, timing resolution and time-of-flight localisation, DOI and count-rate effects."
sources: ["Cherry, Sorenson and Phelps, Physics in Nuclear Medicine", "Lecomte, Novel detector technology for clinical PET (Eur J Nucl Med Mol Imaging 2009;36 Suppl 1:S69-S85)", "https://luxiumsolutions.com/radiation-detection-scintillators/crystal-scintillators/lyso-scintillation-crystals", "https://luxiumsolutions.com/radiation-detection-scintillators/crystal-scintillators/bgo-bismuth-germanate", "NEMA NU 2 Performance measurements of positron emission tomographs (confirm edition)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PET detector design

**Goal:** detect pairs of 511 keV annihilation photons with high efficiency, good energy, timing and spatial resolution.

## Detector elements
- **Scintillator crystals:** LYSO (density 7.1 g/cm3, light yield about 33 photons per keV, decay 36 ns, per the Luxium Solutions LYSO page) are the clinical standard for time-of-flight systems; BGO (density about 7.13 g/cm3, light yield roughly 8-10 photons per keV, decay about 300 ns, per the Luxium Solutions BGO page) has high stopping power but slower timing; others (GSO, LaBr3) exist. Values are approximate; check data sheets.
- **Crystal pitch:** typically 3-4 mm in clinical whole-body scanners, 1-2 mm in preclinical and brain systems; thickness around 20 mm balances sensitivity and depth-of-interaction blurring (gated: unconfirmed, source is paywalled or blocked).
- **Photodetectors:** photomultiplier tubes (PMT) in block detectors or **silicon photomultipliers (SiPM)** which are compact, magnetic-field tolerant (PET/MR) and have good timing. Light sharing and decoding maps identify crystals.

## Timing and TOF
- Coincidence timing window in the order of 3-6 ns (gated: unconfirmed, source is paywalled or blocked); coincidence timing resolution of modern SiPM systems is a few hundred picoseconds.
- **Time of flight** localises the event along the line of response: delta x = c delta t / 2. For 300 ps resolution that is about 4.5 cm (computed: 3e8 x 300e-12 / 2), which reduces noise in the image, especially for large patients.

## Other design issues
- **Depth of interaction (DOI):** parallax blur at the edge of the field of view; DOI-capable detectors or thin crystals reduce it.
- **Energy window** (for example 435-650 keV) balances scatter rejection and sensitivity.
- **Dead time and count rate:** pile-up in block detectors; characterise with NEMA count-rate tests.
- **Temperature control:** SiPM gain depends on temperature and bias.
- **Calibration:** crystal maps, energy, timing offsets, normalisation.

## Verify
- [ ] Measure energy resolution (typically 10-12% for LYSO block) and timing resolution on the module.
- [ ] Crystal identification map shows every crystal separated.
- [ ] NEMA tests for spatial resolution, sensitivity and count rate.
