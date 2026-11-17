---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.color-flow-imaging
name: color-flow-imaging
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [color-flow, colour-doppler, autocorrelation, ensemble-length, wall-filter]
level: advanced
status: verified
description: "Implement and evaluate colour flow imaging: autocorrelation velocity estimation, pulse repetition frequency and aliasing, ensemble length, wall filters and angle dependence."
sources: ["Kasai et al., Real-time two-dimensional blood flow imaging using an autocorrelation technique (IEEE Trans Sonics Ultrason 1985;32:458-464)", "Szabo, Diagnostic Ultrasound Imaging: Inside Out", "https://www.ieee-uffc.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Colour flow imaging

**Goal:** estimate mean blood velocity in a 2D region in real time and know what limits accuracy.

## Method
1. For each line, transmit a packet (ensemble) of pulses at pulse repetition frequency (PRF), the ensemble length is system dependent (a handful to a dozen or so pulses); receive and demodulate to complex (I and Q) data at each depth.
2. **Wall filter:** high-pass along the slow-time (pulse-to-pulse) direction removes the strong, slow signals from vessel walls and tissue (clutter).
3. **Autocorrelation (Kasai):** the phase of the lag-one autocorrelation of slow-time samples gives the mean Doppler frequency; velocity = (c times PRF / (4 pi f0 cos theta)) times that phase, where c is sound speed, f0 transmit frequency and theta the beam-flow angle.
4. Colour-code velocity direction toward or away from the probe, with variance or power for reliability.

## Limits
- **Aliasing:** unambiguous velocity range is the Nyquist velocity = c times PRF / (4 f0 cos theta). Example: c = 1540 m/s, PRF = 5 kHz, f0 = 5 MHz and theta = 60 degrees gives 0.77 m/s (computed: 1540 x 5000 / (4 x 5e6 x cos 60 deg) = 0.770). Increase PRF, lower f0 or increase angle to avoid aliasing; PRF is limited by depth (round-trip time).
- **Angle dependence:** no signal at 90 degrees; velocity accuracy requires an angle correction.
- **Ensemble length** trades velocity precision, frame rate and sensitivity to slow flow.
- Blooming (colour overwrite), motion clutter and low-flow sensitivity affect interpretation.

## Verify
- [ ] Flow phantom velocity versus estimated velocity over the PRF range.
- [ ] Aliasing limit confirmed with calculation and test.
- [ ] Acoustic output remains in limits with the chosen PRF and ensemble.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
