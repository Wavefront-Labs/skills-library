---
id: engineering-technology.telecommunications-engineering.antenna-design.patch-antenna-design-and-matching
name: patch-antenna-design-and-matching
category: engineering-technology
field: telecommunications-engineering
product: antenna-design
tags: [telecommunications-engineering, antenna-design, microstrip-patch, patch-antenna, transmission-line-model, inset-feed, quarter-wave-transformer, impedance-matching, s11, return-loss, vswr, substrate, fr-4, rogers-ro4003c, rt-duroid-5880, openems, cst, hfss, fdtd, fem, far-field, near-field, array-factor, grating-lobes, vna, smith-chart]
level: practitioner
status: gated
description: "Design a rectangular microstrip patch: transmission-line sizing, substrate choice, inset or quarter-wave matching to S11 < -10 dB, openEMS/CST/HFSS simulation, far-field and array checks."
sources: ["Balanis, Antenna Theory: Analysis and Design", "Garg, Bhartia, Bahl and Ittipiboon, Microstrip Antenna Design Handbook", "Pozar, Microwave Engineering", "IEEE Std 149 Test Procedures for Antennas", "IEEE Std 145 Definitions of Terms for Antennas", "openEMS project documentation and tutorials", "Rogers Corporation RO4000 and RT/duroid laminate data sheets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patch antenna design and matching — from equations to a measured S11

**Goal:** size a rectangular microstrip patch for a target frequency, match it to 50 ohms (S11 < -10 dB across the band), and confirm the pattern and gain by simulation and measurement.

## 1. Choose the substrate

| Laminate | er (design) | tan d | Notes |
|---|---|---|---|
| FR-4 | ~4.3-4.6 (varies by lot and frequency) | ~0.02 | Cheap; efficiency often 40-60%; avoid above ~3 GHz for precision work (all FR-4 figures (gated: unconfirmed, source is paywalled or blocked)) |
| Rogers RO4003C | 3.55 design Dk (3.38 +/- 0.05 process spec) | ~0.0027 at 10 GHz (Rogers product page checked) | FR-4 processable; good default |
| RT/duroid 5880 | 2.2 (2.20 +/- 0.02 at 10 GHz) | ~0.0009 at 10 GHz (Rogers product page checked) | Wider bandwidth, higher efficiency, softer |

Thicker, lower-er substrates give more bandwidth (a few percent, roughly proportional to h/lambda) and efficiency, but surface waves and feed inductance grow above h of about 0.05 lambda_0 ((gated: unconfirmed, source is paywalled or blocked)). Use the manufacturer's **design Dk**.

## 2. Size the patch (transmission-line model)

With c = 3e8 m/s, f0 the design frequency and h the substrate height:

- W = c / (2 f0) x sqrt(2 / (er + 1))
- e_eff = (er + 1)/2 + (er - 1)/2 x (1 + 12 h/W)^(-1/2)
- dL = 0.412 h x (e_eff + 0.3)(W/h + 0.264) / ((e_eff - 0.258)(W/h + 0.8))
- L = c / (2 f0 sqrt(e_eff)) - 2 dL

Example, 2.45 GHz on FR-4 (er 4.4, h 1.6 mm): W = 37.3 mm, e_eff = 4.08, dL = 0.74 mm, **L = 28.8 mm** (recomputed: 37.26, 4.081, 0.739, 28.83; the formulas are the standard transmission-line model, textbook not fetched, (gated: unconfirmed, source is paywalled or blocked)). Extend the ground plane at least about 6h beyond the patch on every side ((gated: unconfirmed, source is paywalled or blocked)).

## 3. Match the feed

- Edge input resistance is typically 150-300 ohms ((gated: unconfirmed, source is paywalled or blocked)); take it from simulation.
- **Inset feed:** R_in(y0) = R_edge x cos^2(pi y0 / L). Solve for y0 that gives 50 ohms (often about 0.3 L; recomputed y0 = 0.304 L for 200 ohm edge resistance, 0.31 L at 150 ohm and 0.37 L at 300 ohm). Notch gap about the 50-ohm line width or slightly less; the notch shifts f0 slightly, so re-tune L afterwards.
- **Quarter-wave transformer:** Z_t = sqrt(50 x R_edge), length lambda_g / 4 at f0. Narrowband, and a high Z_t may be too thin to etch.
- **Probe feed:** pin at the 50-ohm point; probe inductance grows with h.
- Acceptance: **S11 <= -10 dB** (VSWR <= 1.92, 10% reflected power) across the band. Tighter specs: -15 dB (VSWR 1.43) (all computed: 1.925, 0.10, 1.433).

## 4. Simulate

- **openEMS** (FDTD, Octave/Python), **CST** (FIT time domain), **HFSS** (FEM frequency domain), or Sonnet/ADS Momentum (planar MoM).
- Mesh at lambda/20 in the dielectric or finer ((gated: unconfirmed, source is paywalled or blocked)), with refinement at patch edges and the feed. Put PML or radiation boundaries at least lambda/4 away. Run time-domain solvers until energy decays at least 40 dB (openEMS end criterion about 1e-4 or lower, (gated: unconfirmed, source is paywalled or blocked)).
- In the final pass, model copper thickness, connector and solder mask, and sweep er +/-0.1 and etch +/-0.05 mm.
- Read out S11, Smith-chart impedance, realised gain, radiation efficiency and E/H-plane cuts. A single patch typically gives 6-8 dBi on low-loss substrate and less on FR-4 ((gated: unconfirmed, source is paywalled or blocked)).

## 5. Measure

Calibrate the VNA (SOLT) at the cable end and de-embed the connector. Far-field distance R >= 2 D^2 / lambda (and R >> D, R >> lambda), with D the largest antenna dimension. Measure gain and patterns in an anechoic chamber or on a near-field scanner with probe compensation.

## 6. Array basics

Realised gain then feeds engineering-technology.telecommunications-engineering.rf-link-budget.point-to-point-link-budget. 
Array factor for N equally spaced elements: AF = sum over n of exp(j n (k d cos(theta) + beta)). With d = lambda/2 there are no grating lobes for any scan angle. In general the condition is d/lambda < 1 / (1 + |sin(theta_0)|) for scan angle theta_0 measured from broadside (computed: 0.5 at 90 degrees, 0.667 at 30 degrees). Doubling the element count adds about 3 dB of directivity. Amplitude tapers (for example Taylor) push sidelobes below the uniform -13 dB at the cost of beamwidth.

## Gotchas

- FR-4 er drifts with frequency and supplier. Expect 2-4% frequency error ((gated: unconfirmed, source is paywalled or blocked)), so tune on a prototype.
- Feed-cable currents on a small ground plane radiate. Use ferrite or a sleeve balun, or S11 changes when you touch the cable.
- Good S11 is not good efficiency; a lossy antenna can match well.
- Housings, radomes and nearby metal detune the patch; simulate in the final enclosure.

## Verify

- [ ] Hand-calculated W, L and inset agree with the simulated resonance to within a few percent.
- [ ] Simulated and measured S11 <= -10 dB across the full operating band, including tolerance sweeps.
- [ ] Mesh convergence: refining the mesh moves f0 by less than 0.5%.
- [ ] Realised gain and radiation efficiency meet spec, not just S11.
- [ ] Pattern measured at or beyond 2 D^2 / lambda (or with near-field transformation) and matches simulation within a couple of dB in the main lobe.
