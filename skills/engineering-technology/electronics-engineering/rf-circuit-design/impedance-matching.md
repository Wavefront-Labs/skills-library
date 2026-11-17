---
id: engineering-technology.electronics-engineering.rf-circuit-design.impedance-matching
name: impedance-matching
category: engineering-technology
field: electronics-engineering
product: rf-circuit-design
tags: [rf-circuit-design, impedance-matching, smith-chart, l-network, pi-network, matching-network, s-parameters, s11, return-loss, vswr, vna, vector-network-analyzer, solt-calibration, port-extension, microstrip, cpwg, coplanar-waveguide, 50-ohm, antenna-matching, self-resonant-frequency, qucs, rf-layout]
level: advanced
status: gated
description: "Match RF loads to 50 ohm: Smith chart L-networks, S11 targets, microstrip/CPWG geometry, real-part parasitics, VNA calibration and tuning on the board."
sources:
  - "Pozar, Microwave Engineering"
  - "Bowick, RF Circuit Design"
  - "Ludwig & Bogdanov, RF Circuit Design: Theory and Applications"
  - "Wadell, Transmission Line Design Handbook"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# RF impedance matching — design on the chart, finish on the VNA

**Goal:** transform a load impedance (antenna, LNA input, PA output, filter port) to
50 Ω over the band of interest, with a layout that keeps the match you designed and a
footprint that lets you tune it on the real board.

## 1. Know the load and the target
- Get the load impedance at the band edges and centre: datasheet S-parameters
  (Touchstone `.s2p`), recommended match, or a VNA measurement of the real part on
  the real board.
- Pick the spec: **S11 ≤ −10 dB** (VSWR ≈ 1.9, ~10 % power reflected; computed: |Γ| = 0.316, VSWR 1.92, |Γ|² = 0.10) is the usual
  minimum for antennas; **≤ −15 to −20 dB** for amplifier interstages and test ports.
- Matching for maximum power (conjugate) vs. for noise (LNA Γopt) vs. for output
  power (PA load-pull) are different targets. Know which you want.

## 2. Design the network
**L-network** (two reactive elements) is the default. For real resistances Rhigh and
Rlow, loaded Q = √(Rhigh/Rlow − 1) (e.g. 50 to 10 Ω gives Q = 2, 3.18 nH series and 6.37 pF shunt at 1 GHz, computed; two sections via √(Rhigh·Rlow) = 22.4 Ω halve Q to 1.11 each); the shunt element goes on the high-resistance
side. Higher Q → narrower bandwidth. If the required Q is too high for the
bandwidth, match in two L-sections via an intermediate resistance (√(Rhigh·Rlow)) to
lower Q and widen the band.

On the Smith chart (impedance/admittance overlay):
- Series L moves clockwise along a constant-resistance circle; series C counter-
  clockwise.
- Shunt C moves clockwise along a constant-conductance circle; shunt L counter-
  clockwise.
- Pick the path that reaches the centre with the fewest, most practical values
  (avoid < 0.5 pF and < 1 nH where tolerance dominates, a rule of thumb (gated: unconfirmed, source is paywalled or blocked)).

Tools: a Smith chart app (several free ones exist), Qucs-S, or a vendor RF
simulator. Simulate with **vendor S-parameter models of the actual capacitors and
inductors**, not ideal parts — at GHz, a 0402 capacitor's ESL and pad capacitance
shift the result noticeably.

## 3. Choose parts
- Capacitors: C0G/NP0, RF series (high Q, known ESR). Inductors: multilayer or
  wire-wound RF types with **self-resonant frequency ≥ ~2× (better 3×) the
  operating frequency** (rule of thumb (gated: unconfirmed, source is paywalled or blocked)); above SRF an inductor is a capacitor.
- Tolerance: ±0.1 pF or ±2 % where available; the match moves with part tolerance.

## 4. Layout preserves the match
- **Transmission lines**: 50 Ω microstrip or grounded coplanar waveguide (CPWG) on a
  defined stack-up. CPWG is attractive on thin-prepreg 4-layer boards because the
  required width is closer to pad width. Compute with a field solver using the
  fab's εr at frequency (FR-4 roughly 4.0–4.4 at 1–2 GHz, varies by laminate (gated: unconfirmed, source is paywalled or blocked)).
- Keep the matching parts **close to the device pin**; any line between device and
  match is part of the transformation and must be modelled.
- **Pad capacitance**: pads much wider than the line add shunt C. On thin dielectrics
  consider a ground cutout under large pads (model it).
- Via fence along CPWG and around the RF section, stitching every ~λ/10 to λ/20 at
  the highest frequency of concern (rule of thumb (gated: unconfirmed, source is paywalled or blocked)).
- Lay out a **pi footprint (shunt–series–shunt)** even if you only need an L: fit a
  0 Ω in the series pad and leave shunt pads empty until tuning.

## 5. Measure and tune on the VNA
1. Calibrate (SOLT, or TRL for higher accuracy) at the end of your cable/fixture.
2. Move the reference plane to the match: use port extension or de-embedding with a
   fixture model, or solder a semi-rigid pigtail and calibrate at its tip. An
   un-extended cable rotates the reflection on the chart and makes values meaningless.
3. Measure the raw load (match pads with 0 Ω series, no shunts) and design from the
   *measured* point.
4. Fit parts, re-measure, iterate. For antennas measure **in the final enclosure,
   with batteries/cables in place**, and away from your hand and the bench metal.
5. Check across the full band and over temperature/production spread if possible.

## Gotchas
- Ground return through a long via adds inductance to shunt elements — use two vias
  per shunt pad at GHz.
- Matching only at the centre frequency then discovering S11 is −6 dB at a band edge.
- Using a 50 Ω cable as a "probe" while it radiates (common-mode current on the
  outside of the shield) changes antenna measurements; use a ferrite/sleeve balun.

## Verify
- [ ] S11 meets the spec across the whole band, measured at the corrected reference plane.
- [ ] Component values sit on the real part series and their SRF is well above the band.
- [ ] Transmission-line widths come from a field solver on the actual stack-up.
- [ ] The match was tuned with the board in its final mechanical environment.
- [ ] Tolerance analysis (or a few boards) shows the match holds production spread.
