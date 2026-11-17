---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.pulsed-wave-doppler
name: pulsed-wave-doppler
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [pulsed-wave-doppler, doppler, ultrasound-doppler, aliasing, prf, nyquist-limit, doppler-angle, wall-filter, spectral-doppler]
level: practitioner
status: draft
description: "Use pulsed-wave Doppler correctly: Doppler equation, PRF and aliasing limit, range-velocity trade-off, angle correction, wall filter and sample volume setup."
sources: ["Szabo, Diagnostic Ultrasound Imaging: Inside Out (Doppler chapters)", "Evans and McDicken, Doppler Ultrasound: Physics Instrumentation and Signal Processing", "IEC 61157 Standard means for the reporting of the acoustic output of medical diagnostic ultrasonic equipment (confirm edition)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Pulsed-wave Doppler

**Goal:** measure blood velocity at a chosen depth without aliasing and with an accurate angle.

## Doppler equation
fd = 2 f0 v cos(theta) / c, with transmit frequency f0, velocity v, beam-to-flow angle theta, and c about 1540 m/s in tissue.
Example: f0 = 3 MHz, v = 1 m/s, theta = 60 degrees gives fd of about 1.95 kHz.

## PRF and aliasing
- The sampling rate is the pulse repetition frequency (PRF). The Nyquist limit is fd max = PRF / 2, so v max = c PRF / (4 f0 cos theta).
- The depth limit is PRF <= c / (2 d), where d is the sample depth. Deep vessels need low PRF and so a low aliasing velocity: the **range-velocity ambiguity**.
- Fixes for aliasing: raise PRF (scale), shift the baseline, use a lower transmit frequency, increase the Doppler angle (decreases cos), use high-PRF mode (multiple pulses in flight), or switch to continuous-wave Doppler (no range gating).

## Controls to set
1. **Sample volume** size and position in the vessel lumen (not the wall).
2. **Angle correction** to the flow direction; keep angle at or below about 60 degrees as error grows steeply at high angles (error in v ~ tan(theta) times angle error).
3. **Wall filter** (high-pass) to remove low-frequency wall motion; set low enough not to remove slow venous flow.
4. **Gain** just below the noise floor; **baseline** to centre the spectrum; sweep speed.
5. Acoustic output: Doppler modes raise intensity; follow the ALARA principle and display thermal and mechanical indices (see acoustic-output-safety).

## Verify
- [ ] Flow phantom or string phantom with known velocity within accuracy specification.
- [ ] Check the maximum measurable velocity in each mode and depth.
- [ ] Angle correction does not exceed recommended limit.
