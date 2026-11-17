---
id: natural-sciences.physics.biophysics.optical-trap-stiffness-calibration
name: optical-trap-stiffness-calibration
category: natural-sciences
field: physics
product: biophysics
tags: [biophysics, optical-tweezers, optical-trap, trap-stiffness, calibration, power-spectrum, power-spectral-density, lorentzian-fit, corner-frequency, equipartition, stokes-drag, faxen-correction, quadrant-photodiode, qpd, back-focal-plane-interferometry, brownian-motion, aliasing, single-molecule, force-spectroscopy, polystyrene-bead, silica-bead, tweezercalib, pico-newton, high-na-objective]
level: advanced
status: gated
description: "Calibrate an optical tweezers trap: QPD position detection, power-spectrum Lorentzian fit, equipartition and drag methods, corner frequency, surface and heating effects."
sources: ["K. Berg-Sørensen & H. Flyvbjerg, Power spectrum analysis for optical tweezers, Rev. Sci. Instrum. 75 (2004) 594", "K. C. Neuman & S. M. Block, Optical trapping, Rev. Sci. Instrum. 75 (2004) 2787"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optical trap stiffness calibration

**Goal:** know the trap stiffness κ (pN/nm) and the detector sensitivity β (nm/V)
so that a bead displacement becomes a force F = κx you can publish.

## 1. Setup assumptions
- High-NA objective (water or oil immersion, NA ≥ 1.2), trapping laser commonly
  1064 nm (low absorption in biological samples).
- Position detection by back-focal-plane interferometry on a quadrant photodiode
  (QPD) or position-sensitive detector, sampled fast (≥ 20–100 kHz) with an
  anti-aliasing filter.
- Beads of known diameter (polystyrene or silica, 0.5–2 µm) in a buffer of known
  viscosity, trapped several µm above the surface unless you correct for it.

## 2. Power-spectrum method (the workhorse)
A bead in a harmonic trap undergoing Brownian motion has a Lorentzian position
spectrum: P(f) = D / (2π²(f_c² + f²)) (two-sided; a one-sided estimate such as `scipy.signal.welch` is twice this, so a fit gave D about 2x too large until halved), with corner frequency f_c = κ / (2πγ),
γ = 6πηr (Stokes drag) and D = k_BT/γ.
1. Record ~10–60 s of bead position (in volts) at fixed laser power.
2. Compute the spectrum in blocks and average (Welch); bin logarithmically.
3. Fit the Lorentzian, ideally including aliasing and the detector filter (the
   Berg-Sørensen–Flyvbjerg approach; tweezercalib and similar packages implement it).
4. κ = 2πγ f_c. The fitted D_volts compared with the theoretical D gives
   β = √(D/D_volts) — the volts→nm conversion.
Typical: f_c of hundreds of Hz to a few kHz; κ ~0.01–1 pN/nm.

## 3. Cross-checks
- **Equipartition:** κ = k_BT / ⟨x²⟩ (needs β already known and no drift; insensitive
  to viscosity, sensitive to detector noise and calibration).
- **Drag (Stokes) method:** oscillate the stage (sinusoid or triangle) at known velocity
  v; F = γv; displacement x = γv/κ. Independent of β if you also calibrate position
  by moving a stuck bead through the beam.
- Agreement within ~10% between methods is a reasonable target.

## 4. Corrections that matter
- **Near a surface:** drag rises (Faxén's law). At a bead-centre height h = 2 r, Faxén's correction gives γ ≈ 1.39× bulk (computed; 1.23× if the gap, not the centre, is 2 r). Calibrate at the working height or apply the correction.
- **Heating:** absorption at the focus warms the focus by roughly 1 K per 100 mW at 1064 nm in water (about 8 K/W, Peterman et al. 2003; a common rule of thumb is 1 K/100 mW; other methods and wavelengths differ widely), lowering viscosity.
- **Linearity:** QPD response is linear only over a limited range (gated: unconfirmed, source is paywalled or blocked); map the full response for your bead and stay inside it.
- **Stiffness scales with power:** calibrate at the power you use, or verify κ ∝ P.
- **Spherical aberration** with oil objectives reduces stiffness deeper into
  aqueous samples; calibrate at the actual depth.

## Gotchas
- Low-frequency drift and mechanical vibrations (pumps, fans) show as spikes or a
  rising floor below ~10 Hz; exclude from the fit window and fix the source.
- Two beads in the trap or a bead stuck to the surface gives nonsense f_c.
- Parasitic filtering by silicon photodiodes at 1064 nm (slow response, penetration
  depth) distorts high frequencies; fit with a filter term or use a dedicated diode.
- *Uncertainty note:* numerical ranges above are typical for µm beads and moderate
  power; your system's values depend on optics, bead index and size.

## Verify
- [ ] Spectrum fit residuals are flat across the window (no systematic curvature).
- [ ] κ from power spectrum and drag/equipartition agree within ~10%.
- [ ] Calibration done at the same height, power and buffer as the experiment.
- [ ] β derived and displacements stay within the detector's linear range.
