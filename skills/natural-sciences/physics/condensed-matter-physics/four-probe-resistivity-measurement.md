---
id: natural-sciences.physics.condensed-matter-physics.four-probe-resistivity-measurement
name: four-probe-resistivity-measurement
category: natural-sciences
field: physics
product: condensed-matter-physics
tags: [condensed-matter-physics, resistivity, four-probe, four-terminal, kelvin-sensing, van-der-pauw, transport-measurement, electrical-transport, lock-in-amplifier, sr830, current-reversal, delta-mode, keithley-6221, nanovoltmeter, thermal-emf, contact-resistance, silver-paint, wire-bonding, ppms, cryostat, rho-vs-t, residual-resistivity-ratio, rrr, superconducting-transition, thin-film, single-crystal]
level: practitioner
status: gated
description: "Measure resistivity of a crystal or film with a four-probe/van der Pauw setup: contacts, current choice, reversal and lock-in, thermal EMFs, geometry factors."
sources: ["L. J. van der Pauw, Philips Research Reports 13 (1958) 1-9", "Keithley Low Level Measurements Handbook (7th ed.)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Four-probe resistivity measurement — getting ρ(T) you can trust

**Goal:** a resistivity-versus-temperature curve whose absolute value, shape and
features (transitions, kinks, upturns) are properties of the sample, not of the
contacts, wiring or electronics.

## 1. Why four probes
Two-terminal R includes lead and contact resistance (often ohms to kΩ on a
crystal). Pass current through the outer pair (I+, I−), measure voltage on the
inner pair (V+, V−) with a high-impedance meter: almost no current flows in the
voltage leads, so their resistance drops out. Everything below is about keeping
that assumption true.

## 2. Geometry choices
- **Bar (linear four-probe):** ρ = (V/I)·(w·t/L), L = distance between *voltage*
  contact centres, w width, t thickness. Thickness is usually the largest error
  (often ±10-20% on a small crystal (gated: unconfirmed, source is paywalled or blocked)) — measure it under a microscope at several points.
- **Van der Pauw:** arbitrary flat shape, uniform thickness, no holes, contacts small
  and on the *edge*. Measure R_AB,CD and R_BC,DA and solve
  exp(−πR₁t/ρ) + exp(−πR₂t/ρ) = 1 numerically (equal R's → ρ = πtR/ln2 ≈ 4.532·t·R; recomputed 4.5324, and the numerical solve for R₁ = 2, R₂ = 3, t = 1 gives ρ = 11.17).
  Check reciprocity: R_AB,CD should equal R_CD,AB within a few percent (gated: unconfirmed, source is paywalled or blocked); if not, a contact
  or the sample is bad.
- Anisotropic crystals: van der Pauw gives a geometric mean-ish value, not ρ_a or ρ_b.
  Use bars cut along the axes or the Montgomery method.

## 3. Contacts
- Typical options: silver paint/epoxy (DuPont 4929N, EpoTek H20E), sputtered or
  evaporated Au pads then wire, indium press, ultrasonic wire bonding for films.
- Aim for contact resistance low and *ohmic*: check I–V is linear through zero at
  base and room temperature. Rectifying contacts give current-dependent "ρ".
- Voltage contacts should be thin lines across the full width (bar) so they
  don't short a shape-dependent fraction of the current.
- Strain: epoxy cooled to 2 K can crack thin crystals or strain them enough to
  shift a transition. Silver paint is gentler; let solvent fully dry.

## 4. Excitation and readout
- **Pick current by power and heating:** keep I²R in the sample (and especially in the
  contacts) well below the cryostat's cooling power at base temperature. Start low
  (1–100 µA for metals, nA for insulators) and confirm V scales linearly with I.
- **DC with current reversal** (or delta mode, e.g. a current source + nanovoltmeter
  pair): V = (V₊ − V₋)/2 cancels thermoelectric EMFs (µV-level from Cu–solder–Ag
  junctions in a temperature gradient), which otherwise produce a fake offset.
- **AC lock-in:** low frequency (10–20 Hz, avoid mains harmonics), constant-current
  via a large series resistor (R_series ≫ R_sample + contacts). Check the phase: a
  growing quadrature signal means capacitive leakage or a failing contact.
- Twist each I and V pair; ground at one point only.

## 5. Running ρ(T)
- Sweep slowly (≤1–2 K/min below 20 K) and record both warming and cooling; hysteresis
  is either physics (first-order transition) or thermal lag between sensor and sample.
- Report RRR = ρ(300 K)/ρ(T→0) for metals — insensitive to geometry errors, a good
  sample-quality number.
- For superconductors, quote T_c by a stated criterion (onset, 50%, zero-resistance)
  and the current used; the transition broadens and shifts with current and field.

## Gotchas
- Negative or wildly temperature-independent "resistance": a voltage contact is open
  or the I and V leads are swapped.
- Resistance that drops step-wise at low T in a non-superconductor can be an indium
  or solder joint going superconducting (In ~3.4 K, Sn ~3.7 K, Pb ~7.2 K (gated: unconfirmed, source is paywalled or blocked)).
- Thin films on conducting substrates: the substrate may carry current (e.g. doped Si).
- *Uncertainty note:* the paint and epoxy brand examples are common lab choices, not
  a requirement; check cure temperature against what your sample tolerates.

## Verify
- [ ] V is linear in I (two or more currents agree) at the lowest temperature.
- [ ] Current-reversed or lock-in readings show no offset (V ≈ 0 at I = 0).
- [ ] Van der Pauw reciprocity holds within a few percent.
- [ ] Warming and cooling curves overlap, or the hysteresis is explained.
- [ ] Geometry uncertainty is propagated into the quoted ρ.
