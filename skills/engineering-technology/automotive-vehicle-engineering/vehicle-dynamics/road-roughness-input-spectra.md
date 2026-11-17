---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.road-roughness-input-spectra
name: road-roughness-input-spectra
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [road-roughness-psd, road-roughness, iso-8608, psd, road-profile, ride-input]
level: practitioner
status: gated
description: "Generate ride-simulation road inputs from ISO 8608 roughness classes using PSD, convert from spatial to time frequency, and synthesise a profile."
sources:
  - "ISO 8608 road surface profiles classification, confirm edition"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Road roughness input spectra

1. ISO 8608 classifies road profile displacement PSD `Gd(n) = Gd(n0)*(n/n0)^(-w)`, n spatial frequency (cycles/m), reference n0 = 0.1 cycles/m, waviness w about 2. Class A (smooth) to H (very rough); class boundaries set `Gd(n0)` ranges (class A below about 32e-6 m^3; each class steps by a factor of 4 in PSD). Confirm values in the standard (class limits, n0, w and the 4x step per class:gated: unconfirmed, source is paywalled or blocked; the factor-of-4 arithmetic and sqrt(4)=2 RMS step were computed).
2. Convert to time: for speed V, `f = n*V`, `Gd(f) = Gd(n)/V`.
3. Synthesis: sum of sines `z(x) = sum sqrt(2*Gd(n_i)*dn)*cos(2*pi*n_i*x + phi_i)` with random phases `phi_i`; band from low cut-off (about 0.01 c/m) to high cut-off (about 10 c/m).
4. Left and right tracks have coherence; use a coherence function or an offset to make track pair realistic.
5. Drive the quarter-car or full-vehicle model and compare body RMS acceleration against the measured vehicle.

**Gotchas:** velocity or acceleration PSDs: convert correctly; low cut-off sets drift.

## Verify
- [ ] Synthesised profile PSD reproduces the target class on log-log axes.
- [ ] Simulated RMS acceleration roughly doubles per class step (PSD steps by 4x).
