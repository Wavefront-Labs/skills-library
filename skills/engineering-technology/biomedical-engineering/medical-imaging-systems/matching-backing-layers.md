---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.matching-backing-layers
name: matching-backing-layers
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [matching-layer, ultrasound-transducer, piezoelectric, backing-layer, quarter-wave, acoustic-impedance, fractional-bandwidth]
level: advanced
status: gated
description: "Design acoustic matching and backing layers for ultrasound transducers: quarter-wave thickness, impedance values for one and two layers, backing trade-offs and bandwidth."
sources: ["Desilets, Fraser and Kino, The design of efficient broad-band piezoelectric transducers (IEEE Trans Sonics Ultrason 1978;25:115-125)", "Szabo, Diagnostic Ultrasound Imaging: Inside Out", "Kino, Acoustic Waves: Devices Imaging and Analog Signal Processing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Matching and backing layers

**Goal:** couple a high-impedance piezoelectric element efficiently into soft tissue and shape the pulse for wide bandwidth.

## Why
Piezoceramic (PZT) has acoustic impedance around 30-35 MRayl; tissue around 1.5 MRayl (gated: unconfirmed, source is paywalled or blocked). Direct coupling reflects most energy and rings long. Matching layers step the impedance and backing damps the rear.

## Matching layers
- **Quarter-wave thickness:** t = lambda / 4 = c / (4 f) at centre frequency, using the layer's own sound speed.
- **Single layer:** Z_m = sqrt(Z_p x Z_t). With Z_p = 33 and Z_t = 1.5 MRayl, Z_m is about 7 MRayl (computed: 7.04).
- **Two layers (Desilets):** Z1 = Z_p^(4/7) Z_t^(3/7) about 8.8 MRayl (computed: 8.77) and Z2 = Z_p^(1/7) Z_t^(6/7) about 2.3 MRayl (computed: 2.33) for the same values (the 4/7 and 3/7 exponents are the Desilets two-layer design (gated: unconfirmed, source is paywalled or blocked)); typical real materials are loaded epoxies (outer layer a polymer such as a low-impedance epoxy or parylene).
- Layers must be thin and uniform (microns); thickness error shifts the centre frequency.
- Example: layer sound speed 2500 m/s at 3.5 MHz gives quarter wavelength 0.18 mm.

## Piezoelectric element
Half-wavelength resonance: t_p = c_p / (2 f) (about 0.57 mm for c_p 4000 m/s at 3.5 MHz); kerfs to form arrays and composites reduce impedance and improve coupling.

## Backing
- High-attenuation, impedance-matched backing (epoxy loaded with tungsten or similar) damps ringing to shorten pulses and widen bandwidth, at the cost of sensitivity.
- Less backing (air-backed) gives high sensitivity and narrow bandwidth, as in therapy transducers.
- Fractional bandwidth targets for imaging are often 60-100% at -6 dB (gated: unconfirmed, source is paywalled or blocked).

## Lens
A focusing lens (silicone rubber, with low sound speed) sets elevation focus and adds attenuation and mismatch; include it in the stack model.

## Verify
- [ ] Simulate the stack with a KLM or finite-element model before building.
- [ ] Measure pulse-echo response: centre frequency, -6 dB bandwidth and sensitivity.
- [ ] Check electrical impedance matched to the cable and front-end.
