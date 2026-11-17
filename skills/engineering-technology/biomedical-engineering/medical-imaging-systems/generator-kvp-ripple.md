---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.generator-kvp-ripple
name: generator-kvp-ripple
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [kvp-ripple, x-ray-tube, x-ray-generation, high-frequency-generator, tube-voltage, waveform, kvp-accuracy, constant-potential]
level: practitioner
status: gated
description: "Understand X-ray generator waveforms and kVp ripple: single-phase, three-phase and high-frequency, effect on output and contrast, and how to measure kVp and ripple."
sources: ["Bushberg et al., The Essential Physics of Medical Imaging (X-ray generators)", "IEC 61223-3-8:2024 Evaluation and routine testing in medical imaging departments - Part 3-8: Acceptance and constancy tests - Imaging performance of X-ray equipment for radiography and radioscopy (https://webstore.iec.ch/en/publication/64680); the older IEC 61223-3-1:1999 was withdrawn on 2010-10-07", "Curry, Dowdey and Murry, Christensen's Physics of Diagnostic Radiology"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Generator waveforms and kVp ripple

**Goal:** know how the tube voltage waveform affects exposure, image quality and test results.

## Waveform types
- **Single-phase** (half or full wave rectified): voltage varies from zero to peak each half cycle, so ripple is 100%; much of the exposure occurs at low kV that adds dose but little image.
- **Three-phase, six-pulse:** about 13% ripple; **twelve-pulse:** about 3-4% (gated: unconfirmed, source is paywalled or blocked).
- **High-frequency (inverter) generators** (the modern default): the voltage is nearly constant, with ripple typically a few percent or less; short exposures are reproducible.
- **Constant potential** for specialist systems.

## Effect
- Lower ripple raises the average photon energy at the same peak kVp, so output (air kerma per mAs) and penetration rise, and the same technique setting gives different dose and contrast on different generators.
- Because kVp refers to peak voltage, compare machines using measured kVp and HVL, not the nominal setting.

## Measurement
1. Use a non-invasive kVp meter (multi-detector with filtration ratios) placed in the beam at the specified distance; run repeated exposures at several kVp, mA and time values.
2. For waveform and ripple use a kV divider on the HV cable or a meter with waveform display (invasive, requires service access).
3. Compare to the tolerance (commonly plus or minus 5% for kVp accuracy in acceptance tests (gated: unconfirmed, source is paywalled or blocked); confirm the standard or protocol).
4. Test reproducibility: standard deviation or coefficient of variation of output over repeated exposures (commonly within 5% or tighter in the protocols).

## Gotchas
- Very short exposures (below 20 ms) may not reach set kV on some generators; check the rise time.
- Meter calibration depends on filtration and waveform.

## Verify
- [ ] kVp accuracy and ripple measured at several settings.
- [ ] Output linearity per mAs and per time within tolerance.
- [ ] Results recorded with generator type, meter model and calibration.
