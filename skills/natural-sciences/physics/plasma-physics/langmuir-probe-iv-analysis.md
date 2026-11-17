---
id: natural-sciences.physics.plasma-physics.langmuir-probe-iv-analysis
name: langmuir-probe-iv-analysis
category: natural-sciences
field: physics
product: plasma-physics
tags: [plasma-physics, plasma-diagnostics, langmuir-probe, single-probe, double-probe, i-v-characteristic, iv-curve, electron-temperature, plasma-density, plasma-potential, floating-potential, ion-saturation-current, electron-saturation, bohm-criterion, sheath, debye-length, rf-compensation, eedf, druyvesteyn, low-temperature-plasma, glow-discharge, icp, rf-plasma, tokamak-edge, oml-theory]
level: advanced
status: gated
description: "Take and analyse a single Langmuir probe I-V curve: probe design, sweep, ion saturation, electron temperature from the exponential region, density and plasma potential."
sources: ["F. F. Chen, Langmuir Probe Diagnostics, IEEE-ICOPS mini-course (2003)", "I. H. Hutchinson, Principles of Plasma Diagnostics (2nd ed.), ch. 3", "R. L. Merlino, Understanding Langmuir probe current-voltage characteristics, Am. J. Phys. 75 (2007) 1078"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Langmuir probe I–V analysis

**Goal:** from one swept-voltage probe trace, extract electron temperature T_e,
density n, floating potential V_f and plasma potential V_p, and know when the
numbers are trustworthy.

## 1. The probe
- A small electrode (tungsten or tantalum wire, ~0.1–0.5 mm diameter, few mm long,
  or a planar disc) in a ceramic/quartz sleeve, inserted where you want local values.
- Size relative to the Debye length λ_D sets the theory: probe radius ≫ λ_D →
  thin-sheath (collection area ≈ probe area); radius ≲ λ_D → orbital-motion-limited
  (OML) collection. Compute λ_D = √(ε₀kT_e / n e²) from a first estimate.
- Keep the probe small enough not to perturb the plasma (its electron saturation
  current must be small compared with what the discharge anodes carry).

## 2. Taking the sweep
- Sweep from well negative (ion saturation, e.g. −50 V) to past V_p; measure current
  over a shunt resistor or with a transimpedance amplifier.
- **RF plasmas:** the plasma potential oscillates; an uncompensated probe gives a
  smeared curve and an overestimated T_e. Use RF compensation (a floating reference
  electrode plus self-resonant chokes at the drive frequency and 2nd harmonic).
- Average many sweeps; clean the probe between runs (bias it strongly positive
  briefly, or ion-bombard it) — contamination layers distort the curve, often as
  hysteresis between up- and down-sweeps.

## 3. Analysis, step by step
1. **Ion saturation:** fit the far-negative region (often slightly sloped) and
   extrapolate across; subtract it from the total to get the electron current I_e.
2. **Floating potential:** where total I = 0.
3. **Electron temperature:** in the transition (retarding) region, I_e ∝ exp(e(V−V_p)/kT_e),
   so plot ln I_e vs V: the slope is e/kT_e. A straight line means a Maxwellian; two
   slopes mean two electron populations (common in low-pressure RF/ICP discharges).
4. **Plasma potential:** the knee where ln I_e stops rising exponentially — best
   taken as the peak of dI/dV (or the zero of d²I/dV²), or the intersection of the
   transition and saturation fits.
5. **Density:** from the ion saturation current with the Bohm criterion,
   I_is ≈ 0.61 · n · e · A (0.61 = exp(-1/2) = 0.6065, recomputed) · √(kT_e / M_i) (thin sheath, M_i ion mass), or from electron
   saturation at V_p, I_es = ¼ n e A √(8kT_e/πm_e). The two often disagree by ×2
   or more — report the method used.
6. **EEDF (optional):** the Druyvesteyn method uses d²I/dV² to give the electron
   energy distribution; needs clean, well-smoothed data.

## Gotchas
- Wrong ion mass (molecular ions in a molecular gas, mixtures) shifts n by √(mass ratio).
- Magnetised plasmas: electron collection across field lines is suppressed, and
  the electron-saturation branch is unreliable; rely on the ion side.
- Probe heating to incandescence at high current changes area and emits electrons.
- Collisional plasmas (mean free path ≲ sheath size) violate the collisionless theory.
- *Uncertainty note:* the 0.61 Bohm factor and which theory (thin sheath vs OML vs
  ABR) applies are approximations; expect ~±50% absolute uncertainty on n and
  ~±20% on T_e from a single probe even when done carefully.

## Verify
- [ ] ln I_e vs V has a clear linear region spanning at least ~2 kT_e/e.
- [ ] Up- and down-sweeps overlap (no contamination hysteresis).
- [ ] λ_D computed and the sheath theory used is consistent with probe size.
- [ ] V_p > V_f by roughly a few kT_e/e (computed from (kT_e/e)·½·ln(M_i/2πm_e): about 4.7 for argon, 2.8 for hydrogen, 3.5 for helium; larger for heavier ions).
- [ ] Density from ion and electron sides compared and the discrepancy reported.
