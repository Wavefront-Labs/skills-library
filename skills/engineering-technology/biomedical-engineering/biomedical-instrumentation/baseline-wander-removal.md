---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.baseline-wander-removal
name: baseline-wander-removal
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [baseline-wander, signal-conditioning, biomedical-filters, ecg-filtering, high-pass-filter, median-filter, st-segment, zero-phase]
level: practitioner
status: draft
description: "Remove baseline wander from ECG and other biosignals: sources, high-pass limits, linear-phase and zero-phase filters, median and spline methods and effects on ST segments."
sources: ["Sornmo and Laguna, Bioelectrical Signal Processing in Cardiac and Neurological Applications", "Kligfield et al., Recommendations for the standardization and interpretation of the electrocardiogram Part I (Circulation 2007)", "IEC 60601-2-25 and IEC 60601-2-27 (ECG requirements; confirm editions)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Baseline wander removal

**Goal:** remove slow drift without distorting the ST segment and other diagnostic features.

## Sources
Respiration (about 0.15-0.5 Hz), body movement, electrode-skin potential changes (sweat, motion), poor contact. Drift often has amplitude much larger than the ST segment.

## Options
- **High-pass filter:** diagnostic ECG recommendations call for a low-frequency cutoff of 0.05 Hz (or 0.67 Hz with linear phase) to avoid ST distortion; monitoring uses 0.5 Hz or higher, accepting ST distortion; check the current guideline text. A causal IIR high-pass at 0.5 Hz causes phase distortion around the QRS and ST (the ST segment can be depressed or elevated artificially).
- **Zero-phase (forward-backward) filtering:** eliminates phase distortion offline; unavailable in real time without delay.
- **Median filter subtraction:** estimate baseline with a median filter of about 200 ms (to remove QRS and P) followed by about 600 ms (to remove T), subtract from the signal. Works offline and approximately online with delay.
- **Cubic spline through isoelectric knots:** use the PR segment or TP segment points as knots; follows drift while preserving ST, depends on correct knot detection.
- **Wavelet or empirical mode decomposition:** remove low-frequency approximation; flexible, more complex.
- **Adaptive filters** driven by a motion reference (accelerometer).

## Design choices
1. Choose by use: diagnostic (preserve ST: low cutoff, linear phase or offline), monitoring (robust: higher cutoff), ambulatory (adaptive plus electrode design).
2. Reduce wander at the source: better electrodes, gel, strain relief, skin preparation.
3. Ensure the ADC range does not saturate during motion.

## Verify
- [ ] Test with the standard's step or ST test signals and record distortion.
- [ ] Compare ST measurements before and after on annotated recordings (for example public ECG databases).
- [ ] Group delay measured for real-time filters.
