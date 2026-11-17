---
id: engineering-technology.electrical-engineering.circuit-analysis.phasor-and-three-phase-analysis
name: phasor-and-three-phase-analysis
category: engineering-technology
field: electrical-engineering
product: circuit-analysis
tags: [circuit-analysis, phasor, ac-analysis, nodal-analysis, mesh-analysis, admittance-matrix, impedance, complex-power, power-factor, pf-correction, three-phase, per-phase-equivalent, wye-delta, star-delta, line-voltage, phase-sequence, symmetrical-components, rms, kcl, kvl, thevenin, numpy, spice, ltspice, complex-power-triangle, line-phase-relations, unbalanced-three-phase]
level: practitioner
status: verified
description: "Solve AC circuits with phasors and nodal analysis, then balanced three-phase systems: per-phase equivalents, Y-delta, complex power, PF correction."
sources:
  - "Alexander & Sadiku, Fundamentals of Electric Circuits"
  - "Hayt, Kemmerly & Durbin, Engineering Circuit Analysis"
  - "Nilsson & Riedel, Electric Circuits"
  - "Grainger & Stevenson, Power System Analysis (symmetrical components)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Phasor and three-phase analysis — the sinusoidal steady state without sign errors

**Goal:** get correct magnitudes, angles and powers for single- and three-phase AC
circuits quickly, with a method that scales (nodal matrices) and checks that catch
the usual mistakes.

## 1. Conventions (decide once, write them on the page)
- Phasors in **RMS**, not peak, unless stated — power formulas then need no ½.
- Reference angle: one source or the line-to-neutral voltage of phase A at 0°.
- Passive sign convention: current enters the + terminal of a load → P > 0 absorbed.
- Phase sequence ABC (positive): B lags A by 120°, C lags B by 120°.

## 2. Convert to the frequency domain
`Z_R = R`, `Z_L = jωL`, `Z_C = 1/(jωC) = −j/(ωC)`, ω = 2πf. A source
`v(t) = Vm cos(ωt + θ)` becomes `(Vm/√2)∠θ`. Only valid at a single frequency in steady
state; for multiple frequencies use superposition per frequency, never add phasors
of different frequencies.

## 3. Nodal analysis in matrix form
Build `Y · V = I` (Y = admittance matrix, diagonal = sum of admittances at the node,
off-diagonal = −admittance between nodes). Solve numerically:
```python
import numpy as np
w = 2*np.pi*50
ZL, ZC, R = 1j*w*10e-3, 1/(1j*w*100e-6), 5.0
Y = np.array([[1/R + 1/ZL, -1/ZL],
              [-1/ZL,      1/ZL + 1/ZC]])
I = np.array([230/R, 0])            # source 230∠0 V behind R as Norton
V = np.linalg.solve(Y, I)
print(abs(V), np.degrees(np.angle(V)))   # numpy angles are radians
```
Run this session: |V| = 226.6 V and 251.4 V, both at −9.89°; the residual of Y·V − I is 1.4e-14.
Voltage sources between two non-reference nodes → supernode, or convert to Norton.
Thevenin equivalent at a port: open-circuit voltage + impedance with sources zeroed.

## 4. Complex power
`S = V · I*` (conjugate of current) = P + jQ. Inductive load: Q > 0, current lags.
|S| in VA, P in W, Q in var, pf = cos(∠V − ∠I).
**PF correction:** `Qc = P (tan φ1 − tan φ2)`; for a capacitor per phase in Y,
`C = Qc / (3 · ω · V_LN²)`.

## 5. Balanced three-phase: reduce to one phase
1. Convert every Δ to Y: `Z_Y = Z_Δ / 3`.
2. Solve phase A alone with V_LN and neutral at 0 V (balanced → no neutral current).
3. Rebuild B and C by shifting −120°, +120°.
Relations (ABC sequence): `V_AB = √3 · V_AN ∠ +30°` (computed for B lagging A by 120°); in a Δ load `I_line = √3 · I_phase ∠ −30°`.
Power: `P = √3 · V_LL · I_L · cos φ`, `S_3φ = 3 · V_LN · I_L*`.

Worked: 400 V, 50 Hz, 10 kW at pf 0.8 lagging →
I = 10 000 / (√3 × 400 × 0.8) = 18.0 A; Q = 7.5 kvar.
To pf 0.95: Qc = 10 × (0.75 − 0.329) = 4.2 kvar total (1.4 kvar/phase), which is 83.8 µF per phase in star at 50 Hz (all computed with Python).

## 6. Unbalanced systems
Use mesh/nodal on the full three-phase circuit, or **symmetrical components**
(`a = 1∠120°`; V0, V1, V2 from the Fortescue transform) — the standard route for
unsymmetrical faults. An open neutral with unbalanced Y loads shifts the star point:
solve the neutral voltage explicitly, don't assume 0 V.

## 7. Gotchas
- Mixing peak and RMS gives powers off by 2.
- The +30° for V_LL holds for ABC; with ACB sequence it is −30°.
- `I*`, not I, in the complex power product — wrong sign of Q otherwise.
- A "kVA" rating on a three-phase nameplate is total, not per phase.
- Transients (switching): first-order τ = RC or L/R; ~5τ to settle (99.3%, computed 1 − e^-5); solve with
  Laplace or simulate — phasors don't apply during transients.

## Verify
- [ ] KCL holds at every node to numerical precision (sum of currents ≈ 0).
- [ ] Power balance: Σ source S = Σ load S (Tellegen).
- [ ] Line and phase quantities differ by √3 where they should, with the right ±30°.
- [ ] Inductive loads show lagging current and positive Q.
- [ ] A SPICE `.ac` run or second method reproduces key results.
