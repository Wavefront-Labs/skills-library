---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.ppg-motion-artifact
name: ppg-motion-artifact
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [ppg-motion, motion-artifact, photoplethysmography, adaptive-filter, wearable-ppg]
level: advanced
status: gated
description: "Reduce motion artefact in photoplethysmography: sensor coupling, wavelength choice, accelerometer reference, adaptive filtering and spectral tracking, and failure detection."
sources: ["Journal literature on PPG motion artefact reduction in wearables (confirm citations)", "ISO 80601-2-61 pulse oximeter equipment (confirm edition)", "https://pubmed.ncbi.nlm.nih.gov/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PPG motion artefact

**Goal:** keep heart rate or SpO2 estimates valid during movement, or flag them as unreliable.

## Causes
- Relative motion between sensor and skin changes the optical path and coupling; blood movement from limb acceleration modulates the signal; ambient light leaks.
- Motion energy overlaps the heart-rate band (0.5 to 4 Hz, which is 30 to 240 beats per minute), so simple filtering fails.

## Mitigation
1. **Mechanical:** stable contact pressure, light shielding, moderate-adhesion straps; green LEDs often have better signal for wrist heart rate (higher absorption by haemoglobin, shallow depth), while red and infrared are needed for SpO2 (gated: unconfirmed, source is paywalled or blocked).
2. **Reference sensor:** a 3-axis accelerometer (and optionally gyroscope) with adaptive noise cancellation (least mean squares) or reference-based decomposition.
3. **Spectral methods:** track the heart-rate peak across time (continuity constraint), avoid locking onto cadence harmonics.
4. **Signal quality index:** reject or flag segments where waveform shape, perfusion index or motion is poor; show no value rather than a wrong one.
5. Sampling (about 25 to 100 Hz is common (gated: unconfirmed, source is paywalled or blocked)) and LED duty cycle balance power and fidelity.

## Verify
- [ ] Tested during standard activity profiles (walking, running, arm swing, typing) against ECG reference.
- [ ] Error statistics reported per activity.
- [ ] Unreliable output suppressed with measured false-valid rate.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
