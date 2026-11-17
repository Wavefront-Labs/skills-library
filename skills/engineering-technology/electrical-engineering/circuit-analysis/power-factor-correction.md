---
id: engineering-technology.electrical-engineering.circuit-analysis.power-factor-correction
name: power-factor-correction
category: engineering-technology
field: electrical-engineering
product: circuit-analysis
tags: [capacitor-bank, capacitor-bank-sizing, circuit-analysis, detuned-reactor, detuned-reactor-selection, electrical-engineering, harmonic-resonance, kvar, power-factor, power-factor-correction]
level: practitioner
status: draft
description: "Size power-factor-correction capacitor banks, check voltage scaling and harmonic resonance, and decide when detuned reactors are needed."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Power factor correction: bank sizing and harmonic safety

**Goal:** raise displacement power factor from `pf1` to `pf2` without creating a resonance.

1. Required reactive power: `Qc = P (tan(acos pf1) - tan(acos pf2))`. Example: 500 kW, 0.80 to 0.95: `500 x (0.7500 - 0.3287) = 210.7 kvar`; round to the nearest standard step (for example a 200 kvar bank in steps).
2. Capacitor output scales with the square of applied voltage: `Q = Qrated (V/Vrated)^2`; a bank rated at 480 V on a 440 V system delivers about 84 % of its nameplate kvar.
3. Resonance check: the parallel resonance with the supply sits near `h = sqrt(Ssc / Qc)` (Ssc = short-circuit MVA at the bus, Qc in the same unit). If `h` lands near a characteristic harmonic of the load (5, 7, 11 for six-pulse drives) the bank can amplify current.
4. Detuned reactors: series reactor of `p` percent of the capacitor reactance gives series resonance at `f0 = f / sqrt(p/100)`. Common choices are 7 % (about 189 Hz on 50 Hz, 227 Hz on 60 Hz) and 14 % (about 134 Hz on 50 Hz); 5.67 % tunes near 210 Hz at 50 Hz. Rated capacitor voltage must exceed the system voltage because the reactor raises capacitor voltage by `1/(1 - p/100)`.
5. Switching: use contactors rated for capacitive inrush or add inrush reactors; automatic controllers step banks on measured kvar with a time delay.
6. Avoid correcting to leading power factor at light load (overvoltage, generator problems).

**Failure modes:** plain capacitors on a bus with significant non-linear load; sizing at nameplate voltage; ignoring discharge time before maintenance.

**Verify:** measure pf and harmonic currents before and after; confirm capacitor current does not exceed its rated RMS with harmonics included.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
