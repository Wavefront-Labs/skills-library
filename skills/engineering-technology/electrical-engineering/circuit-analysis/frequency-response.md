---
id: engineering-technology.electrical-engineering.circuit-analysis.frequency-response
name: frequency-response
category: engineering-technology
field: electrical-engineering
product: circuit-analysis
tags: [bode-plot, bode-plot-construction, circuit-analysis, electrical-engineering, frequency-response, low-pass-filter, passive-filter-design, q-factor, resonance, rlc-filter]
level: practitioner
status: draft
description: "Draw Bode plots, size resonant circuits and passive filters from poles, zeros, Q and loading."
sources:
  - "https://www.ncees.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Frequency response, resonance and passive filters

1. Write `H(s)` in factored form and plot straight-line asymptotes: each pole drops slope by 20 dB/decade at its corner, each zero adds 20 dB/decade; phase moves 90 degrees over about two decades centred on the corner.
2. First-order RC low-pass: `fc = 1/(2 pi R C)`; -3 dB and -45 degrees there.
3. Series RLC: `w0 = 1/sqrt(LC)`, `Q = w0 L/R`, bandwidth `BW = w0/Q`. At resonance voltage across L or C is `Q` times the source voltage, which can exceed insulation or component ratings.
4. Passive filter design: choose the type (low-pass, high-pass, band-pass, notch), the order from required stopband attenuation, then scale normalised prototype values by impedance and frequency. Source and load impedance change the response; buffer or include them in the calculation.
5. Component caveats: inductor self-resonance, capacitor ESR and tolerance shift the real corner.

**Verify:** sweep the circuit in a simulator or with a network analyser and compare the -3 dB point and the stopband attenuation to the design target.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
