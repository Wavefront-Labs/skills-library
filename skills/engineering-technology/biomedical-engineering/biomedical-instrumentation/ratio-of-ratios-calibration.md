---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.ratio-of-ratios-calibration
name: ratio-of-ratios-calibration
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [ratio-of-ratios, pulse-oximetry, spo2, photoplethysmography, calibration-curve, desaturation-study, red-infrared]
level: advanced
status: gated
description: "Derive pulse oximeter SpO2 from the ratio of ratios, build the calibration from controlled desaturation data, and know what limits accuracy at low saturation."
sources: ["Webster (ed.), Design of Pulse Oximeters", "ISO 80601-2-61 Particular requirements for basic safety and essential performance of pulse oximeter equipment (confirm edition)", "FDA guidance on pulse oximeters for premarket notification (current text on fda.gov)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ratio-of-ratios calibration

**Goal:** turn red and infrared photoplethysmograms into an SpO2 estimate with a calibration backed by arterial blood data.

Every figure in this skill (wavelengths, SpO2 = 110 - 25 R, methaemoglobin reading near 85%) is (gated: unconfirmed, source is paywalled or blocked); the 70-100% ARMS evaluation range matches FDA 2013 pulse oximeter guidance.

## Signal chain
- Two LEDs, red near 660 nm and infrared near 940 nm (905-940 nm in some devices), time-multiplexed into one photodiode; ambient light measured in a dark slot and subtracted.
- For each wavelength compute the pulsatile (AC) and non-pulsatile (DC) parts over a beat.
- **R = (AC_red / DC_red) / (AC_ir / DC_ir)**.
- Lambert-Beer theory suggests R relates to saturation, but tissue scattering means R is mapped empirically. A rough linear form SpO2 = 110 - 25 R is often used in teaching; real devices use a measured nonlinear curve, usually stored as a table.

## Calibration procedure
1. In an accredited laboratory with ethics approval, healthy volunteers breathe controlled hypoxic gas mixtures while arterial blood is sampled and measured by a CO-oximeter (SaO2), plateau by plateau down to about 70% saturation (lower values are not ethically obtained in volunteers).
2. Record R at each plateau and fit R-to-SaO2 (polynomial or table), by device design and sensor.
3. Report accuracy as ARMS (root-mean-square error) against SaO2 over 70-100%. Regulators and standards require limits of a few percentage points, with the values depending on the edition and region; confirm in the current FDA guidance and ISO 80601-2-61.

## Limits
- Below 70% the curve is extrapolated, not measured.
- Dyshaemoglobins (carboxy- and methaemoglobin) are read as if oxygenated or as roughly 85% for methaemoglobin; two-wavelength devices cannot separate them.
- Low perfusion, motion and nail polish reduce accuracy; skin pigmentation can bias readings (see pulse-oximeter-skin-tone-bias).

## Verify
- [ ] Ambient-light rejection tested with room and sunlight.
- [ ] Calibration curve checked for monotonic behaviour.
- [ ] Accuracy study design reviewed against current guidance, including a range of skin tones.
