---
id: engineering-technology.automotive-vehicle-engineering.nvh.sunroof-buffeting-control
name: sunroof-buffeting-control
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [buffeting, sunroof-buffeting, wind-throb, helmholtz-resonance, shear-layer, wind-deflector, rossiter, low-frequency-pressure, window-buffeting, wind-noise]
level: practitioner
status: gated
description: "Control sunroof and open-window buffeting: Helmholtz resonance and shear-layer coupling, estimating the frequency, wind deflector design and tunnel or road verification."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "Aeroacoustics references for cavity and open-roof flow resonance"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Sunroof buffeting control

## 1. Phenomenon
With the sunroof (or a rear window) open at moderate speed, a strong low-frequency pressure pulsation (felt as a throb, often 10-30 Hz (gated: unconfirmed, source is paywalled or blocked)) fills the cabin. Shear-layer vortices shed from the leading edge of the opening are convected across it and strike the rear edge, producing pressure pulses; when their frequency matches the cabin's Helmholtz mode, the cabin acts as a resonator and amplifies.

## 2. Estimate the frequencies
- **Cabin Helmholtz resonance:** f_H = (c / (2 pi)) x sqrt(A / (V x L_eff)), with c speed of sound, A opening area, V cabin volume, L_eff effective neck length (physical length plus an end correction of about 0.3 x the hydraulic diameter of the opening, per the Wikipedia Helmholtz resonance article). Computed example: A = 0.15 m2, V = 3 m3, L_eff = 0.17 m gives 30 Hz.
- **Shear layer excitation:** Rossiter-type frequencies f = (n - alpha) U / (L (1/kappa + M)), where L opening length, U flow speed, n integer, M Mach number, alpha and kappa empirical constants (this is Rossiter's formula; take constants from the literature for your geometry). Matching between f_H and the shear-layer frequency at a particular speed (and its multiples) gives a speed range with a peak.
Use these only as screening estimates; confirm with measurement.

## 3. Countermeasures
- **Wind deflector** at the front edge: breaks and disorganises the shear layer vortices or lifts the shear layer above the opening; serrated, perforated or mesh deflectors and slanted edges reduce coherence. Height and angle are tuned by tests.
- **Partial opening positions:** program the stops (for example a vent position or a short-opening stop) at sizes where buffeting is weak.
- **Rear glass lowering** or opening both front and rear windows slightly to change the resonance.
- **Rear-edge geometry** (ramp, slots) to reduce impingement.
- Cabin volume and absorption adjustments are secondary.

## 4. Test and metrics
Wind tunnel and road tests at speeds from about 40 to 140 km/h (a typical sweep, not a standard) in steps with the sunroof at different opening positions, microphones at the ear positions (dB linear or dB(C) because it is low frequency), seat positions, crosswind sensitivity. Targets: absolute low-frequency SPL limit and subjective rating at relevant speeds; also check wind noise at the vent position. CFD (transient, scale-resolving) can predict the peak with careful validation.

## Verify
- [ ] Helmholtz and shear-layer frequencies estimated, then measured.
- [ ] Deflector design swept over height and angle at multiple speeds.
- [ ] Partial-opening positions tested.
- [ ] Rear-window open cases checked.
